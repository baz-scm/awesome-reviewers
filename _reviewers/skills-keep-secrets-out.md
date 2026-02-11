---
title: Keep secrets out
description: Do not commit secret keys, credentials, or signing material to source
  code or public repos. Store secrets in environment variables or a managed secret
  store, load them at runtime, and ensure they are not present in repository history.
  Design signed tokens so that the server validates them and they are short-lived,
  and have a plan to rotate/revoke keys if...
repository: openai/skills
label: Security
language: Python
comments_count: 1
repository_stars: 7991
---

Do not commit secret keys, credentials, or signing material to source code or public repos. Store secrets in environment variables or a managed secret store, load them at runtime, and ensure they are not present in repository history. Design signed tokens so that the server validates them and they are short-lived, and have a plan to rotate/revoke keys if exposure occurs.

Why: a secret embedded in code (e.g., SECRET_KEY used to HMAC-sign tokens) can be extracted and used to forge or replay tokens even if tokens have expirations. Removing secrets from code reduces attack surface and supports secure key management.

How to apply:
- Replace hard-coded secrets with environment/config values. Example change (mimicking the script):

OLD:
SECRET_KEY = "dfc92bc5e95825103283f01c2aa6ca7fe7f6ffc31778ea82c354785c73b0858c"

NEW:
import os
SECRET_KEY = os.environ.get("MERCH_SECRET_KEY")  # set via env or secret manager
if not SECRET_KEY:
    raise RuntimeError("MERCH_SECRET_KEY not configured")

- Use a secret manager (AWS Secrets Manager, GCP Secret Manager, Vault) for production; populate environment or runtime config from there.
- Keep tokens short-lived (include timestamp/expiry in payload) and always verify timestamps and signatures server-side.
- If a secret is committed, treat it as compromised: rotate/revoke the key immediately, remove it from the repository and history (e.g., git filter-branch or BFG), and audit any uses.

Checks/PR guidance:
- Ensure no literal secrets (API keys, HMAC secrets, certificates) are added to commits.
- Add automated scanners (pre-commit hooks, CI secret detection) to block accidental commits.
- Document key rotation procedures and TTL expectations for signed tokens.

References: [0]