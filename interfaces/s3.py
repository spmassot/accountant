import boto3
import pickle


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


def load(thing):
    client().upload_fileobj(pickle.dumps(thing))
