import boto3

# S3 Client
s3 = boto3.client("s3")

# Liste aller Buckets ausgeben
response = s3.list_buckets()
print("Buckets in deinem Konto:")
for bucket in response['Buckets']:
    print("-", bucket['Name'])

# Test: Inhalte eines bestimmten Buckets auflisten
bucket_name = "cloudstream-insights-erenaktuerk"
prefix = "raw/"

response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
if "Contents" in response:
    print(f"\nDateien in {bucket_name}/{prefix}:")
    for obj in response['Contents']:
        print("-", obj['Key'])
else:
    print(f"\nKeine Dateien gefunden in {bucket_name}/{prefix}")