---
title: Consistent module organization
description: 'Keep code organized by responsibility and centralize reusable logic.
  Concretely:


  - Centralize helpers: move shared implementations (plugin loading, dataset parsing,
  prompt helpers, is_notebook, prompt wrappers, etc.) into a single utils or plugin
  package and import them from one place. Avoid copy-pasting variations of the same
  logic across files — this...'
repository: p-e-w/heretic
label: Code Style
language: Python
comments_count: 16
repository_stars: 5002
---

Keep code organized by responsibility and centralize reusable logic. Concretely:

- Centralize helpers: move shared implementations (plugin loading, dataset parsing, prompt helpers, is_notebook, prompt wrappers, etc.) into a single utils or plugin package and import them from one place. Avoid copy-pasting variations of the same logic across files — this prevents drift, duplicate bugs, and inconsistent behavior (see plugin loaders and load_prompts). Example consolidation: replace duplicated _load_tagger_plugin/_load_scorer_plugin logic with a single load_plugin utility used by Evaluator.

  Example pattern:
  - utils.load_plugin(name: str, base_cls: type) -> type | instance
  - utils.load_prompts(spec: DatasetSpecification) -> list[str]
  - utils.prompt_select/text/password(...) that handle notebook vs terminal and are the single source of truth for user interaction

- Enforce separation of concerns: keep UI and interaction code in the CLI layer (main.py); core classes (Model, Evaluator, Scorer) should expose well-typed methods and not prompt the user or perform I/O. If an operation needs user input, prompt in main then call a Model/Evaluator method with the chosen parameters (e.g., prompt in main, then call model.get_merged_model(strategy)).

- Preserve strong typing and clear APIs when refactoring: keep explicit attributes and return types on public classes (avoid silently removing typed fields or returning ambiguous types). Use pydantic/BaseModel types for plugin settings and declare function return types so static checkers catch regressions.

- Reduce duplication and improve resource handling: reuse existing computations (e.g., max_memory), consolidate is_notebook implementations, and avoid relying on del for cleanup — use context managers or explicit close/unlink behavior.

- Small style rules that follow from organization: place imports at the top of modules, prefer named arguments (e.g., dim=...), remove unused imports, and use single authoritative helper functions rather than many inline special cases.

How to apply:
1. Audit the codebase for duplicates of plugin loading, prompt handling, and dataset parsing; create single utilities and adjust callers to import them.
2. Move all prompt/text/password/select calls to a utils.prompt_* module and ensure main.py uses those helpers; domain objects must accept parameters rather than interact with users.
3. When extracting code, carry over type annotations and return types; add or preserve unit tests for behavior that was previously duplicated.
4. Replace flag-heavy control flow with clearer branching or loops and prefer context managers for resource lifecycle.

Benefits: improved readability, fewer subtle behavioral regressions, simpler testing, and stronger static typing — all aligning with code style and maintainability goals.