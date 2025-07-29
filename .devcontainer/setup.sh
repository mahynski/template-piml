#!/bin/bash
devcontainer_path="$(dirname "$(realpath "$0")")/"
requirements="$devcontainer_path/requirements.txt"
root="$devcontainer_path/../"
cd $root
uv init --bare
uv add mlflow jupyterlab pydantic-settings
uv add -r $requirements
