import boto3
import os
from dotenv import load_dotenv

load_dotenv()
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET = os.getenv("S3_BUCKET")

def upload_file(file_path: str, key: str):
    s3.upload_file(file_path, BUCKET, key)

def download_file(key: str, file_path: str):
    s3.download_file(BUCKET, key, file_path)
