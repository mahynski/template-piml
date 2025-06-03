#!/bin/bash
# Start a Jupyter Notebook server with no password so we can easily access it from base env
export MLFLOW_TRACKING_URI="http://127.0.0.1:4342";
jupyter notebook --port 1234 --ip='*' --NotebookApp.token='' --NotebookApp.password='';