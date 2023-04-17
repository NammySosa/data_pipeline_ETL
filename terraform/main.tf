terraform {
    required_version = ">= 1.2.0"

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 4.16"
        }
    }
}

provider "aws" {
    region = var.aws_region
}

# Configure Redshift
# skip_final_snapshot = true allows resource to be destroyed via command: terraform destroy

resource "aws_redshift_cluster" "redshift" {
  cluster_identifier = var.cluster_name
  skip_final_snapshot = true 
  master_username    = "awsuser"
  master_password    = var.rs_password
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  publicly_accessible = "true"
  iam_roles = [aws_iam_role.redshift_read_s3.arn]
  vpc_security_group_ids = [aws_security_group.redshift_security.id]
  
}

# Redshift security configuration; allows incoming/outgoing traffic

 resource "aws_security_group" "redshift_security" {
  name        = "redshift_security"
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

# Give redshift read-only access to S3 bucket to ingest data

resource "aws_iam_role" "redshift_read_s3" {
  name = "RoleForS3ReadOnlyAccess"
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"]
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      },
    ]
  })
}

# force_destroy = true allows resource to be destroyed via command: terraform destroy

resource "aws_s3_bucket" "pipeline_storage" {
  bucket = var.s3_bucket
  force_destroy = true 
}

# Sets bucket to private

resource "aws_s3_bucket_acl" "storage_acl" {
  bucket = aws_s3_bucket.pipeline_storage.id
  acl    = "private"
}
      
