import os
import pathlib

def create_minio_service():
    contents = f"""
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: recsys-minio
  generation: 1
  annotations:
    run.googleapis.com/client-name: gcloud
    run.googleapis.com/ingress: all
    run.googleapis.com/ingress-status: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: '0'
        autoscaling.knative.dev/maxScale: '1'
    spec:
      containers:
        - image: gcr.io/{os.environ['GCP_PROJECT']}/recsys-s3:latest
          env:
            - name: MINIO_ROOT_USER
              value: {os.environ['MINIO_ACCESS_KEY']}
            - name: MINIO_ROOT_PASSWORD
              value: {os.environ['MINIO_SECRET_KEY']}
            - name: RUNTIME
              value: prod
          ports:
            - containerPort: 9000
          resources:
            limits:
              memory: 512Mi
              cpu: 1000m
  traffic:
    - percent: 100
      latestRevision: true
    """
    save_path = pathlib.Path(__file__) / '../../ci/minio_service.yaml'
    with open(save_path, 'w') as file:
        file.write(contents)

def create_flask_service():
    contents = f"""
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: recsys-api
  generation: 1
  annotations:
    run.googleapis.com/client-name: gcloud
    run.googleapis.com/ingress: all
    run.googleapis.com/ingress-status: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: '0'
        autoscaling.knative.dev/maxScale: '1'
    spec:
      containers:
        - image: gcr.io/{os.environ['GCP_PROJECT']}/recsys-api:latest
          env:
            - name: MINIO_ENDPOINT
              value: {os.environ['MINIO_ENDPOINT']}
            - name: CLIENT_ENDPOINT
              value: {os.environ['CLIENT_ENDPOINT']}
            - name: MINIO_ACCESS_KEY
              value: {os.environ['MINIO_ACCESS_KEY']}
            - name: MINIO_SECRET_KEY
              value: {os.environ['MINIO_SECRET_KEY']}
            - name: RUNTIME
              value: {os.environ['RUNTIME']}
          ports:
            - name: http1
              containerPort: 8080
          resources:
            limits:
              memory: 1024Mi
              cpu: 1000m
  traffic:
    - percent: 100
      latestRevision: true 
    """
    save_path = pathlib.Path(__file__) / '../../ci/api_service.yaml'
    with open(save_path, 'w') as file:
        file.write(contents)

def create_svelte_service():
    contents = f"""
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: recsys-client
  generation: 1
  annotations:
    run.googleapis.com/client-name: gcloud
    run.googleapis.com/ingress: all
    run.googleapis.com/ingress-status: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: '0'
        autoscaling.knative.dev/maxScale: '1'
    spec:
      containers:
        - image: gcr.io/{os.environ['GCP_PROJECT']}/recsys-client:latest
          env:
            - name: PUBLIC_API_ENDPOINT
              value: {os.environ['PUBLIC_API_ENDPOINT']}
          ports:
            - name: http1
              containerPort: 8080
          resources:
            limits:
              memory: 1024Mi
              cpu: 1000m
  traffic:
    - percent: 100
      latestRevision: true 
    """
    save_path = pathlib.Path(__file__) / '../../ci/client_service.yaml'
    with open(save_path, 'w') as file:
        file.write(contents)

if __name__ == "__main__":
    create_minio_service()
    create_flask_service()
    create_svelte_service()
