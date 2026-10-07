# Terraform S3 Bucket Demo

## Project Structure

```text
terraform-s3-demo/
|
|-- README.md
|-- terraform.tf
|-- providers.tf
|-- variables.tf
|-- main.tf
|-- outputs.tf
|-- .gitignore
```

## Architecture

```text
terraform.tf
     |
     v
Provider Configuration
     |
     v
variables.tf
     |
     v
main.tf
     |
     v
aws_s3_bucket.demo
     |
     v
AWS S3 Bucket
     |
     +-- Public access blocked
     +-- Server-side encryption enabled
     +-- Versioning enabled
     |
     v
outputs.tf
```

## Prerequisites

Install:

* Terraform
* AWS CLI

Configure AWS:

```bash
aws configure
```

Verify:

```bash
aws sts get-caller-identity
```

## Terraform Workflow

### 1. Initialize

```bash
terraform init
```

Expected:

```text
Initializing the provider plugins...
Terraform has been successfully initialized!
```

### 2. Format

```bash
terraform fmt
```

### 3. Validate

```bash
terraform validate
```

Expected:

```text
Success! The configuration is valid.
```

### 4. Plan

```bash
terraform plan
```

Expected:

```text
Plan: 4 to add, 0 to change, 0 to destroy.
```

### 5. Apply

```bash
terraform apply
```

Terraform asks:

```text
Do you want to perform these actions?
  Only 'yes' will be accepted to approve.
Enter a value:
```

Enter:

```text
yes
```

Expected:

```text
Apply complete! Resources: 4 added, 0 changed, 0 destroyed.
Outputs:
bucket_arn = "arn:aws:s3:::devops-session18-..."
bucket_name = "devops-session18-..."
bucket_region = "ap-south-1"
```

### 6. Check State

```bash
terraform state list
```

Expected:

```text
aws_s3_bucket.demo
aws_s3_bucket_public_access_block.demo
aws_s3_bucket_server_side_encryption_configuration.demo
aws_s3_bucket_versioning.demo
```

Inspect the resource:

```bash
terraform state show aws_s3_bucket.demo
```

### 7. Check Output

```bash
terraform output
```

Or:

```bash
terraform output bucket_name
```

Expected:

```text
"devops-session18-..."
```

### 8. Verify Using AWS CLI

```bash
aws s3 ls
```

Or:

```bash
aws s3api head-bucket --bucket "$(terraform output -raw bucket_name)"
```

### 9. Destroy

After completing the demo:

```bash
terraform plan -destroy
```

Then:

```bash
terraform destroy
```

Enter:

```text
yes
```

Expected:

```text
Destroy complete! Resources: 4 destroyed.
```

Terraform does not force-empty the bucket. Delete test objects and object
versions before destroying it, or AWS will reject the bucket deletion.

## Complete Demo

Run:

```bash
aws sts get-caller-identity
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
terraform output
terraform state list
terraform state show aws_s3_bucket.demo
terraform plan -destroy
terraform destroy
```

## Terraform Lifecycle

```text
              .tf files
                  |
                  v
          terraform init
                  |
                  v
          terraform validate
                  |
                  v
            terraform plan
                  |
                  v
           terraform apply
                  |
                  v
             AWS S3
                  |
                  v
          terraform state
                  |
                  v
          terraform destroy
```
