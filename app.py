from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask  import FlaskPlugin
from flask import Flask, jsonify
from azure.identity import EnvironmentCredential 
from azure.storage.blob import BlobServiceClient
import json, os, time


app = Flask(__name__)

with open("/etc/app.conf", "r") as config:
    data = json.load(config)
    container_name = data["storage_config"]["container_name"]
    storage_account_url = data["storage_config"]["storage_account_url"]


@app.route('/')
def nothing_here():
    return "Nothing to see here. But it shows it works"


spec = APISpec(
    title='A simple app',
    version='3.0.1',
    openapi_version='3.0.0',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

@app.route('/api/swager.json')
def swager_spec():
    return jsonify(spec.to_dict())


az_creds = EnvironmentCredential()
client   = BlobServiceClient(account_url=storage_account_url, credential=az_creds)

def get_blob_list():
    list_of_blobs = []
    blobs = client.get_container_client(container_name).list_blobs()
    for b in blobs:
        list_of_blobs.append(b.name)
    return list_of_blobs


@app.route('/files')
def get_files():
    """Get list of objects
        ---
        get:
            description: Fetch list of items in from object storage
            response:
                200:
                    description: A list of items from the object bucket
                    content:
                        application/json:
                            schema:
                            type: array
                            items:
                            properties:
                              fileName:
                              type: string
                500:
                    description: Unable to fetch file list from container

    """

    return get_blob_list()


if __name__ == '__main__':
    app.run(debug=True)
