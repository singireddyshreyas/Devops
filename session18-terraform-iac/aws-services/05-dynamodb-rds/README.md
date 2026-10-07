# DynamoDB and Amazon RDS

AWS provides both managed NoSQL and relational database services. Select
based on data model, query needs, consistency, operational requirements and
cost—not only on familiarity.

## DynamoDB

DynamoDB is a managed NoSQL key-value and document database.

- A **table** contains items.
- An **item** is a record; its **attributes** are named values.
- The **partition key** determines the partition used to locate an item.
- An optional **sort key** orders related items that share a partition key
  and supports range/key-condition queries.
- Primary key design determines query patterns and distribution; avoid hot
  partitions by choosing keys with appropriate cardinality and access
  distribution.

Common use cases include low-latency key-value lookups, session state,
shopping carts, event metadata and applications with predictable access
patterns.

## Amazon RDS

Amazon Relational Database Service operates relational database engines,
including Amazon Aurora, PostgreSQL, MySQL, MariaDB, Oracle and Microsoft SQL
Server (availability and features vary by Region and engine).

- A **DB instance** provides compute and storage for a database deployment.
- Network placement, security groups, credentials and encryption control
  database access.
- Automated backups and snapshots support recovery; define retention and
  test restores.
- **Multi-AZ** deployments provide a standby/failover capability; they are
  not the same as read scaling.
- **Read replicas** can offload read traffic and improve read availability;
  replication behavior and promotion options depend on the engine.

Common use cases include applications needing relational constraints,
transactions, joins and SQL-compatible operations.

## Comparison

| Need | Consider |
| --- | --- |
| Flexible key-value access at large scale | DynamoDB |
| Relational joins, SQL and transactions | RDS |
| Managed operations | Both provide managed capabilities, but operational responsibilities differ |
| Availability/recovery | Design explicitly with backups, replicas/failover and tested recovery objectives |

## References

- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
