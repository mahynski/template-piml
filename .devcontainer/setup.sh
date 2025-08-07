#!/bin/bash
devcontainer_path="$(dirname "$(realpath "$0")")/";
requirements="$devcontainer_path/requirements.txt";
project_dir="$(realpath $devcontainer_path/../)";
project_name="$(basename $project_dir)";
root_dir="$(realpath $project_dir/../)";
cd $root_dir;
uv init $project_name --bare --no-workspace;
cd $project_dir;
uv add mlflow jupyterlab pydantic-settings pre-commit;
uv add -r $requirements;
