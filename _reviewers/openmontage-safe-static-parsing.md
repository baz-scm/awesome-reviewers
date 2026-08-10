---
title: Safe Static Parsing
description: When parsing configuration or design-token files from external/untrusted
  sources, never execute their contents as part of scanning. Default to static, deterministic
  extraction and “fail closed” (e.g., return `null`/empty) when the config requires
  evaluation.
repository: calesthio/OpenMontage
label: Security
language: Python
comments_count: 1
repository_stars: 46544
---

When parsing configuration or design-token files from external/untrusted sources, never execute their contents as part of scanning. Default to static, deterministic extraction and “fail closed” (e.g., return `null`/empty) when the config requires evaluation.

Apply this pattern:
- **Default non-execution:** Use static parsing (e.g., balanced-brace/quote-aware extraction of literals) instead of `require`, `import`, function/arrow evaluation, template literals, spreads, or any construct that implies runtime behavior.
- **Deny dynamic constructs:** If the parser encounters unsafe indicators (like `require(`, `import(`, `=>`, `function`, template literals, `process.`, `new`, etc.), disqualify and return “unknown” rather than guessing.
- **Require explicit opt-in for execution:** If execution is unavoidable, gate it behind an `allow_*_execution` flag that is **off by default**, clearly documented as dangerous, and tracked in metadata/warnings.
- **Prove with tests:** Add tests that assert the execution path (e.g., `subprocess.run`, `node`) is never called in the default path.

Example shape (self-contained):
```python
def parse_tailwind_config(path: str, allow_config_execution: bool = False):
    text = open(path, 'r', encoding='utf-8', errors='replace').read()

    # Fail-closed on dynamic constructs
    unsafe_markers = [
        'require(', 'import(', '=>', 'function', 'new ', 'process.',
        '`', '{...', '...'
    ]
    if any(m in text for m in unsafe_markers):
        if not allow_config_execution:
            return None  # refuse
        # If opt-in is enabled, execution is explicit and auditable.
        # (Keep this codepath tightly scoped and test-covered.)
        return execute_config_safely(path)

    # Otherwise extract literal theme statically (quote-aware / balanced braces)
    return extract_theme_literal_as_json(text)
```
This prevents supply-chain style attacks where a config triggers arbitrary code execution during analysis, aligning scanning tools with security best practices.