# Using this Template

<img src="logo.png" align="right" width=110 />

A small set of demonstrations are available in the `projects/` directory which illustrate different PINN implementations in PyTorch and Tensorflow.

To get started:

~~~bash
$ bash .devcontainer/setup.sh
$ bash .devcontainer/start_mlflow.sh
$ bash .devcontainer/start_jupyter.sh
~~~

Then navigate to `demo/` and install the virtual environment with uv.

~~~bash
$ cd projects/demo
$ uv sync
$ uv run ipython kernel install --user --env VIRTUAL_ENV ../.venv --name=demo
~~~

These are already configured with ipykernel, so you can just install the Jupyter kernel directly as shown above.

## Using UV

### General Philosophy of UV Projects

["Projects"](https://docs.astral.sh/uv/concepts/projects/) in [uv](https://docs.astral.sh/uv/) are sequestered bodies of work organized inside a single root directory. These create virtual environments to manage their dependencies separately from others so you can create different projects as needed, e.g., inside some master `projects/` directory. To [create a new project](https://docs.astral.sh/uv/concepts/projects/init/):

~~~bash
$ cd projects/
$ uv init new_project # Creates new project root directory projects/new_project
$ cd new_project
~~~

This creates a `pyproject.toml` without a build system that essentially acts like a `requirements.txt` file.

To [add new dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/) to a project, either:
1. Add directly to `dependencies=[]` in the `pyproject.toml` file, then run `uv sync` to synchronize the environment, or
2. run `uv add new_dependency` from the project root directory.

To (attempt to) update a single package while keeping the rest fixed:

~~~bash
$ uv lock --upgrade-package package_of_interest
~~~

You can further customize your `pyproject.toml` file to configure your project:
* [General configuration guidelines](https://docs.astral.sh/uv/concepts/projects/config/#configuring-projects)
* [Adding PyTorch](https://docs.astral.sh/uv/guides/integration/pytorch/)

To [run](https://docs.astral.sh/uv/concepts/projects/run/) things you can do one of 2 things:
1. Use:

   ~~~bash
   $ uv run my_script.py
   ~~~

2. Activate the environment first then execute like normal:

   ~~~bash
   $ source .venv/bin/activate
   $ python my_script.py
   ~~~

### Packages vs. Projects

You can also create a [new python **package**](https://docs.astral.sh/uv/concepts/projects/init/#packaged-applications) instead of a **project**. The difference is that the package's `pyproject.toml` file will be equipped with a build system, so when it runs it will be installed into the local environment (i.e., often a project as shown below). The package is automatically configured with a `main` function in its `__init__.py` file so you can run the package as shown below.

~~~bash
$ cd projects/new_project
$ uv init --package my_new_package # Create a new package
$ ... # Modify this as needed
$ uv run my_new_package # Installs package into new_project and executes the main() function
~~~

### Jupyter Kernels

It is recommended that you create independent kernels in Jupyter for each project. This way there is a single installation of Jupyter only single server running.

~~~bash
$ ROOT=/path/to/2022-my-new-project # Wherever the root is
$ cd projects/new_project
$ uv add --dev ipykernel # From inside the project directory
$ uv run ipython kernel install --user --env VIRTUAL_ENV $ROOT/.venv --name=new_project # Install the local venv into the server running at ROOT
~~~

Anything you install in the notebook will be installed in the environment but will not be reflected in the `pyproject.toml` file until you `uv sync` that project directory.  Anything you install "normally", e.g., via `uv add`, will be avilable in Jupyter notebooks running this kernel.

## Setup SSH Keys

If you are using this inside a devcontainer you will need to add an ssh key to push changes directly back to your Git account. Follow the instructions below inside your container, OR commit/push changes from a terminal outside of your container.

~~~bash
$ ssh-keygen -t ed25519 # Create a key - press enter each time you are prompted
$ cat ~/.ssh/id_ed25519.pub # Copy the contents of this file
~~~

Go to `User settings > SSH Keys` on your GitLab account or `User > Settings > SSH and GPG Keys` on GitHub. Click `Add new key` and copy the contents above into the `Key` area.  Give it a title and expiration date, then click `Add key`.

## Locking the Environment

"Locking" is the process of resolving your project's dependencies into a lockfile. "Syncing" is the process of installing a subset of packages from the lockfile into the project environment.

Note that when `uv run` commands are executed the environment is [automatically synced and locked](https://docs.astral.sh/uv/concepts/projects/sync/). You can always manually `uv sync` to keep the environment and `pyproject.toml` files consistent.

At the end of a project it is good practice to export the entire environment to a lockfile for posterity, especially if not working in a development container.
See uv's [documentation](https://docs.astral.sh/uv/pip/compile/#locking-requirements) for more information. As an alternative, the approach below works both with and without `uv`.

~~~bash
$ source .project-env/bin/activate
$ uv pip freeze > requirements.in # You can drop "uv" to just rely on pip to handle this
$ uv pip compile requirements.in > requirements.txt # You can drop "uv" to just rely on pip to handle this
~~~

This environment can be recreated later.

~~~bash
$ uv pip install -r requirements.txt
~~~

## Accessing Endpoints

You may need to add a `.cert` file to access certain resources on a local network to avoid a "self-signed certificate" error.  [One solution](https://gist.github.com/anhldbk/8ef2d465152dd4b31429725f4534603f) is to:

~~~bash
$ export SSL_CERT_FILE=/path/to/file.crt
~~~

This `.crt` file can be stored in the `.ignore/` folder if necessary.

## Contributors

Update the CITATION.cff file to enable appropriate citations.

The logo for this repository (logo.png) was generated using ChatGPI on July 25, 2025 with the prompt "Create a logo that represents automatic machine learning"






How To Use
---

<img src="logo.png" align="right" width=200 />

First clone and open in VSCode, then "Reopen in Container" to install devcontainer.

To launch Jupyter notebook server:
~~~bash
$ bash .devcontainer/start_jupyter.sh # at 127.0.0.1:1234
~~~

To launch Jupyter MLFlow server:
~~~bash
$ bash .devcontainer/start_mlflow.sh # at 127.0.0.1:4342
~~~


Citation
---
The logo for this repository (logo.png) was generated using Google Gemini 2.0 Flash (Imagen 3) on Mar. 26, 2025 with the prompt "Create a logo of outline of a brain with one half including symbols reminiscent of science, for example an atom, beaker, pendulum, or satellite, and the other half a small fully connected neural network displaying the connected nodes."
