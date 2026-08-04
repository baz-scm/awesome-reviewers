---
title: Parameterized Runtime Configuration
description: 'Ensure configuration is explicit, supported, and environment-specific
  values are parameterized.


  Apply these rules:

  - Use non-deprecated minimum runtime versions in setup docs (e.g., prefer Python
  3.10+ over 3.8/3.9).'
repository: awslabs/agentcore-samples
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 3244
---

Ensure configuration is explicit, supported, and environment-specific values are parameterized.

Apply these rules:
- Use non-deprecated minimum runtime versions in setup docs (e.g., prefer Python 3.10+ over 3.8/3.9).
- Do not rely on “defaults” for environment-specific endpoints; require/derive them from variables (especially region/account-specific service URLs).
- Make local dev environment setup deterministic by providing commands that install the correct tooling into the intended virtual environment.

Example (.env + derived endpoint):
```bash
# .env
AWS_REGION=us-west-2
ENDPOINT_URL=https://bedrock-agentcore-control.${AWS_REGION}.amazonaws.com
```

Example prerequisite update (doc):
- “Python 3.10+ required” (instead of 3.8/3.9) and keep dev commands consistent with that environment.