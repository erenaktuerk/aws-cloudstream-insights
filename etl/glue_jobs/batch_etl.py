import boto3
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import logging
from io import BytesIO
from datetime import datetime
import json
import time
from botocore.exceptions import ClientError

# --------------------------
# Logging configuration
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --------------------------
# S3 Configuration
# --------------------------
RAW_BUCKET = "cloudstream-insights-396421249599"
CURATED_BUCKET = "cloudstream-insights-396421249599"

RAW_PREFIX = "raw/"
CURATED_PREFIX = "curated/"

# Retry settings for S3 operations
S3_MAX_RETRIES = 3
S3_RETRY_DELAY = 2  # seconds

# --------------------------
# S3 Client
# --------------------------
s3_client = boto3.client("s3")

# --------------------------
# Helper functions
# --------------------------
def list_s3_files(bucket: str, prefix: str) -> list[str]:
    """
    List all files under a specific S3 prefix.
    Returns a list of keys.
    """
    logging.info(f"Listing files in s3://{bucket}/{prefix}")
    keys = []
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.append(obj["Key"])
    logging.info(f"Found {len(keys)} files")
    return keys

def read_json_from_s3(bucket: str, key: str) -> pd.DataFrame:
    """
    Robust S3 JSON reader.
    Supports:
      - JSON Lines
      - Standard JSON arrays ([{}, {}, ...])
      - Single JSON objects ({...})
      - Lists of scalars ([1,2,3])
    Includes retry logic for transient S3 errors.
    """
    logging.info(f"Reading raw data from s3://{bucket}/{key}")
    
    for attempt in range(1, S3_MAX_RETRIES + 1):
        try:
            obj = s3_client.get_object(Bucket=bucket, Key=key)
            content = obj["Body"].read().decode("utf-8").strip()
            break
        except ClientError as e:
            logging.warning(f"S3 read attempt {attempt} failed for {key}: {e}")
            if attempt == S3_MAX_RETRIES:
                logging.error(f"Max retries reached for {key}. Skipping file.")
                return pd.DataFrame()
            time.sleep(S3_RETRY_DELAY)
    
    if not content:
        logging.warning(f"{key} is empty. Skipping file.")
        return pd.DataFrame()

    # Attempt JSON Lines first
    try:
        df = pd.read_json(BytesIO(content.encode()), lines=True)
    except ValueError:
        logging.warning(f"{key} is not JSON Lines. Trying standard JSON format.")
        try:
            df = pd.read_json(BytesIO(content.encode()))
        except ValueError:
            # Handle arrays of scalars or single objects
            try:
                parsed = json.loads(content)
                if isinstance(parsed, list):
                    if all(isinstance(x, dict) for x in parsed):
                        df = pd.DataFrame(parsed)
                    else:
                        df = pd.DataFrame({"value": parsed})
                elif isinstance(parsed, dict):
                    df = pd.DataFrame([parsed])
                else:
                    logging.error(f"Unsupported JSON format in {key}: {parsed}")
                    return pd.DataFrame()
            except Exception as e:
                logging.error(f"Failed to parse {key}: {e}")
                return pd.DataFrame()

    logging.info(f"Read {len(df)} rows from {key}")
    return df

def write_parquet_to_s3(df: pd.DataFrame, bucket: str, key: str):
    """
    Write a DataFrame to S3 as a Parquet file.
    Skips writing if DataFrame is empty.
    """
    if df.empty:
        logging.warning("DataFrame empty. Skipping Parquet write.")
        return

    logging.info(f"Writing curated data to s3://{bucket}/{key}")
    buffer = BytesIO()
    table = pa.Table.from_pandas(df)
    pq.write_table(table, buffer)
    buffer.seek(0)
    s3_client.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())
    logging.info("Write successful")

def perform_data_quality_checks(df: pd.DataFrame):
    """
    Enhanced data quality checks for production readiness.
    Checks include:
      - Empty DataFrame
      - Missing values
      - Schema enforcement (user_id=int, event=str)
    """
    logging.info("Performing data quality checks")
    
    if df.empty:
        logging.warning("DataFrame is empty")

    # Missing values
    missing_values = df.isnull().sum().sum()
    if missing_values > 0:
        logging.warning(f"Data contains {missing_values} missing values")

    # Schema checks and coercion
    if "user_id" in df.columns:
        if not pd.api.types.is_integer_dtype(df["user_id"]):
            logging.warning("Column 'user_id' is not integer type, coercing to int")
            df["user_id"] = pd.to_numeric(df["user_id"], errors="coerce")
    if "event" in df.columns:
        if not pd.api.types.is_string_dtype(df["event"]):
            logging.warning("Column 'event' is not string type, casting to str")
            df["event"] = df["event"].astype(str)

    logging.info("Data quality checks completed")

# --------------------------
# Main ETL workflow
# --------------------------
def main():
    """
    Main ETL pipeline workflow:
      1. List all raw files in S3
      2. Read JSON
      3. Transform & normalize
      4. Run data quality checks
      5. Write partitioned Parquet to curated S3
    """
    raw_files = list_s3_files(RAW_BUCKET, RAW_PREFIX)
    if not raw_files:
        logging.warning("No files found in raw zone")
        return

    for raw_key in raw_files:
        if raw_key.endswith("/"):
            continue
        try:
            df = read_json_from_s3(RAW_BUCKET, raw_key)
            if df.empty:
                logging.warning(f"Skipping {raw_key} due to empty dataset")
                continue

            # --------------------------
            # Transformation
            # --------------------------
            logging.info("Starting transformation")
            df.columns = [col.lower().replace(" ", "_") for col in df.columns]
            df["processed_at"] = datetime.utcnow()
            logging.info("Transformation completed")

            # --------------------------
            # Data Quality
            # --------------------------
            perform_data_quality_checks(df)

            # --------------------------
            # Partitioned write
            # --------------------------
            date_str = datetime.utcnow().strftime("%Y/%m/%d")
            file_name = raw_key.split("/")[-1].replace(".json", ".parquet")
            curated_key = f"{CURATED_PREFIX}{date_str}/{file_name}"
            write_parquet_to_s3(df, CURATED_BUCKET, curated_key)

        except Exception as e:
            logging.error(f"Pipeline failed for {raw_key}: {e}")
            continue

if __name__ == "__main__":
    main()