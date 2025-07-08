---
title: Consistent environment variable naming
description: 'When naming environment variables, ensure that names are both technically
  accurate and follow established project conventions:


  1. Use terminology that precisely reflects the actual content and purpose of the
  variable, especially for security-related configurations.'
repository: prowler-cloud/prowler
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 11834
---

When naming environment variables, ensure that names are both technically accurate and follow established project conventions:

1. Use terminology that precisely reflects the actual content and purpose of the variable, especially for security-related configurations.

2. Follow established prefixing conventions in your project to indicate which system or component uses the variable.

Example:
```
# Bad: Inconsistent prefixing and potentially unclear naming
ARTIFACTS_STORAGE_PATH="/path/to/artifacts"
SAML_PUBLIC_CERT=""

# Good: Consistent prefixing and accurate naming
DJANGO_ARTIFACTS_STORAGE_PATH="/path/to/artifacts"
DJANGO_SAML_CERT=""  # or DJANGO_SAML_X509_CERT if more precision is needed
```

This approach improves code maintainability by making the purpose of variables immediately clear and ensuring consistency across the codebase.