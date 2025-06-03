#!/bin/bash
head_path="$(dirname "$(realpath "$0")")/mlflow";
if [[ ! -e $head_path ]]; then
    mkdir $head_path;
fi
backend_path="$head_path/mlruns.db";
artifacts_path="$head_path/mlartifacts";
mlflow server --host 127.0.0.1 --port 4342 --backend-store-uri sqlite:///$backend_path --artifacts-destination $artifacts_path