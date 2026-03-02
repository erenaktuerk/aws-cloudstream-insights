provider "aws" {
  region = var.aws_region
}

module "s3" {
  source = "./modules/s3"
}

module "iam" {
  source = "./modules/iam"
}

module "glue" {
  source = "./modules/glue"
}

module "kinesis" {
  source = "./modules/kinesis"
}

module "flink" {
  source = "./modules/flink"
}

module "redshift" {
  source = "./modules/redshift"
}