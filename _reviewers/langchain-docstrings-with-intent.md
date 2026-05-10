---
title: Docstrings With Intent
description: 'Adopt a single documentation standard: every docstring/comment should
  (1) explain intent and observable behavior, (2) make responsibility/ownership explicit,
  (3) be traceable when tied to external or non-obvious defaults, (4) be safe when
  examples could do harm, and (5) follow established docstring conventions without
  duplicating type annotations.'
repository: langchain-ai/langchain
label: Documentation
language: Python
comments_count: 15
repository_stars: 136312
---

Adopt a single documentation standard: every docstring/comment should (1) explain intent and observable behavior, (2) make responsibility/ownership explicit, (3) be traceable when tied to external or non-obvious defaults, (4) be safe when examples could do harm, and (5) follow established docstring conventions without duplicating type annotations.

Practical rules
- Traceability: If behavior depends on a provider default/version, include a short comment with a stable link (and what to monitor) rather than leaving it implicit.
- Ownership/responsibility: For each field/option, document what the system/provider sets, what LangChain standardizes, and whether users are allowed to mutate it.
- Behavior over names: When option names like “ignore”/“response” or “reasoning” are non-obvious, document the exact semantics and data shape (including sync vs async expectations when relevant).
- Actionability: For runtime errors, tell users exactly what to change (and mention relevant handlers/paths like sync/async) to resolve the issue.
- Examples with caveats: For tool/execution examples, add clear warnings (and prefer safer examples). Avoid “copy/paste and run” without guardrails.
- Conventions + consistency: Don’t restate type information in docstrings when type annotations already exist; follow the repo’s docstring sections/format for Args/Example.
- Edge cases: If a field allows multiple types (e.g., `int | str`) or has special handling, document why and when the special case occurs.

Example pattern
```python
def _gpt5_defaults_to_no_reasoning(model: str) -> bool:
    """Return True if a gpt-5 variant defaults to reasoning_effort='none'.

    Notes:
        Source: See OpenAI GPT-5.2 Prompting Guide and GPT-5.2 model docs.
        If OpenAI changes these defaults, update this helper and add a regression test.

    Args:
        model: Model identifier (e.g., 'gpt-5.2', 'gpt-5.2-pro').

    Returns:
        True when the model defaults to no reasoning.
    """
    ...
```

Applying this standard will make docs easier to maintain, reduce user confusion, and prevent unsafe or misleading copy/paste behavior.