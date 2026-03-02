resource "aws_redshift_cluster" "analytics" {
  cluster_identifier = "cloudstream-analytics"
  database_name      = "analytics"
  master_username    = "admin"
  master_password    = "examplepassword"

  node_type = "dc2.large"
  cluster_type = "single-node"
}