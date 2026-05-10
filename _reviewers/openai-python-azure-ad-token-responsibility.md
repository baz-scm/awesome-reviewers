---
title: Azure AD token responsibility
description: When adding Azure Active Directory authentication (Security), make token
  acquisition and dependency responsibility explicit and align it with your SDK’s
  lifecycle.
repository: openai/openai-python
label: Security
language: Markdown
comments_count: 2
repository_stars: 30731
---

When adding Azure Active Directory authentication (Security), make token acquisition and dependency responsibility explicit and align it with your SDK’s lifecycle.

- If your client library has no initialization state (or you want to avoid hidden auth flows), require the caller to obtain the AAD token (e.g., via `azure.identity`) and pass it into the request.
- Do not add authentication dependencies server-side unless the library truly performs token acquisition. Prefer: caller uses the Azure SDK/identity, then your client only transmits the resulting token.
- Document the exact contract: set `api_type = "azure_ad"` and provide the acquired credential token as `api_key` (used for request headers).

Example (documented flow):
```python
from azure.identity import DefaultAzureCredential
import openai

default_credential = DefaultAzureCredential()
# Acquire token for Azure Cognitive Services
token = default_credential.get_token("https://cognitiveservices.azure.com")

openai.api_type = "azure_ad"
openai.api_key = token.token
```

This keeps the authentication flow predictable (caller-owned, token-only passthrough) and reduces the risk of surprising security behavior or broken SDK integration.