---
title: Prefer lightweight observability integrations
description: Observability integrations should minimize external dependencies and
  avoid patching LiteLLM's core functions. Instead of requiring users to install additional
  SDKs, prefer lightweight approaches using custom loggers with direct HTTP calls
  (like httpx) or implement CustomBatchLogger interfaces. Avoid monkey-patching completion
  functions as this can cause...
repository: BerriAI/litellm
label: Observability
language: Markdown
comments_count: 3
repository_stars: 28310
---

Observability integrations should minimize external dependencies and avoid patching LiteLLM's core functions. Instead of requiring users to install additional SDKs, prefer lightweight approaches using custom loggers with direct HTTP calls (like httpx) or implement CustomBatchLogger interfaces. Avoid monkey-patching completion functions as this can cause unexpected errors and conflicts with other integrations.

The preferred pattern follows langsmith's approach - use pure httpx for sending telemetry data rather than requiring SDK installations. This reduces dependency bloat, prevents version conflicts, and maintains better isolation between different observability tools.

Example of preferred approach:
```python
# Good: Lightweight custom logger
class MyObservabilityLogger(CustomBatchLogger):
    def __init__(self, api_key):
        self.api_key = api_key
        
    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        # Use httpx to send data directly
        httpx.post("https://api.example.com/logs", 
                  json={"request": kwargs, "response": response_obj})

# Avoid: Requiring SDK installation and patching
# weave.init()  # This patches litellm functions
```

This approach ensures observability works reliably across all LiteLLM providers without introducing additional complexity or potential conflicts.