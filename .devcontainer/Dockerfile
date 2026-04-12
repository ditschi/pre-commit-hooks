FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu

# Install packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y --allow-downgrades \
        python3.10 \
        python3.10-venv \
        python3.10-distutils \
        python3-pip \
    && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
    && \
    rm -rf /var/lib/apt/lists/*

# update and install python modules
RUN python -m pip install --upgrade pip \
    && \
    python -m pip install pipx \
    && \
    python -m pipx install uv \
    && \
    python -m pipx install "nox[pbs]" \
    && \
    python -m pipx install pip-tools

ENV PATH="/root/.local/bin:${PATH}"
