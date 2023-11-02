FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu

# Install packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y --allow-downgrades \
        python3 \
        python3-pip \
    && \
    rm -rf /var/lib/apt/lists/*

# update and install python modules
RUN python3 -m pip install --upgrade pip \
    && \
    python3 -m pip install pipenv tox
