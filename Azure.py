import os
from multiprocessing.pool import ThreadPool
from azure.storage.blob import BlobServiceClient


local_blob_path = cmd_folder
my_connection_string = cnx
my_blob_container = container
nfiles = 10

def get_blob_service_client(my_connection_string):
    return BlobServiceClient.from_connection_string(my_connection_string)

def get_container(my_connection_string, my_blob_container):
    # Initialize the connection to Azure storage account
    blob_service_client =  BlobServiceClient.from_connection_string(my_connection_string)
    return blob_service_client.get_container_client(my_blob_container)

def list_files_container(my_container):
    my_blobs = my_container.list_blobs()

def download_all_blobs_in_container(my_container):
    # get a list of blobs
    my_blobs = my_container.list_blobs()
    result = run(my_blobs)
    print(result)

def run(blobs):
    # Download several files at a time!
    with ThreadPool(processes=int(nfiles)) as pool:
        return pool.map(save_blob_locally, blobs)

def save_blob_locally(blob, my_container):
    file_name = blob.name
    print(file_name)
    bytes = my_container.get_blob_client(blob).download_blob().readall()

    # Get full path to the file
    download_file_path = os.path.join(local_blob_path, file_name)
    # for nested blobs, create local path as well!
    os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

    with open(download_file_path, "wb") as file:
        file.write(bytes)
    return file_name
    
def create_container(blob_service_client, new_container=None):
    if new_container is not None:
        my_container = blob_service_client.create_container(new_container)

def delete_container(blob_service_client, del_container=None):
    if del_container is not None:
        my_container = blob_service_client.get_container_client(del_container)
        my_container.delete_container()

def list_container(blob_service_client, Show = True):
    my_containers = blob_service_client.list_containers() 
    
    if Show:
        print('List of container:')
        for container in my_containers: 
            print (" {}".format(container.name))
    
def list_files_container(blob_service_client, container=None,Show = True):
    my_container = blob_service_client.get_container_client(container)
    my_blobs = my_container.list_blobs() 
    
    if Show:
        print('List of blobs in {}:'.format(container))
        for blob in my_blobs: 
            print (" {}".format(blob.name))
    
def upload_file(blob_service_client, container,path_data,file_name,tipo):
    file_name = str(os.path.splitext(os.path.basename(file_name))[0]) + '.' + tipo
    blob_client = blob_service_client.get_blob_client(container=container, blob=file_name)
    
    upload_file_path = os.path.join(path_data, file_name)
    
    print('Uploading file - {}'.format(file_name))
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data,overwrite=True)
        