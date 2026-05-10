---
title: Config Contracts And Defaults
description: 'Treat environment variables and configuration flags as a documented
  contract: the code must (1) read settings from the correct source with safe defaults,
  (2) make feature-flag behavior explicit (including what becomes a true no-op when
  disabled), and (3) validate any external runtime dependency that the integration
  relies on.'
repository: infiniflow/ragflow
label: Configurations
language: Python
comments_count: 5
repository_stars: 80174
---

Treat environment variables and configuration flags as a documented contract: the code must (1) read settings from the correct source with safe defaults, (2) make feature-flag behavior explicit (including what becomes a true no-op when disabled), and (3) validate any external runtime dependency that the integration relies on.

Apply this standard:
- Feature flags: if a toggle changes output structure, confirm the “disabled” behavior is intentional and harmless to the core payload.
  - Example pattern:
    ```python
    docs = {}
    if include_document_metadata:
        documents = DocumentService.get_by_ids([...])
        docs = {d.id: DocMetadataService.get_document_metadata(d.id) or {} for d in documents}
    # When false, metadata loop should no-op; chunk title/url/content still come from chunks.
    ```
- Config/env parsing: use the intended settings/env source and add a default to avoid breaking existing deployments.
  - Example pattern:
    ```python
    secure = str(settings.MINIO.get("secure", False)).lower() == "true"
    client = Minio(host, access_key=..., secret_key=..., secure=secure)
    ```
- External dependency validation: if a library shells out (e.g., Java) or relies on host tools, detect and warn/fail early with the required version and where it must be installed.
- Environment variable semantics: document assumptions about env-var behavior (e.g., `CUDA_VISIBLE_DEVICES` remapping makes device indices continuous within the process), and ensure the code aligns with those semantics.
- Avoid config mistakes: keep imports consistent with the intended module (e.g., `DEBUG` from the correct settings namespace).