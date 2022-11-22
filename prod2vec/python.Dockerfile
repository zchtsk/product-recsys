FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install core requirements
COPY prod2vec/requirements.txt .
RUN pip install -r requirements.txt

# Copy Module
COPY prod2vec .

# Copy Artifacts
RUN mkdir -p /datalake
COPY datalake /datalake

# Run the web service on container startup
ENV RUNTIME prod
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 api:app