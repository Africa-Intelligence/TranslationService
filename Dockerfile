# syntax=docker/dockerfile:1
FROM python:3.12-bullseye

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.7.1


# System deps:
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /src
COPY . .

# Fix permissions for the src directory
RUN chmod -R 755 /src

# Install any needed packages using poetry
RUN poetry install

# Run the application
CMD ["poetry", "run", "main.py"]
