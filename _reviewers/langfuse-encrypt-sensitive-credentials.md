---
title: Encrypt sensitive credentials
description: Sensitive credentials such as API keys, passwords, access tokens, and
  secret keys should never be stored in plain text in databases or configuration files.
  This creates significant security risks if the database is compromised or if unauthorized
  access occurs.
repository: langfuse/langfuse
label: Security
language: Sql
comments_count: 1
repository_stars: 13574
---

Sensitive credentials such as API keys, passwords, access tokens, and secret keys should never be stored in plain text in databases or configuration files. This creates significant security risks if the database is compromised or if unauthorized access occurs.

Instead:
- Use encryption for sensitive fields before storing in the database
- Consider dedicated secret management solutions (like HashiCorp Vault, AWS Secrets Manager)
- Use environment variables for local development

Example of an improved approach:
```sql
-- CreateTable
CREATE TABLE "blob_storage_integrations" (
    "project_id" TEXT NOT NULL,
    "bucket_name" TEXT NOT NULL,
    "prefix" TEXT NOT NULL,
    "access_key_id" TEXT NOT NULL,
    "encrypted_secret_key" TEXT NOT NULL,
    "encryption_iv" TEXT NOT NULL,
```

In your application code, implement proper encryption/decryption methods to handle these sensitive values when needed.