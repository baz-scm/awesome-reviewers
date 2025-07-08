---
title: AI model persistence
description: When containerizing AI applications, ensure proper model persistence
  by mounting volumes to the default cache locations used by AI frameworks and setting
  appropriate environment variables. This prevents redundant downloads of large models
  and improves development efficiency.
repository: vllm-project/vllm
label: AI
language: Other
comments_count: 2
repository_stars: 51730
---

When containerizing AI applications, ensure proper model persistence by mounting volumes to the default cache locations used by AI frameworks and setting appropriate environment variables. This prevents redundant downloads of large models and improves development efficiency.

Example for Hugging Face models in Docker:
```yaml
volumes:
  - models:/root/.cache/huggingface
environment:
  HF_HOME: /root/.cache/huggingface
```