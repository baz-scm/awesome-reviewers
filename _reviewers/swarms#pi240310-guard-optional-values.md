---
title: Guard optional values
description: 'Many defects in this codebase come from treating an `Optional`/nullable
  value as if it were always present: dereferencing an attribute that might not exist
  yet, indexing into a dict whose shape varies, assuming a container value is of the
  expected type, or passing a possibly-`None` string into a function that requires
  `str`. Before touching a value that is...'
repository: kyegomez/swarms#pi240310
label: Null Handling
language: Python
comments_count: 11
repository_stars: 7337
---

Many defects in this codebase come from treating an `Optional`/nullable value as if it were always present: dereferencing an attribute that might not exist yet, indexing into a dict whose shape varies, assuming a container value is of the expected type, or passing a possibly-`None` string into a function that requires `str`. Before touching a value that is typed `Optional[...]`, may be `None` by default, or may not exist on all code paths, add an explicit guard:

1. **Narrow before use.** Bind the optional value to a local variable once and check it, instead of re-reading `self.attr` (or similar) multiple times — repeated reads do not narrow under static checkers and are also vulnerable to being swapped out concurrently.
   ```python
   path = self.memory_md_path
   if path and os.path.exists(path):
       size = os.path.getsize(path)
   ```
2. **Default instead of crashing.** Use `getattr(obj, "attr", default)` / `dict.get(key, default)` when the attribute or key may be absent, especially for properties computed from nested objects that could themselves be `None` or differently shaped (e.g. summing usage across sub-agents, or checking `director.llm` before `isinstance`).
3. **Validate shape/type before operating.** Don't assume a value is a `dict`, number, or object with attribute access just because it usually is — check `isinstance(...)` before recursing into it, doing arithmetic on it, or calling `.keys()`/`.get()`. Handle both dict-shaped and attribute-shaped inputs explicitly (e.g. tool-call payloads that may be either a dict or an object) rather than silently returning `None` for the branch you didn't anticipate.
4. **Fall back to a safe default for required strings.** When an `Optional[str]` (e.g. `agent.agent_name`) must be passed where a non-`None` string is required, use `value or "fallback"` / `value or ""` rather than passing the raw optional through.
5. **Prefer explicit truthiness over `setdefault`-style presence checks** when the goal is "don't overwrite a real value" — a pre-existing empty string or `None` key still counts as "present" for `setdefault`, silently dropping the value you meant to set.
6. **Keep annotations honest.** A parameter or attribute whose default is `None` must be typed `Optional[...]`; an annotation like `metadata: Dict[str, Any] = None` is a latent bug that both misleads readers and suppresses the warnings that would otherwise catch missing guards.

Applying these patterns consistently prevents `AttributeError`/`TypeError` at runtime (including inside `finally` blocks or properties that are read unconditionally) and keeps static type checkers useful instead of noisy.</description>
</invoke>
