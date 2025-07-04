---
title: Enforce authentication boundaries
description: 'Implement strict authentication boundaries and access controls to prevent
  security vulnerabilities:


  1. When multiple authentication methods are supported, ensure they are mutually
  exclusive to prevent confusion about which method is active. Add validation code
  that raises explicit exceptions when conflicting credentials are provided.'
repository: apache/airflow
label: Security
language: Other
comments_count: 3
repository_stars: 40858
---

Implement strict authentication boundaries and access controls to prevent security vulnerabilities:

1. When multiple authentication methods are supported, ensure they are mutually exclusive to prevent confusion about which method is active. Add validation code that raises explicit exceptions when conflicting credentials are provided.

Example:
```python
def authenticate(self):
    if self.jwt_token and self.username and self.password:
        raise AirflowException(
            "Both JWT and Password/Username authentication provided. "
            "Please configure only one authentication method."
        )
    
    if self.jwt_token:
        return self._authenticate_with_jwt()
    elif self.username and self.password:
        return self._authenticate_with_credentials()
    else:
        raise AirflowException("No valid authentication method configured")
```

2. Restrict direct access to sensitive resources (like databases) by implementing authentication barriers and API-based access patterns. This follows the principle of least privilege, where components should only have the minimum access necessary to perform their functions.

3. For token-based authentication systems, implement proper token lifecycle management including secure issuance, validation, renewal, and expiration handling through well-defined communication channels.