variable "aws_region" {
  description = "AWS region for the Session 19 mini project."
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type for the HTTP demo."
  type        = string
  default     = "t3.micro"
}

variable "bucket_prefix" {
  description = "Prefix for the private, versioned S3 demo bucket."
  type        = string
  default     = "session19-lab-"
}
