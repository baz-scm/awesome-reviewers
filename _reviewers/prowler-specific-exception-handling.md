---
title: Specific exception handling
description: Handle exceptions with specificity rather than using broad catch-all
  blocks. Catch specific exception types, provide clear error messages, and respond
  appropriately based on the error type. This improves error diagnosis and enables
  targeted recovery strategies.
repository: prowler-cloud/prowler
label: Error Handling
language: Python
comments_count: 8
repository_stars: 11834
---

Handle exceptions with specificity rather than using broad catch-all blocks. Catch specific exception types, provide clear error messages, and respond appropriately based on the error type. This improves error diagnosis and enables targeted recovery strategies.

For example, instead of:
```python
try:
    decrypted_key = fernet.decrypt(self.api_key)
    return decrypted_key.decode()
except Exception:
    return None
```

Use specific exception types with proper logging:
```python
try:
    decrypted_key = fernet.decrypt(self.api_key)
    return decrypted_key.decode()
except InvalidToken:
    logger.warning("Failed to decrypt API key: invalid token.")
    return None
except Exception as e:
    logger.error(f"Unexpected error while decrypting API key: {e}")
    return None
```

For service-specific errors (like AWS S3), handle known error codes separately:
```python
try:
    s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
except ClientError as e:
    error_code = e.response.get("Error", {}).get("Code")
    if error_code == "NoSuchKey":
        return Response(
            {"detail": "The scan has no reports."},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(
        {"detail": "There is a problem with credentials."},
        status=status.HTTP_403_FORBIDDEN,
    )
```

Also, ensure that error messages are consistent with the actual state of the system and don't report success when errors occur.