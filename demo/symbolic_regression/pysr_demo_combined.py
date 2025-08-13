"""
Use PySR to fit the [x'', y''] data from the NN.
See https://ai.damtp.cam.ac.uk/pysr/ for API details.

This assumes we have 2 files, ax.txt and ay.txt which contain
[x, y, x', y', x_hat], [x, y, x', y', y_hat] where 
[x, y, x', y'] is the state of the system at a given time and 
x"_hat and y"_hat are the predicted residual accelerations.

In this case, we are doing a joint regression for x"_hat and
y"_hat to predict them together.
"""
import os
import pysr
import numpy as np 

from pysr import PySRRegressor, TensorBoardLoggerSpec

def load(filenames): # Load from Jupyter
    y = []
    for file in filenames:
        X_tot = np.loadtxt(file)
        X = X_tot[:, :-1]
        y.append(X_tot[:, -1].reshape(-1,1))
    y = np.hstack(y)

    # Assumes X is the same in each file
    return X, y

if __name__ == '__main__':
    run = True
    
    head = 'pysr_result/'

    if run: # Run SR
        if not os.path.exists(head):
            os.makedirs(head)

        X, y = load(['ax.txt', 'ay.txt'])

        logger_spec = TensorBoardLoggerSpec(
            log_dir=head+"logs/run",
            log_interval=10,  # Log every 10 iterations
        )

        model = PySRRegressor(
            output_directory=head,
            maxsize=20,
            niterations=40,  # < Increase me for better results
            binary_operators=["+", "*"],
            unary_operators=[
                "cos",
                "exp",
                "sin",
                "inv(x) = 1/x",
                # ^ Custom operator (julia syntax)
            ],
            extra_sympy_mappings={"inv": lambda x: 1 / x},
            # ^ Define operator for SymPy as well
            elementwise_loss="loss(prediction, target) = (prediction - target)^2",
            # ^ Custom loss function (julia syntax)
        )

        model.fit(X, y)

    # Print results
    model = PySRRegressor.from_file(run_directory=head+os.listdir(head)[0])
    
    print(model)

    # View on tensorboard
    # tensorboard --logdir pysr_result/logs/
