# Amazon EC2: Compute

Amazon Elastic Compute Cloud (EC2) provides virtual machine instances in an
AWS Region. An instance runs in one Availability Zone and is launched from
an Amazon Machine Image (AMI).

## Core concepts

- **AMI:** A regional machine image containing an operating system and
  optional software configuration.
- **Instance type:** Defines CPU, memory, networking and accelerator
  characteristics. Choose based on measured workload needs.
- **Key pair:** A public/private key credential used for supported remote
  login methods. Protect private keys and never commit them.
- **Security Group:** A stateful virtual firewall attached to network
  interfaces/instances. Inbound access is denied unless allowed by a rule;
  return traffic for allowed connections is permitted.
- **EBS:** Persistent block storage volumes commonly attached to EC2
  instances. Volume lifecycle and backups should be planned separately.
- **Public IP:** Routable only when the subnet route, address assignment and
  security controls allow it. A private IP is used for VPC-internal
  communication and private routing.
- **Lifecycle:** Instances move through pending, running, stopping/stopped,
  shutting-down and terminated states. Stop/start can change an
  auto-assigned public IPv4 address; termination removes the instance.

## Common use cases

EC2 can host web services, build agents, development environments, batch
workers and legacy applications. Prefer managed services when they reduce
operational burden; use EC2 when instance-level control is required.

## Operational and security notes

- Patch the guest operating system and use supported AMIs.
- Attach an IAM instance profile rather than storing AWS keys on the host.
- Expose only required ports and restrict administrative access.
- Encrypt EBS volumes and establish backup/recovery practices.
- Review instance and data-transfer costs; stop or terminate unused labs.

## References

- [Amazon EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
- [EC2 instance types](https://aws.amazon.com/ec2/instance-types/)
