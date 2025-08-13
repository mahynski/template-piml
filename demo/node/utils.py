"""
Demonstration of NODEs.

Author: Nathan A. Mahynski
"""
import torch

import numpy as np
import pytorch_lightning as pl
import torch.nn as nn

from numpy.typing import NDArray
from torchdiffeq import odeint as td_odeint
from typing import Any, ClassVar, Union

class Trajectory2D:
    """2D trajectory for an object.""" 
    t: NDArray[np.floating]
    x: NDArray[np.floating]
    y: NDArray[np.floating]
    vx: NDArray[np.floating]
    vy: NDArray[np.floating]
    mass: np.floating

    def __init__(self, t: NDArray[np.floating], x: NDArray[np.floating], y: NDArray[np.floating], vx: NDArray[np.floating], vy: NDArray[np.floating], mass: float) -> None: # Can expand to include other intrinsic properties like A, Cd, etc.
        """
        Instantiate the trajectory.

        Parameters
        ----------
        t : ndarray(float, ndim=1)
            Time for each point.

        x : ndarray(float, ndim=1)
            X-coordinate for each point.

        y : ndarray(float, ndim=1)
            Y-coordinate for each point.

        vx : ndarray(float, ndim=1)
            X-velocity for each point.

        vy : ndarray(float, ndim=1)
            Y-velocity for each point.

        mass : float
            Mass of the object.
        """
        assert len(t) == len(x) == len(y) == len(vx) == len(vy)
        setattr(self, "t", t)
        setattr(self, "x", x)
        setattr(self, "y", y)
        setattr(self, "vx", vx)
        setattr(self, "vy", vy)
        setattr(self, "mass", mass)
    
    def __getitem__(self, i: int) -> list:
        """Retrieve the ith entry in the trajectory."""
        return [self.t[i], self.x[i], self.y[i], self.vx[i], self.vy[i], self.mass]

    def __len__(self) -> int:
        """Total length of the trajectory."""
        return len(self.t)


def build_time_lagged_set(trajectories: list[Trajectory2D], max_incrs: int = 3) -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    """
    For each point in each trajectory create an (initial, final) state pair.

    Parameters
    ----------
    trajectories : list(Trajectory2D)
        List of trajectories for an object.

    max_incrs : int, optional(default=3)
        Number of time points to look into future and create a time-lagged pair.

    Returns
    -------
    X_train : ndarray(float, ndim=2)
        Rows of initial states to use as training. Each state is a [t0, -x0-, -param-] form.

    y_train : ndarray(float, ndim=2)
        Rows of final states to use as targets during training. Each state is a [t1, -x1-, -param-] form.

    Notes
    -----
    The time gaps might vary, which is ok.  We just build a set of targets that up to `max_incrs` number of observations in the future from each starting point.
    """
    X_train, y_train = [], []

    for traj in trajectories:
        for i in range(len(traj)-1): # t0 starting points
            initial_state = traj[i]
            for j in range(1, max_incrs+1): # t1 ending points
                if i+j < len(traj):
                    final_state = traj[i+j]
                    
                    X_train.append(initial_state) # Retain absolute time since for future applications that might matter
                    y_train.append(final_state)
    
    X_train = np.vstack(X_train)
    y_train = np.vstack(y_train)

    return X_train, y_train

class Dynamics(nn.Module): 
    """NODE for dynamics (acceleration components) of system."""
    vector_field_resid: ClassVar[nn.Module]
    method: ClassVar[str]
    atol: ClassVar[float]
    rtol: ClassVar[float]
    ndim: ClassVar[int]
    
    def __init__(self, vector_field_resid: nn.Module, method: str = 'dopri8', atol: float = 1.0e-8, rtol: float = 1.0e-8) -> None:
        """
        Instantiate the dynamics.

        Parameters
        ----------
        vector_field_resid : nn.Module
            Neural network to fit the residual of the known dynamics. It should take the state vector [t0, -x0-, -params-] and output just the positions at t1.

        method : str, optional(default='dopri8')
            ODE solver to use.

        atol : float, optional(default=1.0e-8)
            Absolute tolerance in ODE solver.

        rtol : float, optional(default=1.0e-8)
            Relative tolerance in ODE solver. 
        """
        super().__init__()
        setattr(self, "vector_field_resid", vector_field_resid)
        setattr(self, "method", method)
        setattr(self, "atol", atol)
        setattr(self, "rtol", rtol)
        setattr(self, "ndim", vector_field_resid[-1].out_features)
        assert(self.ndim == 2)
        
    def forward(self, t: torch.Tensor, state: torch.Tensor) -> torch.Tensor:
        """
        Compute the derivative of the state with respect to time.

        User should implement this method in derived classes.

        Parameters
        ----------
        t : torch.tensor(ndim=0)
            Current time of the system's state. Ignored for autonomous systems.

        state : torch.tensor(ndim=1)
            Current system state, e.g., [x, y, x', y'].

        Returns
        -------
        deriv : torch.tensor(ndim=1)
            Derivative of system state, e.g., [x', y', x'', y''].
        """
        raise NotImplementedError

    def propagate(self, x0: torch.Tensor, t1: torch.Tensor) -> torch.Tensor:
        """
        Propagate a single initial state forward in time by a single increment.

        Parameters
        ----------
        x0 : torch.tensor(ndim=1)
            Initial state of the system, e.g., [t0, x0, y0, vx0, vy0, m].

        t1 : torch.tensor(ndim=0)
            Absolute time to integrate the system forward from `t0` to `t1`.

        Returns
        -------
        trajectory : torch.tensor(ndim=1)
            New position of the system at `t1`, e.g., [x1, y1].
        """
        t0 = x0[0]
        state = x0[1:1+2*self.ndim] # [x0, y0, vx0, vy0]
        solution = td_odeint(self, 
                          state, 
                          torch.cat([t0.view(1), t1.view(1)]), # Must given t0 for odeint API
                          atol=self.atol, 
                          rtol=self.rtol, 
                          method=self.method
                         )
        trajectory = solution[1, 0:self.ndim] # Select (x, y) from final state @t1
        
        return trajectory
        
class Learner(pl.LightningModule):
    """Train the NODE."""
    system: ClassVar[nn.Module]
    decay: ClassVar[float]
    ndim: ClassVar[int]
    
    def __init__(self, ndim: int, system: nn.Module, decay: float = 1.0) -> None:
        """
        Instantiate the learner.

        Parameters
        ----------
        ndim : int
            Number of dimensions (2) in the system.
            
        system : nn.Module
            Neural network which takes a state and outputs the second derivative of coordinates (accelerations).

        decay : float, optional(default=1.0)
            Decay factor to weight time points that are further away from starting point differently. Default of 1.0 applies no weighting so all points are treated equally.
        """
        super().__init__()
        self.save_hyperparameters()
        setattr(self, "ndim", ndim)
        setattr(self, "system", system)
        setattr(self, "decay", decay)
    
    def forward(self, curr_state: torch.Tensor, target_state: torch.Tensor) -> torch.Tensor:
        """
        Perform a forward pass through the network to propagate the system state.

        Parameters
        ----------
        curr_state : torch.Tensor
            Current state of the system [t0, -x0-, -params-].
            
        target_state : torch.Tensor
            Final (target) state of the system [t1, -x1-, -params-].
            
        Returns
        -------
        trajectory : torch.Tensor
            Final positions of objects at `t1`.
        """
        trajectory = self.system.propagate(x0=curr_state, t1=target_state[0])
        
        return trajectory
    
    def training_step(self, batch, batch_idx) -> dict[str, float]:
        """
        Training step.

        Parameters
        ----------
        batch : iterable
            (curr_state, target_state) for this batch of training data.

        batch_idx : int
            Batch index.

        Returns
        -------
        loss : dict
            Dictionary of {'loss': loss}.
        """
        curr_state_batch, target_state_batch = batch
        loss = torch.tensor(0.0, requires_grad=True)
        for i, (curr_state, target_state) in enumerate(zip(curr_state_batch, target_state_batch)):
            trajectory = self(curr_state, target_state)
            weight = self.decay**(target_state[0] - curr_state[0])
            loss = loss + torch.sum(torch.square(trajectory - target_state[1:1+self.ndim]))*weight
        loss = loss.mean()
        
        metrics = {"loss": loss}
        self.log_dict(metrics, on_step=True, on_epoch=True, prog_bar=True, logger=True) # logs metrics for each training_step, and the average across the epoch, to the progress bar and logger

        return metrics

    def test_step(self, batch, batch_idx) -> dict[str, float]:
        """
        Testing or inference step.

        Parameters
        ----------
        batch : iterable
            (curr_state, target_state) for this batch of test data.

        batch_idx : int
            Batch index.

        Returns
        -------
        loss : dict
            Dictionary of {'test_loss': loss}.
        """
        curr_state_batch, target_state_batch = batch
        loss = torch.tensor(0.0, requires_grad=True)
        trajectories = torch.empty((curr_state_batch.shape[0], self.ndim), requires_grad=False)
        for i, (curr_state, target_state) in enumerate(zip(curr_state_batch, target_state_batch)):
            trajectory = self(curr_state, target_state)
            trajectories[i] = trajectory
            weight = self.decay**(target_state[0] - curr_state[0])
            loss = loss + torch.sum(torch.square(trajectory - target_state[1:1+self.ndim]))*weight
        loss = loss.mean()
        
        metrics = {"test_loss": loss}
        self.log_dict(metrics)
        
        return metrics

    def validation_step(self, batch, batch_idx) -> dict[str, float]:
        """
        Validation step.

        Parameters
        ----------
        batch : iterable
            (curr_state, target_state) for this batch of validation data.

        batch_idx : int
            Batch index.

        Returns
        -------
        loss : dict
            Dictionary of {'val_loss': loss}.
        """
        curr_state_batch, target_state_batch = batch
        loss = torch.tensor(0.0, requires_grad=True)
        for i, (curr_state, target_state) in enumerate(zip(curr_state_batch, target_state_batch)):
            trajectory = self(curr_state, target_state)
            weight = self.decay**(target_state[0] - curr_state[0])
            loss = loss + torch.sum(torch.square(trajectory - target_state[1:1+self.ndim]))*weight
        loss = loss.mean()
        
        metrics = {"val_loss": loss}
        self.log_dict(metrics)

        return metrics
    
    def predict_step(self, batch, batch_idx) -> torch.Tensor:
        """
        Validation step.

        Parameters
        ----------
        batch : iterable
            (curr_state, target_state) for this batch of predict data.

        batch_idx : int
            Batch index.

        Returns
        -------
        trajectories : torch.Tensor
            Final positions of objects.
        """
        curr_state_batch, target_state_batch = batch
        trajectories = torch.empty((curr_state_batch.shape[0], self.ndim), requires_grad=False)
        for i, (curr_state, target_state) in enumerate(zip(curr_state_batch, target_state_batch)):
            trajectory = self(curr_state, target_state)
            trajectories[i] = trajectory
        
        return trajectories
        
    def configure_optimizers(self) -> None:
        """
        Configure optimizer.
        """
        return torch.optim.Adam(self.parameters(), lr=0.01)