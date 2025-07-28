#!/bin/bash
source "$(dirname "$(realpath "$0")")/../.venv/bin/activate";
export MLFLOW_TRACKING_URI="http://127.0.0.1:1235";
jupyter lab --port 1234 --ip='*' --NotebookApp.token='' --NotebookApp.password='';