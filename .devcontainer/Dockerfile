FROM mcr.microsoft.com/devcontainers/python:3.12

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano curl \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}"

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
