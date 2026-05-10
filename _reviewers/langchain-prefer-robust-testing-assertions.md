---
title: Prefer Robust Testing Assertions
description: 'When adding/changing tests, optimize for (1) clear intent, (2) stability
  against refactors, and (3) determinism.


  Practical rules:

  - Assert observable behavior, not intermediate implementation details. If you need
  to validate a request payload, mock the SDK client and inspect what was actually
  sent (not private helpers/step-by-step logic).'
repository: langchain-ai/langchain
label: Testing
language: Python
comments_count: 9
repository_stars: 136312
---

When adding/changing tests, optimize for (1) clear intent, (2) stability against refactors, and (3) determinism.

Practical rules:
- Assert observable behavior, not intermediate implementation details. If you need to validate a request payload, mock the SDK client and inspect what was actually sent (not private helpers/step-by-step logic).
- Keep assertions intent-focused and resilient: use targeted field assertions rather than full object/dump equality unless the exact structure is truly contract-stable. If a full expected dict is stable/readable, compare to that dict directly.
- Ensure deterministic behavior in test inputs/expected outputs (avoid unordered `set`/`dict` conversions without sorting).
- Use fixtures (e.g., `autouse`) for repeated setup/teardown patterns like forcing a fresh module import.
- Avoid duplicating existing coverage for the same behavior; extend the existing test where the behavior is already asserted.

Example: readable, stable expectation
```py
result = convert_to_openai_function(MyModel)
assert result == {
    "name": "MyModel",
    "parameters": {"type": "object", "properties": {}, "required": []},
    "strict": True,
}
```

Example: avoid brittle intermediate-step tests (assert the actual SDK call)
```py
client = MagicMock()
# arrange llm to use mocked client
llm.invoke("hello", prompt_cache_key="k")
called_kwargs = client.create.call_args.kwargs
assert called_kwargs["prompt_cache_key"] == "k"
```

Example: fix nondeterministic ordering
```py
items = list(set(items))          # flaky
items = sorted(set(items))        # deterministic
```