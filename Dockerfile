# Use the official Python image with version 3.12
FROM python:3.12.2

# Install Poetry
# Not recommended but works sufficiently fine
RUN pip install poetry

# Numerical planner enhsp is java based
RUN apt update && apt -y install openjdk-17-jdk

RUN mkdir -p /app/clab_prototype/
# Set the working directory
WORKDIR /app

# Copy the local folder 'clab_protoype' to the container
COPY clab_prototype /app/clab_prototype
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock
COPY README.md /app/README.md

# Some packages are installed directly from GitHub
RUN mkdir -p /root/.ssh && \
    touch /root/.ssh/known_hosts && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts
RUN poetry install --all-extras

# Set the default command to start your application
CMD ["poetry"]