---
title: Naming convention alignment
description: When adding/adjusting commands, options, helpers, or telemetry, ensure
  names are (1) semantically accurate and (2) consistent with existing CLI/module
  conventions.
repository: Azure/azure-cli
label: Naming Conventions
language: Python
comments_count: 9
repository_stars: 4592
---

When adding/adjusting commands, options, helpers, or telemetry, ensure names are (1) semantically accurate and (2) consistent with existing CLI/module conventions.

Practical rules:
1. **Follow established flag/parameter patterns**: reuse the same flag names and option/short-name conventions used by similar existing commands.
   - Prefer the established pair for a concept (e.g., `--registry/-r` vs introducing `--name/-n` for the same “registry_name” concept).
2. **Keep helper/function names truthful**: if logic supports more than the original scope, rename to remove ambiguity.
   - Example: if `get_docker_command()` can return Podman too, rename to something like `get_container_runtime_command()` (or similar).
3. **Standardize command/group identifiers (including casing)**: ensure top-level command strings and registered group names match the module/UI naming expectations and are handled consistently (e.g., avoid case-sensitive behavior affecting module resolution).
4. **Use names that match responsibility**: if you split behavior (e.g., validate image name vs validate image layers), name the functions to reflect what each does.
5. **Preserve intended semantics for “private”/name-mangled access**: when calling name-mangled private methods, use the correct form so refactors don’t silently break behavior.

Example checklist for a change:
- If the change adds a new CLI option for an existing concept, search for other commands that already expose that concept; copy their flag naming style.
- If you broaden a helper’s behavior (Docker→Podman), rename the helper and update all call sites.
- If you alter command routing/registration, verify the exact command/group names and casing match the loader/UI expectations.