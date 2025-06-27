# filepath: ai-notes-summarizer/src/aws/s3_utils.py

"""
This module contains utility functions for interacting with AWS S3.
These functions can be used to upload and download files, which is essential
for storing job descriptions and resumes in the context of the AI notes summarizer application.
"""

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket.

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except ClientError as e:
        print(f"Failed to upload {file_name} to {bucket}/{object_name}: {e}")
        return False
    return True

def download_file_from_s3(bucket, object_name, file_name):
    """Download a file from an S3 bucket.

    :param bucket: Bucket to download from
    :param object_name: S3 object name
    :param file_name: File to download to
    :return: True if file was downloaded, else False
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except ClientError as e:
        print(f"Failed to download {object_name} from {bucket}: {e}")
        return False
    return True