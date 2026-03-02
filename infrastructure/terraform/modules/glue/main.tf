resource "aws_glue_catalog_database" "analytics" {
  name = "cloudstream_insights_db"
}

resource "aws_glue_job" "batch_etl" {
  name     = "cloudstream-batch-etl"
  role_arn = aws_iam_role.glue_role.arn

  command {
    name            = "glueetl"
    script_location = "s3://cloudstream-insights-scripts/batch_etl.py"
  }

  max_retries = 1
  glue_version = "4.0"
}