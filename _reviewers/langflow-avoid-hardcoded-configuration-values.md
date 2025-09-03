---
title: Avoid hardcoded configuration values
description: Replace hardcoded configuration values with configurable parameters to
  improve flexibility and maintainability. Hardcoded timeouts, domain strings, validation
  constraints, and operational parameters should be exposed as advanced inputs, environment
  variables, or settings.
repository: langflow-ai/langflow
label: Configurations
language: Python
comments_count: 4
repository_stars: 111046
---

Replace hardcoded configuration values with configurable parameters to improve flexibility and maintainability. Hardcoded timeouts, domain strings, validation constraints, and operational parameters should be exposed as advanced inputs, environment variables, or settings.

Examples of improvements:
- Expose timeout values as configurable inputs: `timeout_seconds` parameter instead of hardcoded `timeout=600`
- Make domain strings configurable: `domain` input instead of hardcoded `"audio.transcription"`
- Allow environment-specific validation: configurable URL scheme validation that can accept `http://` for local development while defaulting to `https://` for production
- Convert magic numbers to named constants with configuration options: `MAX_SESSIONS_PER_SERVER`, `SESSION_IDLE_TIMEOUT` that can be overridden via settings

```python
# Instead of hardcoded values:
response = client.predictions.wait(response.id, timeout=600)
domain = "audio.transcription"

# Use configurable parameters:
IntInput(
    name="timeout_seconds",
    display_name="Timeout (seconds)",
    value=600,
    advanced=True,
    info="Maximum time to wait for processing completion"
)

DropdownInput(
    name="domain",
    display_name="Processing Domain",
    options=["audio.transcription", "audio.diarization"],
    value="audio.transcription",
    advanced=True
)
```

This approach enables users to customize behavior for their specific use cases, supports different environments (development vs production), and makes the code more maintainable by centralizing configuration management.