---
title: AI eval config correctness
description: 'When writing eval/test configurations for AI models and agents, make
  sure each run is properly isolated and uses accurate, model-specific parameters
  so results stay reproducible and uncontaminated:'
repository: promptfoo/promptfoo
label: AI
language: Yaml
comments_count: 3
repository_stars: 26565
---

When writing eval/test configurations for AI models and agents, make sure each run is properly isolated and uses accurate, model-specific parameters so results stay reproducible and uncontaminated:

- Never hardcode a static session/conversation ID for stateful conversational agents (e.g., Bedrock Agents). The service persists prior turns under that ID, so later eval runs can be influenced by context or assertions left over from earlier runs — effectively a form of data leakage across runs. Generate a fresh ID per run (e.g., from an environment variable or timestamp) while keeping the same value across the ordered tests within a single run.
- Match provider request/response payloads exactly to the documented schema for the specific model version under test. Don't carry over fields from a previous model generation (e.g., a `schemaVersion` key used by an older model) if the current model's schema omits it — mismatched schemas can silently produce invalid inference calls and skew evaluation results.
- When mixing deterministic fixed-case tests with generated adversarial/red-team cases, keep them in separate configs with assertions tuned to each mode (e.g., `guardrails`/`not-guardrails` vs a redteam `defaultTest` override), so an attack that is allowed through isn't mis-scored as acceptable output.

Following these practices keeps AI evaluation pipelines deterministic, comparable across runs, and faithful to the actual model/agent behavior being measured.