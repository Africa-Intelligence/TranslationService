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
WORKDIR /app

# Copy relevant files
COPY pyproject.toml poetry.lock ./
# Copy the main file separately to create a distinct cache layer
COPY src/main.py src/
COPY src ./src

# Fix permissions for the app directory
RUN chmod -R 755 /app

# Install any needed packages using poetry
RUN poetry install

# Run the application
CMD ["poetry", "run", "src/main.py"]
