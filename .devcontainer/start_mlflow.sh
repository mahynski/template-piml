#!/bin/bash
source "$(dirname "$(realpath "$0")")/../.venv/bin/activate";
head_path="$(dirname "$(realpath "$0")")/mlflow";
mkdir -p $head_path;
backend_path="$head_path/mlruns.db";
artifacts_path="$head_path/mlartifacts";
mlflow server --host 127.0.0.1 --port 1235 --backend-store-uri sqlite:///$backend_path --artifacts-destination $artifacts_path