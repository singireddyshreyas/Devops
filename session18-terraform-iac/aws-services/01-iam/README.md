# AWS IAM: Identity and Access Management

IAM controls who or what can access AWS and which actions are permitted.
Access decisions are based on identities, policies and resource policies.

## Main concepts

- **User:** An identity for a person or workload requiring long-term
  credentials. Prefer federation and temporary credentials over access keys.
- **Group:** A collection of users to which identity policies can be
  attached. Groups do not contain roles.
- **Role:** An identity with permissions assumed temporarily by a trusted
  principal, such as an EC2 workload, CI job or federated user.
- **Policy:** A JSON document describing allowed or explicitly denied
  actions, resources and optional conditions.
- **Permission:** The effective result of applicable identity, resource,
  boundary and organization policies; an explicit deny overrides an allow.

## Least privilege and best practices

1. Grant only the actions and resources needed for a task; scope policies
   with resource ARNs and conditions wherever supported.
2. Prefer IAM Identity Center/federation for people and IAM roles for
   workloads. Avoid long-lived access keys and never commit credentials.
3. Do not use the root user for daily work; protect it with MFA and keep its
   credentials secure.
4. Use separate roles for separate workloads and limit which principals may
   assume each role.
5. Review unused permissions and rotate/revoke credentials when necessary.
6. Enable CloudTrail and monitor IAM and account activity.

## Common use cases

- A developer signs in through a federated identity provider and assumes a
  role for a limited development account.
- An EC2 instance assumes an instance profile role to read a specific S3
  prefix without embedding an access key on disk.
- A GitHub Actions workflow uses short-lived OIDC federation to assume a
  deployment role instead of storing AWS access keys.

## References

- [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
