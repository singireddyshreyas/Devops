# Amazon VPC: Networking

Amazon Virtual Private Cloud (VPC) provides a logically isolated network
for AWS resources in a Region. A VPC spans Availability Zones; subnets each
belong to one Availability Zone.

## Core concepts

- **CIDR:** Defines the IPv4/IPv6 address range for a VPC or subnet. Plan
  ranges to avoid overlap with connected networks.
- **Subnet:** A range of addresses in one Availability Zone. A subnet is
  considered public when its route table has a route to an Internet Gateway;
  assigning a public IP alone does not create internet routing.
- **Route table:** Selects the next hop for network destinations. Each
  subnet is associated with a route table, explicitly or implicitly.
- **Internet Gateway (IGW):** Enables internet routing for public IPv4/IPv6
  traffic when routes and addressing are configured.
- **NAT Gateway:** Allows instances in private subnets to initiate outbound
  IPv4 connections without accepting unsolicited inbound connections.
  NAT Gateway hourly and data processing charges apply.
- **Security Group:** Stateful firewall attached to network interfaces.
- **Network ACL:** Stateless subnet-level firewall; ingress and egress rules
  are evaluated separately and return traffic must be allowed explicitly.
- **Public vs private subnet:** A route to an IGW makes a subnet public.
  Private subnets normally use NAT or private endpoints for outbound access
  and have no direct IGW route.

## Common use cases

VPCs isolate environments, segment public and private workloads, control
network paths and connect cloud networks to corporate networks or other
VPCs. Use security groups for workload-level access and NACLs for an
additional subnet boundary where required.

## References

- [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [Subnets and route tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html)
