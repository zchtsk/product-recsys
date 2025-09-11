FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
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

# Copy Artifacts
RUN mkdir -p /datalake
COPY datalake /datalake

# Run the web service on container startup
ENV RUNTIME prod
CMD exec uv run gunicorn --bind :$PORT --workers 1 --threads 2 --timeout 0 api:app