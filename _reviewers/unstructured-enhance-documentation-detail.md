---
title: Enhance documentation detail
description: Documentation should provide comprehensive detail that enables users
  to understand impacts and developers to understand implementation. For breaking
  changes, include migration guidance, deprecated features, and specific functional
  changes. For technical documentation, provide granular step-by-step explanations
  that trace execution flow.
repository: Unstructured-IO/unstructured
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 12117
---

Documentation should provide comprehensive detail that enables users to understand impacts and developers to understand implementation. For breaking changes, include migration guidance, deprecated features, and specific functional changes. For technical documentation, provide granular step-by-step explanations that trace execution flow.

For breaking changes in changelogs:
- Advise where to find replacement functionality
- List all deprecated extras/features
- Specify which submodules or functionalities are removed
- Include related implementation updates

For developer guides:
- Diagram and explain the complete execution journey
- Trace granularly at function level (e.g., "incoming request -> constructing command -> building pipeline -> executing pipeline")
- Enable developers to understand where code fits and how to debug

Example from changelog:
```markdown
## 0.16.0

### Breaking Changes
* **Remove ingest implementation**
  - Migration: Use new unstructured-ingest library (link to installation guide)
  - Deprecated extras: s3, local-inference, github (see migration guide)
  - Removed submodules: unstructured.ingest.v1.*, unstructured.ingest.connectors.*
  - Related: embed submodule updated with SecretStr for secret handling
```