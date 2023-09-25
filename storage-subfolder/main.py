import os

from flask import Flask, request

from google.events.cloud import storage

app = Flask(__name__)

# Triggered by a change in a storage bucket
@app.route("/", methods=["POST"])
def index():
    print(request.json)
    data = request.json

    methodName = data["protoPayload"]["methodName"]
    insertId = data["insertId"]
    bucketName = data["resource"]["labels"]["bucket_name"]
    fileName = data["protoPayload"]["resourceName"]
    requestMetadata = data["protoPayload"]["requestMetadata"]
    timeCreated = data["protoPayload"]["requestMetadata"]["requestAttributes"]["time"]

    print(f"Event ID: {insertId}")
    print(f"Event type: {methodName}")
    print(f"Bucket: {bucketName}")
    print(f"File: {fileName}")
    print(f"requestMetadata: {requestMetadata}")
    print(f"Created: {timeCreated}")

    return(f"Finished reading file!", 200)

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
