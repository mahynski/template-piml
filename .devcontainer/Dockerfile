FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

# Need git and build-essential (provides gcc compiler) for pre-commit
RUN apt update -y \
 && apt install git -y \
 && apt install build-essential -y

# Also add timezone support
RUN apt install tzdata -y \
 && ln -sf /usr/share/zoneinfo/$(cat /etc/timezone) /etc/localtime \
 && echo $(cat /etc/timezone) > /etc/timezone

ENV TZ=America/New_York

# Create a user with a given User and Group ID
# https://vsupalov.com/docker-shared-permissions/
ARG UID
ARG GID
RUN addgroup --gid $GID user
RUN adduser --disabled-password --gecos '' --uid $UID --gid $GID user

SHELL ["/bin/bash", "--login", "-c"]

USER user
