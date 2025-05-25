
# A plug-and-play boilerplate Flask application for securely uploading images (PNG, JPG, JPEG, GIF, ....) to Microsoft Azure Blob Storage. 

# How to run?

pip install -r requirements.txt

replace the .env values

python azureStorageTemplate.py


# How to request Blobs?
Storage Account > Data Storage > Containers > -The container you are working with-
Select Change Access level
Select Anonymous access level - Blob (anonymous read access for blobs only)
Select a block and use the URL 
eg. https://<ContainerName>.blob.core.windows.net/<ContainerName>/<BlobName> 
Using the link will download the blob to your device. 
You can display it in HTML with scr="-link-"

# How to get AZURE_STORAGE_CONNECTION_STRING and AZURE_CONTAINER_NAME?
Storage Account > Security + Networking > Access Keys 



