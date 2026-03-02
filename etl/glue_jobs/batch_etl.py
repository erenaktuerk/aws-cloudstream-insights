import boto3
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import logging
from io import BytesIO
from datetime import datetime

# --------------------------
# Logging configuration
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --------------------------
# Configuration
# --------------------------
RAW_BUCKET = "cloudstream-insights-396421249599"
CURATED_BUCKET = "cloudstream-insights-396421249599"
RAW_PREFIX = "raw/"
CURATED_PREFIX = "curated/"

# --------------------------
# S3 Client
# --------------------------
s3_client = boto3.client("s3")

# --------------------------
# Helper functions
# --------------------------
def read_json_from_s3(bucket: str, key: str) -> pd.DataFrame:
    """
    Read a JSON file from S3 and return a Pandas DataFrame.
    """
    logging.info(f"Reading raw data from s3://{bucket}/{key}")
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    df = pd.read_json(obj['Body'], lines=True)
    logging.info(f"Read {len(df)} rows")
    return df

def write_parquet_to_s3(df: pd.DataFrame, bucket: str, key: str):
    """
    Write a Pandas DataFrame to S3 as a Parquet file.
    """
    logging.info(f"Writing curated data to s3://{bucket}/{key}")
    buffer = BytesIO()
    table = pa.Table.from_pandas(df)
    pq.write_table(table, buffer)
    buffer.seek(0)
    s3_client.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())
    logging.info("Write successful")

def perform_data_quality_checks(df: pd.DataFrame):
    """
    Perform simple data quality checks.
    """
    logging.info("Performing data quality checks")
    if df.empty:
        logging.warning("DataFrame is empty!")
    if df.isnull().sum().sum() > 0:
        logging.warning("Data contains missing values")
    logging.info("Data quality checks completed")

# --------------------------
# Main ETL workflow
# --------------------------
def main():
    """
    Main ETL workflow:
    1. Read raw data from S3
    2. Clean & transform
    3. Write curated data to S3
    """
    # Example: process a single file
    raw_key = RAW_PREFIX + "20260302_152758_sample_event.json"
    df = read_json_from_s3(RAW_BUCKET, raw_key)

    # --------------------------
    # Transformation example
    # --------------------------
    logging.info("Starting transformation")
    # Example: flatten nested JSON or rename columns
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    df['processed_at'] = datetime.utcnow()
    logging.info("Transformation completed")

    # --------------------------
    # Data quality
    # --------------------------
    perform_data_quality_checks(df)

    # --------------------------
    # Write curated data
    # --------------------------
    curated_key = CURATED_PREFIX + "20260302_152758_sample_event.parquet"
    write_parquet_to_s3(df, CURATED_BUCKET, curated_key)

if __name__ == "__main__":
    main()