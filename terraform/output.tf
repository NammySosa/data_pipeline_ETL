# output file stores structured infrastructure data 

output "redshift_cluster_hostname" {
  description = "Redshift Cluster Name"
  value       = replace(
      aws_redshift_cluster.redshift.endpoint,
      format(":%s", aws_redshift_cluster.redshift.port),"",
  )
}

output "redshift_port" {
    description = "Redshift Cluster Port Number"
    value = aws_redshift_cluster.redshift.port
}

output "redshift_password" {
    description = "Redshift Password"
    value = var.rs_password
}

output "redshift_username" {
    description = "Redshift Username"
    value = aws_redshift_cluster.redshift.master_username
}

output "redshift_role" {
    description = "Redshift IAM Role"
    value = aws_iam_role.redshift_role.name
}

data "aws_caller_identity" "current" {}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "aws_region" {
    description = "AWS"
    value = var.aws_region
}

output "s3_bucket_name" {
    description = "Region set for AWS"
    value = var.s3_bucket
}
