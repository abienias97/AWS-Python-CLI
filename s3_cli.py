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

def upload_file(file_path, destination_key):
    try:
        s3.upload_file(file_path, S3_BUCKET_NAME, destination_key)
        print(f"File {file_path} uploaded successfully to {destination_key}.")
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")

def delete_files_matching_regex(pattern):
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=S3_PREFIX)
        if 'Contents' in response:
            regex = re.compile(pattern)
            keys_to_delete = [{'Key': obj['Key']} for obj in response['Contents'] if regex.search(obj['Key'])]
            
            if keys_to_delete:
                s3.delete_objects(
                    Bucket=S3_BUCKET_NAME,
                    Delete={
                        'Objects': keys_to_delete,
                        'Quiet': True
                    }
                )
                print(f"Deleted {len(keys_to_delete)} files.")
            else:
                print("No files matched the pattern.")
        else:
            print("No files found.")
    except NoCredentialsError:
        print("Credentials not available.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S3 Bucket Operations")
    
    parser.add_argument("operation", choices=["list", "upload", "list-regex", "delete-regex"], help="Operation to perform")
    parser.add_argument("--file", type=str, help="Local file path to upload")
    parser.add_argument("--destination", type=str, help="S3 destination key (for upload)")
    parser.add_argument("--pattern", type=str, help="Regex pattern to filter files")

    args = parser.parse_args()

    if args.operation == "list":
        list_files()
    elif args.operation == "upload":
        if args.file and args.destination:
            upload_file(args.file, args.destination)
        else:
            print("Please provide both --file and --destination arguments for upload.")
    elif args.operation == "list-regex":
        if args.pattern:
            list_files_matching_regex(args.pattern)
        else:
            print("Please provide a --pattern argument for filtering.")
    elif args.operation == "delete-regex":
        if args.pattern:
            delete_files_matching_regex(args.pattern)
        else:
            print("Please provide a --pattern argument for deleting files.")