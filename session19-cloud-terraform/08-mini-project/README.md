# 08 - Session 19 Mini Project

---

# Requirements

Create:

```text
AWS Region
   |
   v
VPC: 10.20.0.0/16
   |
   +-- Public Subnet: 10.20.1.0/24
   |
   +-- Internet Gateway
   |
   +-- Public Route Table
   |
   +-- Route Table Association
   |
   +-- Web Security Group
   |
   +-- EC2 web instance
   |
   +-- Private, encrypted, versioned S3 bucket
```

The EC2 demo exposes HTTP only and does not open SSH. S3 public access is
blocked; the bucket is not force-deleted if it contains objects.

---

# What This Demonstrates

You are now combining:

```text
Cloud fundamentals
        +
Networking
        +
Terraform
```

---

# Project Structure

```text
08-mini-project/
|
|-- README.md
|-- versions.tf
|-- variables.tf
|-- main.tf
|-- outputs.tf
|-- terraform.tfvars.example
|-- .gitignore
```

---

# Architecture

```text
                         Internet
                            |
                            v
                   Internet Gateway
                            |
                    +-------+-------+
                    |      VPC      |
                    |  10.20.0.0/16 |
                    |                |
                    |  Route Table   |
                    |       |        |
                    |       v        |
                    | Public Subnet  |
                    | 10.20.1.0/24  |
                    |       |        |
                    | Security Group |
                    |       |        |
                    |  EC2 + Nginx   |
                    +----------------+

       Terraform-managed S3 bucket (private, encrypted, versioned)
```

---

# Run the Project

Copy variables:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Initialize:

```bash
terraform init
```

Format:

```bash
terraform fmt
```

Validate:

```bash
terraform validate
```

Expected:

```text
Success! The configuration is valid.
```

Plan:

```bash
terraform plan
```

The plan creates billable AWS resources, including an EC2 instance. Read the
entire plan, confirm the selected account and region, and consider the
estimated cost before applying. The project is not automatically applied.

Apply:

```bash
terraform apply
```

Enter:

```text
yes
```

---

# Verify

Show outputs:

```bash
terraform output
```

Expected shape:

```text
instance_id = "i-..."
instance_public_dns = "ec2-...compute.amazonaws.com"
security_group_id = "sg-..."
subnet_id = "subnet-..."
website_url = "http://ec2-...compute.amazonaws.com"
vpc_cidr = "10.20.0.0/16"
vpc_id = "vpc-..."
s3_bucket_name = "session19-lab-..."
```

Test the HTTP endpoint after the EC2 instance finishes bootstrapping:

```bash
curl "$(terraform output -raw website_url)"
```

The response should contain `Session 19 Terraform web demo`.

Show resources:

```bash
terraform state list
```

Expected:

```text
aws_internet_gateway.main
aws_route_table.public
aws_route_table_association.public
aws_security_group.web
aws_subnet.public
aws_instance.web
aws_s3_bucket.artifacts
aws_s3_bucket_public_access_block.artifacts
aws_s3_bucket_server_side_encryption_configuration.artifacts
aws_s3_bucket_versioning.artifacts
aws_vpc.main
```

---

# AWS CLI Verification (Optional -> You can check directly in dashboard too)

VPC:

```bash
aws ec2 describe-vpcs \
  --filters "Name=tag:Name,Values=session19-mini-vpc" \
  --query 'Vpcs[].{VpcId:VpcId,Cidr:CidrBlock,State:State}'
```

Subnet:

```bash
aws ec2 describe-subnets \
  --filters "Name=tag:Name,Values=session19-mini-public-subnet" \
  --query 'Subnets[].{SubnetId:SubnetId,Cidr:CidrBlock,AZ:AvailabilityZone}'
```

Route table:

```bash
aws ec2 describe-route-tables \
  --filters "Name=tag:Name,Values=session19-mini-public-rt" \
  --query 'RouteTables[].{RouteTableId:RouteTableId,VpcId:VpcId}'
```

Security group:

```bash
aws ec2 describe-security-groups \
  --filters "Name=group-name,Values=session19-mini-web-sg" \
  --query 'SecurityGroups[].{GroupId:GroupId,VpcId:VpcId}'
```

EC2:

```bash
aws ec2 describe-instances \
  --instance-ids "$(terraform output -raw instance_id)" \
  --query 'Reservations[].Instances[].{InstanceId:InstanceId,State:State.Name,PublicDnsName:PublicDnsName}'
```

S3:

```bash
aws s3api get-public-access-block \
  --bucket "$(terraform output -raw s3_bucket_name)"
aws s3api get-bucket-encryption \
  --bucket "$(terraform output -raw s3_bucket_name)"
```

---

# Cleanup

```bash
terraform plan -destroy
terraform destroy
```

Enter:

```text
yes
```

Expected:

```text
Destroy complete! Resources: 11 destroyed.
```

Remove any S3 test objects and versions before destroying the bucket. Stop
the EC2 instance only if you intend to retain the rest of the infrastructure;
`terraform destroy` removes all resources managed by this project.

---

## Security discussion

This is a short-lived lab, not a production network. Explain why the instance
has no SSH ingress, why the S3 bucket blocks public access, and what further
controls (private subnet, IAM instance profile, restricted egress, monitoring
and backups) a production design would need.

---

# Interview Questions

Explain these without looking at notes:

```text
1. IaaS vs PaaS vs SaaS
2. Region vs Availability Zone
3. VPC vs Subnet
4. Public vs Private Subnet
5. Route Table
6. Internet Gateway
7. Security Group
8. Terraform
9. terraform plan vs terraform apply
10. terraform state
11. terraform destroy
```
