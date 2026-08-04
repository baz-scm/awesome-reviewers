---
title: Avoid brittle AI heuristics
description: 'When building agent evaluation and agent runtime logic, avoid ad-hoc,
  brittle inference from unstructured strings or hardcoded scenario lists. Instead:'
repository: awslabs/agentcore-samples
label: AI
language: Python
comments_count: 2
repository_stars: 3244
---

When building agent evaluation and agent runtime logic, avoid ad-hoc, brittle inference from unstructured strings or hardcoded scenario lists. Instead:
- For evaluation, store scenario/ground-truth items in a managed, predefined dataset format (so runs are consistent, shareable, and tooling-compatible).
- For agent intent/features selection, don’t infer options via brittle parsing (e.g., URL substring checks). Prefer explicit user selection, or use a dedicated intent/classification step (LLM or classifier) with a well-defined output schema.

Example (replace URL substring detection with explicit user selection):
```python
# Bad: brittle heuristic
# if "pricing" in url.lower() or "price" in url.lower(): ...

# Good: explicit selection (or use model classification separately)
console.print("Enter categories to analyze:")
choices = ["pricing", "features", "models", "regions", "apis"]
selected = []
for c in choices:
    if Confirm.ask(f"Analyze {c}?", default=False):
        selected.append(c)

# selected now drives analysis deterministically
```

Implementation checklist:
- Move evaluation scenario definitions + expected outputs into AgentCore dataset management.
- Replace heuristic slot-detection with explicit selections or a separate intent step that returns structured, validated fields.
- Add tests that cover representative inputs to prevent silent regressions in AI behavior.