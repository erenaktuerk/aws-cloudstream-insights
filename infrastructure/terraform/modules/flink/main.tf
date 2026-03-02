resource "aws_kinesisanalyticsv2_application" "flink_app" {
  name                   = "cloudstream-flink-app"
  runtime_environment    = "FLINK-1_15"
  service_execution_role = aws_iam_role.flink_role.arn

  application_configuration {
    application_code_configuration {
      code_content {
        s3_content_location {
          bucket_arn = "arn:aws:s3:::cloudstream-insights-flink"
          file_key   = "streaming_job.jar"
        }
      }
      code_content_type = "ZIPFILE"
    }
  }
}