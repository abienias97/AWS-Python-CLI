# AWS Python CLI

This program is a CLI that lets you interact with some features of AWS S3.

## Requirements:

Before you begin you have to install Python 3 and all the needed libraries. Also remember to set your .env file.

To install python dependecies, run:
`pip install boto3 python-dotenv argparse`

`.env` file structure:
```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=your_region
S3_BUCKET_NAME=bucket_name
S3_PREFIX=prefix
```

## Features with examples:

- List files in bucket  
`python s3_cli.py list`
- List files matching REGEX in bucket  
`python s3_cli.py list-regex --pattern ".*.txt"`
- Upload file to specific location in bucket  
`python s3_cli.py upload --file test.txt --destination test/test.txt`
- Delete files matching REGEX in bucket  
`python s3_cli.py delete-regex --pattern ".*.log"`
