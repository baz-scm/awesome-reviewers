---
title: Test actual behavior
description: Tests must exercise the real implementation and verify genuine outcomes
  of the change being made, not reimplement the logic under test, duplicate coverage
  of unrelated/pre-existing utilities, or assert on trivialities that cannot fail.
  When a bug fix or feature touches specific internal methods, write tests that call
  those methods (or exercise the full...
repository: run-llama/llama_index
label: Testing
language: Python
comments_count: 8
repository_stars: 52785
---

Tests must exercise the real implementation and verify genuine outcomes of the change being made, not reimplement the logic under test, duplicate coverage of unrelated/pre-existing utilities, or assert on trivialities that cannot fail. When a bug fix or feature touches specific internal methods, write tests that call those methods (or exercise the full path, e.g. via mocks of the surrounding class) rather than re-deriving the expected result with the same algorithm used in production code — for example, call the real `_strip_thinking_tokens(text)` helper instead of re-running the same regex substitution inline in the test, and mock the surrounding `PGVectorStore` internals to test `_mmr_query`/`_prepare_mmr_query` rather than re-testing the already-covered `get_top_k_mmr_embeddings` utility. When validating that an action (e.g. a tool call) occurred, assert on its actual effect/result (e.g. by running it through `FunctionAgent` and checking tool outputs) rather than only inspecting the arguments it was called with. When a test is parametrized or covers multiple scenarios (e.g. multiple docstring styles, multiple literal-type unions, tool name/description substitution alongside literal braces), assert correctness for every case, not just the first. Finally, drop tests that only validate language/arithmetic mechanics (e.g. `assert top_k * factor == 20`) since they provide no regression value — replace them with tests that assert the actual arguments passed to the underlying call.