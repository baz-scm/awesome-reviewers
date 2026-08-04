---
title: Region configuration consistency
description: 'Ensure configuration-dependent behavior (region/profile) is applied
  consistently from resolution through client creation through every API call.


  Rules:'
repository: awslabs/mcp
label: Configurations
language: Python
comments_count: 6
repository_stars: 9545
---

Ensure configuration-dependent behavior (region/profile) is applied consistently from resolution through client creation through every API call.

Rules:
1) One source of truth: have a single `get_region(profile?)` (and `get_client_factory(...)`) used everywhere you build requests or resources.
2) Avoid split-brain with singletons: if you support runtime overrides like `set_region_override()`, do not use module-load singleton clients created with a different region. Either rebuild clients when the region changes or require a factory that is created per override.
3) Propagate `region` end-to-end: if a tool accepts `region`, every discovery/status/deep-dive call in that tool must use that same resolved region (not module-global singletons).
4) Prefer resource-scoped values: when AWS responses/ARNs contain the authoritative region, derive it from the ARN (or response) rather than using module-global `AWS_REGION`.
5) Respect profile/account context: any region/account enumeration (e.g., active regions) must honor the selected profile (`AWS_API_MCP_PROFILE_NAME`, `--profile`) consistently.

Example (fixing split-brain with overrides):
```python
_DEFAULT_REGION = os.environ.get('AWS_REGION', 'us-east-1')
_region_override: str | None = None
_client_factory = None

def set_region_override(region: str) -> None:
    global _region_override
    _region_override = region

def get_region() -> str:
    return _region_override or _DEFAULT_REGION

def get_client(service: str):
    # Ensure clients are built with the same resolved region
    region = get_region()
    return boto3.client(service, region_name=region)
```
If you truly must keep singleton clients, document that overrides won’t affect client behavior—otherwise treat it as a correctness bug.