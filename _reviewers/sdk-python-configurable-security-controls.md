---
title: configurable security controls
description: Design security mechanisms with configurable behavior to handle different
  threat scenarios and use cases. Avoid rigid, one-size-fits-all security implementations
  that may not suit all deployment contexts.
repository: strands-agents/sdk-python
label: Security
language: Python
comments_count: 1
repository_stars: 4044
---

Design security mechanisms with configurable behavior to handle different threat scenarios and use cases. Avoid rigid, one-size-fits-all security implementations that may not suit all deployment contexts.

Security controls should provide configuration options that allow teams to adjust behavior based on their specific threat model. For example, a content filtering system might need different redaction strategies - sometimes redacting only the violating content, other times redacting both input and output to prevent cascading security issues.

```python
# Good: Configurable security behavior
def _has_blocked_guardrail(self, guardrail_data: dict[str, Any]) -> tuple[bool, bool]:
    blocked_input = any(self._find_detected_and_blocked_policy(assessment) 
                       for assessment in input_assessment.values())
    blocked_output = any(self._find_detected_and_blocked_policy(assessment) 
                        for assessment in output_assessments.values())
    
    return blocked_input, blocked_output

# Configuration allows different redaction strategies:
# - guardrail_redact_input: redact only input violations
# - guardrail_redact_output: redact only output violations  
# - Both: redact both when either triggers (prevents cascading issues)
```

This approach enables security controls to adapt to different scenarios, such as preventing assistants from echoing trigger words that could create security loops, while still allowing targeted redaction when appropriate.