---
title: avoid hardcoded secrets
description: Never include real API keys, passwords, or other sensitive credentials
  directly in source code, including example files and configuration. This creates
  security vulnerabilities and risks credential exposure in version control systems.
repository: Unstructured-IO/unstructured
label: Security
language: Python
comments_count: 2
repository_stars: 12117
---

Never include real API keys, passwords, or other sensitive credentials directly in source code, including example files and configuration. This creates security vulnerabilities and risks credential exposure in version control systems.

For example code and documentation, use clear placeholder text that indicates where credentials should be provided:

```python
# Bad - real API key hardcoded
access_config=PineconeAccessConfig(api_key="0e8555a2-b944-4da4-837e-03b1202e00c7")

# Good - clear placeholder
access_config=PineconeAccessConfig(api_key="<YOUR_PINECONE_API_KEY_HERE>")

# Better - environment variable
access_config=PineconeAccessConfig(api_key=os.getenv("PINECONE_API_KEY"))
```

When handling credentials in configuration classes, mark sensitive fields appropriately to ensure they are handled securely:

```python
@dataclass
class SqlAccessConfig(AccessConfig):
    username: str  # Not sensitive, needed for access
    password: t.Optional[str] = enhanced_field(sensitive=True)  # Mark as sensitive
```

Use environment variables, secure configuration files, or credential management systems for real deployments.