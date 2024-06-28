# syntax=docker/dockerfile:1
FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-devel

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
  POETRY_HOME='/opt/poetry' \
  POETRY_VERSION=1.7.1 \
  PATH="/opt/poetry/bin:$PATH"

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry --version

# Set the working directory in the container
WORKDIR /app

# Copy relevant files
COPY . ./

# Fix permissions for the app directory
RUN chmod -R 755 /app

# Install any needed packages using poetry
RUN poetry install

# Run the application
CMD ["poetry", "run", "python", "src/main.py"]
