import boto3
import os
from datetime import datetime


def upload_file_to_s3(bucket_name: str, file_path: str, s3_prefix: str = "raw/") -> None:
    """
    Uploads a local file to an S3 bucket.

    Parameters
    ----------
    bucket_name : str
        Name of the target S3 bucket.
    file_path : str
        Local path to the file.
    s3_prefix : str
        S3 folder prefix (default: raw/).

    Raises
    ------
    Exception
        If upload fails.
    """

    s3_client = boto3.client("s3")

    file_name = os.path.basename(file_path)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    s3_key = f"{s3_prefix}{timestamp}_{file_name}"

    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"✅ Upload successful: s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print("❌ Upload failed.")
        raise e


if __name__ == "__main__":
    BUCKET_NAME = "cloudstream-insights-396421249599"
    FILE_PATH = "data/sample_event.json"

    upload_file_to_s3(BUCKET_NAME, FILE_PATH)