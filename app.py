from flask import Flask
from azure.identity import EnvironmentCredential 
from azure.storage.blob import BlobServiceClient
import json, os, time
from flasgger import Swagger 

app = Flask(__name__)

# Reading the configuration
with open("/etc/app.conf", "r") as config:
    data = json.load(config)
    container_name = data["storage_config"]["container_name"]
    storage_account_url = data["storage_config"]["storage_account_url"]

# Swagger init
template = {"info": {"description": "API <style>.models {display: none !important}</style>"}}
swagger = Swagger(app, template=template)

# Logging in via a service principal
az_creds = EnvironmentCredential()
client   = BlobServiceClient(account_url=storage_account_url, credential=az_creds)

# Function to read the names of the files inside the container
def get_blob_list():
    list_of_blobs = []
    blobs = client.get_container_client(container_name).list_blobs()
    for b in blobs:
        list_of_blobs.append(b.name)
    return list_of_blobs

# Root path of the app
@app.route('/')
def nothing_here():
    return "Nothing to see here. But it shows it works"

# API endpoint
@app.route('/files')
def get_files():

    """Endpoint returning a list of files stored in an Azure container.
    Returns a json array of strings.
    ---
    definitions:
      Files:
        type: array
        properties:
          file_name:
            type: string
    responses:
      200:
        description: A list of files stored in an Azure container 
      500:
        description: Unable to fetch file list from container
"""

    return get_blob_list()


if __name__ == '__main__':
    app.run()
