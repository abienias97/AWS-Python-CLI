import os
import re
import argparse
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS credentials and config
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION') # No region was specified?
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_PREFIX = os.getenv('S3_PREFIX')

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def list_files():
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=S3_PREFIX)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(obj['Key'])
        else:
            print("No files found.")
    except NoCredentialsError:
        print("Credentials not available.")

def list_files_matching_regex(pattern):
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=S3_PREFIX)
        if 'Contents' in response:
            regex = re.compile(pattern)
            for obj in response['Contents']:
                if regex.search(obj['Key']):
                    print(obj['Key'])
        else:
            print("No files found.")
    except NoCredentialsError:
        print("Credentials not available.")

list_files_matching_regex("READ*")
