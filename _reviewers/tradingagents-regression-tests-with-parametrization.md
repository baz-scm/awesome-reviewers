---
title: Regression Tests With Parametrization
description: When changing business logic that affects output shape/order or resolution
  rules, add regression tests that assert observable outcomes for edge cases, and
  keep the suite maintainable by parameterizing repeated mock/assert patterns.
repository: TauricResearch/TradingAgents
label: Testing
language: Python
comments_count: 3
repository_stars: 71953
---

When changing business logic that affects output shape/order or resolution rules, add regression tests that assert observable outcomes for edge cases, and keep the suite maintainable by parameterizing repeated mock/assert patterns.

Apply it like this:
- Assert externally visible results (e.g., rendered header count, resolved fallback value), not internal implementation.
- For ordering-sensitive logic, test the exact post-processing order (e.g., ensure limiting happens after deduplication).
- For resolution logic with tricky inputs, add explicit assertions for representative edge cases (including “unknown suffix/provider” paths).
- If multiple tests share the same mocking/assertion structure, refactor into a single parameterized test (e.g., subTest) and extend coverage by adding more cases to the table.

Example pattern (parameterized warning tests):
```python
import warnings
import unittest
from unittest.mock import patch

class UnknownModelWarningTests(unittest.TestCase):
    def assert_one_user_warning(self, warning_records, provider, model):
        self.assertEqual(len(warning_records), 1)
        self.assertIs(warning_records[0].category, UserWarning)
        self.assertIn(f"Unknown {provider} model '{model}'.", str(warning_records[0].message))

    def test_unknown_model_warns(self):
        cases = [
            ("OpenAI",  "tradingagents.llm_clients.openai_client.UnifiedChatOpenAI",  "fake-openai-model"),
            ("Anthropic","tradingagents.llm_clients.anthropic_client.ChatAnthropic","fake-claude-model"),
            ("Google",  "tradingagents.llm_clients.google_client.NormalizedChatGoogleGenerativeAI", "fake-gemini-model"),
        ]

        for provider, patch_path, model in cases:
            with self.subTest(provider=provider, model=model):
                with patch(patch_path, side_effect=lambda **kwargs: kwargs):
                    with warnings.catch_warnings(record=True) as warnings_list:
                        warnings.simplefilter("always")
                        # call the provider client get_llm() here
                        llm = ...
                self.assertEqual(llm["model"], model)
                self.assert_one_user_warning(warnings_list, provider, model)
```

Also, for limit/order-sensitive behavior, ensure your test locks in the final observable output (e.g., count of headers) after all transformations, not just intermediate steps.