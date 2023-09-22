# Cloud Storage subfolder example
This example shows how to setup an [Eventarc](https://cloud.google.com/eventarc) listener for a Google Cloud Storage bucket to trigger on object creation in a specific subfolder.

## Setup
### Local Environment settings
Change the BUCKET name and REGION as you need:
```
export PROJECT_ID="$(gcloud config get-value project)"
export PROJECT_NUMBER="$(gcloud projects describe $(gcloud config get-value project) --format='value(projectNumber)')"

export REGION='us-east1'
export SERVICE=eda1-$PROJECT_ID-service
export BUCKET=gs://eda1-$PROJECT_ID
export IN_FOLDER='eda1-inbound'
export OUT_FOLDER='eda1-outbound'
```

### Enable GCP APIs
```
gcloud services enable run.googleapis.com cloudbuild.googleapis.com iamcredentials.googleapis.com artifactregistry.googleapis.com

```

### Grant IAM Permissions
```
gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com --role roles/eventarc.eventReceiver

gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:service-$PROJECT_NUMBER@gs-project-accounts.iam.gserviceaccount.com --role roles/pubsub.publisher

gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com --role roles/iam.serviceAccountTokenCreator
```

### Deploy the code
This will scan the source code in the current directory, build it into a production-ready container image using [Cloud Build](https://cloud.google.com/build) & [Google Cloud's buildpacks](https://cloud.google.com/docs/buildpacks/overview), store the resulting image in the [Artifact Registry](https://cloud.google.com/artifact-registry) and lastly deploy it to [Cloud Run](https://cloud.google.com/run)
```
gcloud run deploy $SERVICE --source .
```

### Setup the GCS Bucket and folders
```
gsutil mb -l $REGION $BUCKET
gsutil mb -l $REGION $BUCKET/${OUT_FOLDER}
gsutil mb -l $REGION $BUCKET/${IN_FOLDER}
```

### Create an Eventarc trigger
```
gcloud eventarc triggers create dt-table-uptd-trigger \
 --location=$REGION--destination-run-service=dt-table-uptd-service \
 --destination-run-region=$REGION \
 --event-filters="type=google.cloud.audit.log.v1.written" \
 --event-filters="serviceName=storage.googleapis.com" \
 --event-filters="methodName=storage.objects.create" \
 --event-filters-path-pattern="resourceName=/projects/_/buckets/$BUCKET/objects/$IN_FOLDER/*" \
 --service-account=$PROJECT_NUMBER-compute@developer.gserviceaccount.com
```

### Test the trigger
```
touch eda1-test
gsutil cp ~/eda1-test $BUCKET/$IN_FOLDER/eda1-test
gcloud alpha run services logs read $SERVICE \
--region $REGION --limit=100 --format "value(log)"
```
