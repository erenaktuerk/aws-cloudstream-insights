resource "aws_s3_bucket" "raw" {
  bucket = "cloudstream-insights-raw"
}

resource "aws_s3_bucket" "curated" {
  bucket = "cloudstream-insights-curated"
}

resource "aws_s3_bucket" "analytics" {
  bucket = "cloudstream-insights-analytics"
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.raw.id

  versioning_configuration {
    status = "Enabled"
  }
}