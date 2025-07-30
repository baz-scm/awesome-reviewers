---
title: embedding provider configuration
description: When configuring embedding providers in AI integrations, ensure proper
  dimension specification and use dedicated test files for different providers. Always
  specify the embedding dimension that matches your chosen provider (e.g., 384 for
  huggingface embedders) and avoid modifying existing configurations for testing purposes.
repository: Unstructured-IO/unstructured
label: AI
language: Shell
comments_count: 2
repository_stars: 12117
---

When configuring embedding providers in AI integrations, ensure proper dimension specification and use dedicated test files for different providers. Always specify the embedding dimension that matches your chosen provider (e.g., 384 for huggingface embedders) and avoid modifying existing configurations for testing purposes.

Instead of changing embedding providers in existing files for testing, create separate test files for each provider. This prevents disruption to working configurations and provides clearer test isolation.

Example of proper configuration:
```bash
PYTHONPATH=. ./unstructured/ingest/main.py \
  --embedding-provider "langchain-huggingface" \
  --embedding-dimension 384 \
  astra \
  --token "$ASTRA_DB_APPLICATION_TOKEN" \
  --collection-name "$COLLECTION_NAME"
```

For testing new providers, create dedicated test files like `test_unstructured_ingest/src/local-embed-vertexai.sh` rather than modifying existing provider configurations. This approach maintains stability while enabling comprehensive testing of different AI embedding services.