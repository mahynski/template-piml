How To Use
---

<img src="logo.png" align="right" width=200 />

### Clone repo

1. Set up ssh-keys (instructions below) on the machine you are working on.
 
2. Select a location on your local machine and name (here, "my-new-project") for your new project.

~~~bash
$ git clone git@gitlab.altamiracorp.com:nathan.mahynski/ml-project-template.git ./path/to/my-new-project
$ cd ./path/to/my-new-project
~~~

3. Update the git url to create a new repository.

~~~bash
$ git remote -v # Check the url is still pointing to git@gitlab.altamiracorp.com:nathan.mahynski/project-template.git
$ git remote set-url origin git@gitlab.altamiracorp.com:user.name/my-new-project.git # Update user.name to your username
$ git remote -v # Check the new url is set correctly
~~~

4. Now push to create the "my-new-project" repo on your account.  Make sure you have an ssh-key set with the correct authority or this will not work.

~~~bash
$ git push -u origin main 
~~~

5. If using VSCode, do NOT "Open in Container" yet - first update the settings as described below, then "Re-open in container".

### Update Settings

1. Insert a project description here.
2. Create a [conda](https://www.anaconda.com/) environment for this project.  First modify `conda-env.yml` to include the relevant repositories and dependencies needed; also give the environment a good name (e.g., similar or same as this repo) - the default is "project-env". Then create the environment (see below).
3. If you do not want to work in a development container, skip to "Local Installation" to use a conda environment on your local (non virtual) machine.
4. Otherwise, a Docker [dev container](https://code.visualstudio.com/docs/devcontainers/containers) template for [VS Code](https://code.visualstudio.com/) is provided in the `.devcontainer/` folder.  This creates a [miniconda](https://docs.anaconda.com/miniconda/) container and installs the environment specified in `conda-env.yml` into the default IPython kernel in the container. To use:
   * Change the `UID` and `GID` in `.devcontainer/Dockerfile` if needed.
   * Optional: If you want to connect to other containers, e.g., running ollama for code assitance in [Continue](https://docs.continue.dev/), you might need to consider [Docker networking](https://docs.docker.com/engine/network/tutorials/standalone/). You can skip this in which case ollama will bind to your localhost at your chosen port on the default "bridge" network, which is acceptable on personal devices.
   * Add [additional arguments](https://containers.dev/implementors/json_reference/) as needed, e.g., "runArgs": ["--gpus", "all"] to [access host gpus](https://stackoverflow.com/questions/25185405/using-gpu-from-a-docker-container). This is helpful if you are doing deep learning in the container/project. You may have to install the appropriate drivers first.
      * Note that the `devcontainer.json` file already contains settings to detect and "forward" GPUs from your local machine, if available.
   * Change the name of the conda environment (default="project-env") in the `conda-env.yml` and files in .devcontainer/.
   * Install the "Dev Containers" Extension in VS Code.
   * First `git clone` this repo, then [open the folder in the container](https://code.visualstudio.com/docs/devcontainers/containers#_quick-start-open-an-existing-folder-in-a-container) by selecting "Dev Containers: Open Folder in Container" from the Command Palette.
   * From a terminal in VS Code, (1) navigate to your desired starting point (`data/analysis` is recommended), then (2) run `$ bash /path/to/.devcontainer/start_jupyter.sh` to launch a Jupyter server (forwarded on port 1234 by default) from the head of the repo.  The default kernel contains the `conda-env.yml` packages but is not renamed.
      * Note that this installs the `project-env` jupyter kernel automatically.
      
### Setup SSH Keys

If you are using this inside a devcontainer you will need to add an ssh key to push changes back to your GitLab account.

~~~bash
$ ssh-keygen -t ed25519 # Create a key - press enter each time you are prompted
$ cat ~/.ssh/id_ed25519.pub # Copy the contents of this file 
~~~

Go to `User settings > SSH Keys` on your GitLab account. Click `Add new key` and copy the contents above into the `Key` area.  Give it a title and expiration date, then click `Add key`.

Local Installation
---
You can easily set up the conda environment for this project on your local (non virtual) machine if you do not want to use a devcontainer. You will need to install the environment in your Jupyter kernel to use it (third command below); this is handled automatically in the devcontainer approach. Change the name of the conda environment (default="project-env") in the `conda-env.yml` if you wish.

~~~bash
$ conda env create -f conda-env.yml
$ conda activate project-env
$ python -m ipykernel install --user --name=project-env
~~~

Maintaining Provenance
---

At the end of a project it is good practice to export the entire conda environment for posterity, especially if not working in a development container.

~~~bash
$ conda env export > environment.yml
~~~

This environment can be recreated later; the `conda-env.yml` file can also be exchanged for this, but I prefer to keep both as a record.

~~~bash
$ conda env create -f environment.yml
~~~

This works for many cases, but if you need an *exactly reproducible* environment use [conda-lock](https://github.com/conda/conda-lock) instead.

Citation
---

The logo for this repository (logo.png) was generated using Google Gemini 2.0 Flash (Imagen 3) on Mar. 26, 2025 with the prompt "Create a logo of outline of a brain with one half including symbols reminiscent of science, for example an atom, beaker, pendulum, or satellite, and the other half a small fully connected neural network displaying the connected nodes."