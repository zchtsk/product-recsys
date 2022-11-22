FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install core requirements
COPY prod2vec .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "uvicorn[standard]"

# Run the web service on container startup
ENV RUNTIME prod
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 api:app