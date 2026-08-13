---
title: Control Agent Context Budgets
description: 'Always cap and actively prevent generative-agent context bloat.


  1) Enforce explicit context/prompt budgets in code (hard max + warning threshold)
  so inputs never silently grow.'
repository: bmad-code-org/bmad-method
label: AI
language: JavaScript
comments_count: 2
repository_stars: 51859
---

Always cap and actively prevent generative-agent context bloat.

1) Enforce explicit context/prompt budgets in code (hard max + warning threshold) so inputs never silently grow.
2) Prevent accidental retrieval/ingestion of large file sets into the model context. For agent config generation, ensure `resources` (or equivalent auto-loaded context) is empty unless the agent explicitly needs it—otherwise the agent may load far more than intended.
3) Validate after configuration changes using your existing guardrails (warn/error) or integration checks, since misconfigured resource loading can manifest as “context limit/token limit” issues.

Example (pattern):
```js
// 1) Context budget guardrails
const LLM_MAX_CHARS = 700_000;
const LLM_WARN_CHARS = 600_000;

function enforceContextBudget(text) {
  if (text.length > LLM_MAX_CHARS) {
    throw new Error('LLM context exceeds maximum allowed size');
  }
  if (text.length > LLM_WARN_CHARS) {
    console.warn('LLM context nearing maximum allowed size');
  }
}

// 2) Avoid auto-loading repo files into context
function buildAmazonQAgentConfig({ title, prompt, tools, resourcesFromYaml }) {
  return {
    name: `bmad-${title}`,
    prompt,
    tools,
    // Default: empty; only populate if YAML explicitly requires it.
    resources: Array.isArray(resourcesFromYaml) ? resourcesFromYaml : [],
  };
}
```

Apply this standard whenever you:
- tune model input sizes or prompt composition
- generate agent configs or wire up “resources/files” features
- change retrieval/context logic (directly or indirectly)