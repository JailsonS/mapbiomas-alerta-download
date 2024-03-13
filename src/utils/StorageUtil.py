from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials

import os, json


class StorageUtil:

    def __init__(self, pathCredential:str, projectId:str, bucket_name:str) -> None:
        self.pathCredential = pathCredential
        self.client = self._auth(pathCredential, projectId)
        self.bucket_name = bucket_name

    def _auth(self, dirServiceAccount, projectId) -> storage.Client:
        serviceAccount = json.load(open(dirServiceAccount))
        creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(serviceAccount))
        return storage.Client(credentials=creds, project=projectId)
    
    def getFile(self, dir):

        filename = dir.split('/')[-1]
        tempDir =  os.path.abspath('./data/' + filename)

        blob = self.client.get_bucket(bucket_name=self.bucket_name).get_blob(dir)

        blob.download_to_filename(tempDir)

        return tempDir

    def listBuckets(self):
        return self.client.list_buckets()
    
    def listObjects(self, bucket: str, prefix:str):
        return self.client.get_bucket(bucket).list_blobs(prefix=prefix)
    
    def uploadFile(self, bucket: str, sourceFileName: str, destinationBlobName, cog=False):
        try:
            if cog:
                cogDir = sourceFileName.replace('chip', 'cog')
                os.system("gdal_translate {} {} -of COG -co COMPRESS=LZW".format(sourceFileName, cogDir))
                sourceFileName = cogDir

            bucket = self.client.get_bucket(bucket)
            
            blob = bucket.blob(destinationBlobName)

            blob.upload_from_filename(sourceFileName)

            print(f"File {sourceFileName} uploaded to {destinationBlobName}.")

            if cog:
                os.remove(cogDir)
    
        except Exception as e:
            print(e)

    def move_blob(self, bucket_name, blob_name, destination_bucket_name, destination_blob_name):
        """Moves a blob from one bucket to another with a new name."""

        storage_client = self.client

        source_bucket = storage_client.bucket(bucket_name)
        source_blob = source_bucket.blob(blob_name)
        destination_bucket = storage_client.bucket(destination_bucket_name)

        blob_copy = source_bucket.copy_blob(
            source_blob, destination_bucket, destination_blob_name,
        )
        source_bucket.delete_blob(blob_name)

        print(
            "Blob {} in bucket {} moved to blob {} in bucket {}.".format(
                source_blob.name,
                source_bucket.name,
                blob_copy.name,
                destination_bucket.name,
            )
        )
