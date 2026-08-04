---
title: Explicit memory disabling
description: When building LLM agents for AgentCore/runtime environments, don’t rely
  on framework defaults for memory. If your agent does not use conversational/session
  memory, explicitly disable it (e.g., set `memory_mode='NO_MEMORY'`) to prevent the
  runtime/framework from automatically creating/using STM.
repository: awslabs/agentcore-samples
label: AI
language: Other
comments_count: 2
repository_stars: 3244
---

When building LLM agents for AgentCore/runtime environments, don’t rely on framework defaults for memory. If your agent does not use conversational/session memory, explicitly disable it (e.g., set `memory_mode='NO_MEMORY'`) to prevent the runtime/framework from automatically creating/using STM.

Example (pattern):
```python
# Only enable memory if you actually need it.
agent = Agent(
    model=bedrock_model,
    system_prompt=system_prompt,
    tools=[web_search],
    memory_mode='NO_MEMORY',
)
```

If you later add memory, make that change intentional (and document why), rather than leaving defaults enabled inadvertently.