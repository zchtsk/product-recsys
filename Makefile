REGION = us-central1

###### MINIO DEPLOYMENT
tag_s3:
	docker commit minio gcr.io/$(GCP_PROJECT)/recsys-s3:latest

push_s3:
	docker push gcr.io/$(GCP_PROJECT)/recsys-s3:latest

launch_s3: push_s3
	gcloud run services replace ci/minio_service.yaml --region=$(REGION)

public_s3: launch_s3
	gcloud run services set-iam-policy recsys-minio ci/policy.yaml --region=$(REGION) --quiet

deploy_s3: public_s3
	echo "Minio Deployed"

remove_s3:
	gcloud run services delete recsys-minio --region=$(REGION) --quiet

###### API DEPLOYMENT
tag_api:
	docker tag zachtsk/recsys-api gcr.io/$(GCP_PROJECT)/recsys-api:latest

push_api: tag_api
	docker push gcr.io/$(GCP_PROJECT)/recsys-api:latest

launch_api: push_api
	gcloud run services replace ci/api_service.yaml --region=$(REGION)

public_api: launch_api
	gcloud run services set-iam-policy recsys-api ci/policy.yaml --region=$(REGION) --quiet

deploy_api: public_api
	echo "API Deployed"

remove_api:
	gcloud run services delete recsys-api --region=$(REGION) --quiet

###### CLIENT
tag_client:
	docker tag zachtsk/recsys-client gcr.io/$(GCP_PROJECT)/recsys-client:latest

push_client: tag_client
	docker push gcr.io/$(GCP_PROJECT)/recsys-client:latest

launch_client: push_client
	gcloud run services replace ci/client_service.yaml --region=$(REGION)

public_client: launch_client
	gcloud run services set-iam-policy recsys-client ci/policy.yaml --region=$(REGION) --quiet

deploy_client: public_client
	echo "Client Deployed"

remove_client:
	gcloud run services delete recsys-client --region=$(REGION) --quiet

###### CLOUD RUN SERVICE FILE BUILDER
build_service:
	python -m scripts.build_service_yamls