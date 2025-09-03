---
title: Follow consistent naming patterns
description: Maintain consistent naming conventions across all aspects of the codebase,
  including file structures, folder organization, environment variables, and identifiers.
  This ensures predictability and reduces cognitive load for developers.
repository: BerriAI/litellm
label: Naming Conventions
language: Python
comments_count: 7
repository_stars: 28310
---

Maintain consistent naming conventions across all aspects of the codebase, including file structures, folder organization, environment variables, and identifiers. This ensures predictability and reduces cognitive load for developers.

Key principles:
- **File/folder structure**: Match provider names exactly (e.g., `llms/nvidia/` not `llms/meta/` for `meta-llama`)
- **Test organization**: Mirror source structure (`tests/litellm/integrations/SlackAlerting/test_slack_alerting.py` matches `litellm/integrations/SlackAlerting/`)
- **Environment variables**: Follow framework conventions (`*_API_BASE` for litellm, while supporting `*_BASE_URL` for cross-framework compatibility)
- **Naming brevity**: Use concise but clear names (`prisma_airs` instead of `panw_prisma_airs`)
- **External API alignment**: Match external service naming conventions (`space_id` vs `space_key` based on API requirements)

Example:
```python
# Good: Consistent with framework patterns
NVIDIA_API_BASE = os.getenv("NVIDIA_API_BASE") or os.getenv("NVIDIA_BASE_URL")  # Support both

# Good: File structure matches provider
# litellm/llms/nvidia/chat/transformation.py
# tests/litellm/llms/nvidia/chat/test_transformation.py

# Good: Concise enum naming
class SupportedGuardrailIntegrations(Enum):
    PRISMA_AIRS = "prisma_airs"  # Not "panw_prisma_airs"
```