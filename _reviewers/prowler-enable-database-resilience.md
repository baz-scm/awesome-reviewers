---
title: Enable database resilience
description: 'Always configure appropriate resilience features for database services
  to ensure data durability and high availability. This includes:


  1. **Enable regular backups with sufficient retention periods** for all database
  clusters to prevent data loss'
repository: prowler-cloud/prowler
label: Database
language: Json
comments_count: 2
repository_stars: 11834
---

Always configure appropriate resilience features for database services to ensure data durability and high availability. This includes:

1. **Enable regular backups with sufficient retention periods** for all database clusters to prevent data loss
2. **Configure multi-AZ deployments** for critical database services to ensure high availability

When implementing these features through infrastructure as code or CLI commands, use placeholders instead of hardcoded values for better reusability and documentation.

Example for configuring DocumentDB backups:
```
aws docdb modify-db-cluster --region <REGION> --db-cluster-identifier <DB_CLUSTER_ID> --backup-retention-period 7 --apply-immediately
```

Example for enabling Multi-AZ for DMS instances:
```
aws dms modify-replication-instance --region <REGION> --replication-instance-arn <REPLICATION_INSTANCE_ARN> --multi-az --apply-immediately
```