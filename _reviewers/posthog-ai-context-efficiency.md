---
title: AI context efficiency
description: When providing context to LLMs, choose the most efficient method based
  on the nature and size of the context data. For bounded, static context (like feature
  flag mappings or configuration options), inject the information directly into the
  system prompt rather than using tool calls. This approach is faster, more cost-effective,
  and reduces complexity.
repository: PostHog/posthog
label: AI
language: Python
comments_count: 4
repository_stars: 28460
---

When providing context to LLMs, choose the most efficient method based on the nature and size of the context data. For bounded, static context (like feature flag mappings or configuration options), inject the information directly into the system prompt rather than using tool calls. This approach is faster, more cost-effective, and reduces complexity.

**Prefer prompt injection when:**
- Context data is relatively small and bounded
- Data doesn't change frequently during the conversation
- You want to minimize API calls and latency

**Use tool calls when:**
- Context data is large or unbounded
- Data needs to be fetched dynamically based on user input
- You need the LLM to make decisions about what context to retrieve

**Example:**
```python
# Good: Inject bounded feature flag context into prompt
enhanced_system_prompt = SURVEY_CREATION_SYSTEM_PROMPT
if feature_flag_context:
    enhanced_system_prompt += f"\n\n## Available Feature Flags\n{feature_flag_context}"

# Avoid: Using tool calls for static, bounded context
# This adds unnecessary complexity and cost
def retrieve_flag_id(feature_key): # Tool call - overkill for small static data
    return api_call_to_get_flag_id(feature_key)
```

Also ensure your prompts only reference capabilities the LLM actually has - avoid instructing LLMs to manipulate internal state variables they cannot access.