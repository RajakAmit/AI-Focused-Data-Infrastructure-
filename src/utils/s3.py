
import os

import boto3
from botocore.exceptions import ClientError


def get_minio_client():
    endpoint = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    # Ensure endpoint_url includes scheme (http:// or https://)
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        endpoint = "http://" + endpoint

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=os.getenv("MINIO_ACCESS_KEY", "minio"),
        aws_secret_access_key=os.getenv("MINIO_SECRET_KEY", "minio123"),
        # Optional: region_name="us-east-1",  # if needed
    )


def put_object(bucket: str, key: str, file_path: str):
    client = get_minio_client()

    try:
        # Try creating the bucket if it doesn't exist
        client.create_bucket(Bucket=bucket)
        print(f"✅ Bucket '{bucket}' created.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyOwnedByYou':
            # Bucket exists and owned by you - safe to proceed
            pass
        elif error_code == 'BucketAlreadyExists':
            # Bucket exists but owned by someone else - raise error
            raise Exception(f"Bucket '{bucket}' already exists and is owned by another user.")
        else:
            # Unexpected error - re-raise
            raise e

    try:
        client.upload_file(file_path, bucket, key)
        print(f"✅ Uploaded file '{file_path}' to bucket '{bucket}' with key '{key}'.")
    except ClientError as e:
        print(f"❌ Failed to upload file '{file_path}' to bucket '{bucket}'. Error: {e}")
        raise e
