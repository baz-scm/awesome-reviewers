---
title: Use configurable default values
description: Make configuration values flexible and robust by avoiding hardcoded values
  and providing sensible defaults. This ensures your application works correctly even
  with incomplete configuration and supports different environments without code changes.
repository: prowler-cloud/prowler
label: Configurations
language: Python
comments_count: 8
repository_stars: 11834
---

Make configuration values flexible and robust by avoiding hardcoded values and providing sensible defaults. This ensures your application works correctly even with incomplete configuration and supports different environments without code changes.

Key practices:
1. Use environment variables with default values:
```python
# Better: Provide a sensible default
prowler_db_connection = os.environ.get('PROWLER_DB_CONNECTION', "memory://")

# Better: Use framework utilities for type conversion
FINDINGS_BATCH_SIZE = env.int("DJANGO_FINDINGS_BATCH_SIZE", 1000)
```

2. Extract magic numbers into configurable settings:
```python
# Problematic: Hardcoded threshold
if months_inactive >= 6:

# Better: Use a configurable setting
inactive_threshold_days = settings.REPOSITORY_INACTIVE_THRESHOLD_DAYS
months_inactive = (now - latest_activity).days / 30.44
if months_inactive >= inactive_threshold_days / 30.44:
```

3. Make version requirements configurable to avoid code changes for policy updates:
```python
# Problematic: Hardcoded version check
if sql_server.minimal_tls_version in ("1.2", "1.3"):

# Better: Use configuration setting
if sql_server.minimal_tls_version in settings.RECOMMENDED_TLS_VERSIONS:
```

4. Implement graceful fallbacks when configurations are missing:
```python
try:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_DEFAULT_REGION,
    )
except (ClientError, NoCredentialsError, ParamValidationError, ValueError):
    # Fallback to default credentials provider chain
    s3_client = boto3.client("s3")
```

This approach makes your application more maintainable, environment-agnostic, and future-proof.