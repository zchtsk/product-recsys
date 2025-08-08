FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy Module
COPY prod2vec .

# Copy scripts for initialization
COPY scripts /app/scripts
COPY start_server.py /app/

# Create datalake directory and copy any existing data
RUN mkdir -p /datalake
COPY datalake /datalake

# Run the initialization script on container startup
ENV RUNTIME prod
CMD ["uv", "run", "python", "start_server.py"]