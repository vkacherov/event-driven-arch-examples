import functions_framework
from google.cloud import storage
from flask import Flask

app = Flask(__name__)

@app.route("/")
# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def main(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucketName = data["bucket"]
    fileName = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucketName}")
    print(f"File: {fileName}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    # Create a Cloud Storage client
    #storage_client = storage.Client()

    # Get the bucket and object
    #bucket = storage_client.bucket(bucketName)
    #obj = bucket.blob(fileName)

    # Read the file contents
    #file_contents = obj.read()

    # Print the file contents
    #print(file_contents)
    if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
