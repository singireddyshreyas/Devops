variable "aws_region" {
  type        = string
  description = "AWS region where the S3 bucket will be created."
  default     = "ap-south-1"
}
variable "bucket_prefix" {
  type        = string
  description = "Prefix used to create a globally unique S3 bucket name."
  default     = "devops-session18-"
}
