---
title: Typed API Contracts
description: 'For each API endpoint, treat the request as a strict contract: define
  a dedicated typed request model for the exact payload shape, validate required inputs
  early, and keep auth/tenant scoping and client URL construction consistent.'
repository: infiniflow/ragflow
label: API
language: Python
comments_count: 5
repository_stars: 80174
---

For each API endpoint, treat the request as a strict contract: define a dedicated typed request model for the exact payload shape, validate required inputs early, and keep auth/tenant scoping and client URL construction consistent.

Apply:
- Use a dedicated request schema per endpoint (don’t reuse a model if the payload shape differs). 
- Validate required fields immediately (e.g., reject empty or missing required collections).
- Build/whitelist update payloads from allowed fields only.
- Use centralized auth (e.g., a decorator) rather than manual token parsing; enforce tenant ownership/scoping invariants for create/update/delete.
- Keep endpoint base URL/versioning and Authorization header formats consistent between client and server.

Example (endpoint + Pydantic request validation):
```python
from pydantic import BaseModel, Field
from flask import request

class UpdateMetadataSettingReq(BaseModel):
    metadata: dict
    enable_metadata: bool | None = None
    built_in_metadata: dict | None = None

@app.route('/document/update_metadata_setting', methods=['POST'])
@token_required
def update_metadata_setting(tenant_id):
    req = UpdateMetadataSettingReq.model_validate(request.json)

    update_payload = {"metadata": req.metadata}
    if req.enable_metadata is not None:
        update_payload["enable_metadata"] = req.enable_metadata
    if req.built_in_metadata is not None:
        update_payload["built_in_metadata"] = req.built_in_metadata

    # additionally enforce tenant ownership before updating
    DocumentService.update_parser_config(doc_id=req_id, update_payload=update_payload)
    return get_json_result(data=True)
```

This prevents payload mismatches, inconsistent behavior across endpoints, and security/ownership mistakes while keeping API clients predictable (stable URL/version and auth header conventions).