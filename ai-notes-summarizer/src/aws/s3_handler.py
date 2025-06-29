import boto3
import os
from dotenv import load_dotenv

load_dotenv()
#Connect to AWS S3 Bucket
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET = os.getenv("S3_BUCKET")

#Upload resume to S3 bucket
def upload_fileobj(fileobj, key: str):
    s3.upload_fileobj(fileobj, BUCKET, key)

#Download resume from S3 bucket
def download_file(key: str, file_path: str):
    s3.download_file(BUCKET, key, file_path)

#Check if a file exists in the S3 bucket
def file_exists(key: str) -> bool:
    try:
        s3.head_object(Bucket=BUCKET, Key=key)
        return True
    except s3.exceptions.ClientError:
        return False
    
def delete_file(key: str):
    try:
        s3.delete_object(Bucket=BUCKET, Key=key)
    except s3.exceptions.ClientError as e:
        print(f"Error deleting file {key}: {e}")
        raise e