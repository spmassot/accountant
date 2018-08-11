import boto3
import pickle
from os import getenv


def client():
    return boto3.client('s3')


def all_buckets():
    return [b['Name'] for b in client().list_buckets()['Buckets']]


def initialize_bucket(bucket_to_initialize):
    if bucket_to_initialize not in all_buckets():
        client().create_bucket(
            ACL='private',
            CreateBucketConfiguration={
                'LocationConstraint': 'us-east-1'
            }
        )


def upload(thing):
    return client().upload_fileobj(pickle.dumps(thing))


def create_folder(folder_name):
    client().put_object(
        Bucket=getenv('FILE_BUCKET'),
        Body='',
        Key=folder_name+'/'
    )


def put_file_in_folder(file_name, file_data, folder_name):
    client().put_object(
        Bucket=getenv('FILE_BUCKET'),
        Body=file_data,
        Key=folder_name+'/'+file_name
    )


def list_objects():
    response = client().list_objects(Bucket=getenv('FILE_BUCKET')).get('Contents')
    if response:
        return [x['Key']  for x in response]
    else:
        return []
