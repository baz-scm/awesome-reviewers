---
title: Region Configuration Standard
description: Do not hard-code AWS region (or other environment-specific settings)
  inside scripts or service logic. Instead, make region resolution consistent, configurable,
  and source-of-truth driven.
repository: awslabs/agentcore-samples
label: Configurations
language: Python
comments_count: 4
repository_stars: 3244
---

Do not hard-code AWS region (or other environment-specific settings) inside scripts or service logic. Instead, make region resolution consistent, configurable, and source-of-truth driven.

Practical rules:
- Prefer the standard environment variable: `AWS_REGION` (or `AWS_DEFAULT_REGION`).
- If not set, infer from the active AWS credentials/session (e.g., boto3 `Session().region_name`).
- Allow an explicit override via CLI/config (e.g., `--region`) when the environment differs from the default.
- Keep service-specific conditionals data-driven (e.g., handle `us-east-1` LocationConstraint) but do not embed fixed regions as the primary configuration.

Example pattern:
```python
import os
import boto3
import argparse


def resolve_region(cli_region: str | None) -> str:
    if cli_region:
        return cli_region
    return (
        os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or boto3.session.Session().region_name
        or "us-west-2"  # only if you truly want a documented fallback
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", help="AWS region for all AWS clients")
    args = parser.parse_args()

    region = resolve_region(args.region)
    s3 = boto3.client("s3", region_name=region)
```

Impact: fewer “works in my account” failures, consistent behavior across deployments (us-east-1 vs us-west-2), and clearer configuration management.