import os
from flask import Flask, request, jsonify, send_file, abort
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

AZURE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# images will defaulf as the container name if AZURE_CONTAINER_NAME is not set
CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME', 'images')

# add the file types you want to allow
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize Azure Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

# Ensure container exists
try:
    container_client = blob_service_client.create_container(CONTAINER_NAME)
except Exception:
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Read file bytes
        data = file.read()
        try:
            # Upload to Azure Blob Storage
            blob_client = container_client.get_blob_client(filename)
            blob_client.upload_blob(data, overwrite=True)
            url = blob_client.url
            return jsonify({'message': 'Upload successful', 'url': url}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
