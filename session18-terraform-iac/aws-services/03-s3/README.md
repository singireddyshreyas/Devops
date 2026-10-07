# Amazon S3: Object Storage

Amazon Simple Storage Service (S3) stores objects inside buckets. An object
consists of data, a key and metadata. S3 is object storage, not a mounted
filesystem or a block device.

## Core concepts

- **Bucket:** A container for objects. Bucket names are globally unique
  within an AWS partition and bucket names are not secret.
- **Object:** Data identified by its key, with optional metadata and
  version information.
- **Storage classes:** Standard, Intelligent-Tiering, Standard-IA,
  One Zone-IA, Glacier Instant/Flexible Retrieval and Deep Archive have
  different access, durability, retrieval and cost characteristics.
- **Versioning:** Retains multiple versions of an object and can help recover
  from accidental overwrite or deletion.
- **Lifecycle policy:** Transitions or expires objects according to age,
  tags or other rule filters.
- **Encryption:** Server-side encryption is available with S3-managed or
  KMS keys; client-side encryption is another option.
- **Bucket policy:** A resource-based JSON policy that can grant or deny
  access to bucket resources. It works alongside IAM and organization
  controls.

## Common use cases

S3 is used for static assets, backups, data lakes, logs and artifacts. Select
the storage class based on access frequency and recovery expectations.

## Safe defaults

Block public access unless public hosting is an explicit reviewed
requirement. Enable encryption, use least-privilege IAM/bucket policies,
consider versioning and lifecycle rules, and audit access. Avoid putting
credentials or sensitive data in object names or public URLs.

## References

- [Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [S3 storage classes](https://aws.amazon.com/s3/storage-classes/)
