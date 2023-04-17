variable "cluster_name" {
  description = "Redshift cluster name"
  type        = string
  default     = ""
}

variable "rs_password" {
  description = "Redshift master password"
  type        = string
  default     = ""
}

variable "s3_bucket" {
  description = "S3 bucket name"
  type        = string
  default     = ""
}

variable "aws_region" {
  description = "AWS Region name"
  type        = string
  default     = ""
}