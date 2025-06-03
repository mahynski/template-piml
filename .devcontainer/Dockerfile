FROM continuumio/miniconda3:latest
# RUN apt update -y

# Create a user with a given User and Group ID
# https://vsupalov.com/docker-shared-permissions/
ARG UID
ARG GID
RUN addgroup --gid $GID user
RUN adduser --disabled-password --gecos '' --uid $UID --gid $GID user

USER user
COPY conda-env.yml /

ENV PYTHONDONTWRITEBYTECODE=true

# Create conda env
RUN conda env create -f conda-env.yml

# Make RUN commands use bash not sh -necessary to make conda work
SHELL ["/bin/bash", "--login", "-c"]

# Initialize conda in bash config files (~/.bashrc) for all future RUNs
RUN conda init bash

# Install kernel 
RUN conda activate project-env \
 && python -m ipykernel install --user --name=project-env

# Install notebook outside of environments
# Run in base conda env so it knows about pip
RUN conda run pip install notebook python-dotenv mlflow
