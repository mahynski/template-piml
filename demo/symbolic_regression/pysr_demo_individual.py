"""
Use PySR to fit the x'' and y'' data from the NN separately.
See https://ai.damtp.cam.ac.uk/pysr/ for API details.

This assumes we have 2 files, ax.txt and ay.txt which contain
[x, y, x', y', x_hat], [x, y, x', y', y_hat] where
[x, y, x', y'] is the state of the system at a given time and
x"_hat and y"_hat are the predicted residual accelerations.

In this case, we are doing a separate regression for x"_hat and
y"_hat to predict them individually.
"""
import os
import pysr
import numpy as np 

from pysr import PySRRegressor

def load(filename): # Load from Jupyter
    X_tot = np.loadtxt(filename)
    X = X_tot[:, :-1]
    y = X_tot[:, -1]

    return X, y

if __name__ == '__main__':
    run = True

    if run: # Run SR
        for file in ['ax', 'ay']:
            output_directory = file +'_pysr_result'
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            model = PySRRegressor(
                output_directory=output_directory,
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

            model.fit(*load(file+'.txt'))

    # Print results
    model = PySRRegressor.from_file(run_directory="ax_pysr_result/"+os.listdir('ax_pysr_result/')[0])
    print(model)

    model = PySRRegressor.from_file(run_directory="ay_pysr_result/"+os.listdir('ay_pysr_result/')[0])
    print(model)
