---
title: Validate and Scope Cache
description: 'When using cached data/artifacts, treat the cache as ephemeral and potentially
  stale/corrupt. Apply three rules:


  1) Make cache scope explicit (and CI-safe)'
repository: bmad-code-org/bmad-method
label: Caching
language: Markdown
comments_count: 3
repository_stars: 51859
---

When using cached data/artifacts, treat the cache as ephemeral and potentially stale/corrupt. Apply three rules:

1) Make cache scope explicit (and CI-safe)
- Document what environments populate the cache (e.g., per-machine) and what clears it (e.g., fresh checkout/ephemeral CI). If a CLI option lists “available keys,” ensure users know it reflects cached state, not global state.

2) Validate before trusting
- If a cached artifact exists, verify it is usable before loading.
- Minimum checks: file exists, is non-empty, and matches an expected shape/version marker (e.g., a required header or schema prefix).

3) Fall back deterministically
- If validation fails, do not proceed with cached content. Regenerate/recompile from source (and optionally confirm the regenerated output exists and is non-empty).

Example pattern (epic context cache)
```bash
# Pseudocode/steps
if cache_file_exists(epic_N_context) then
  content = read(cache_file)
  if content is empty OR not content.startswith("# Epic <N> Context") then
    delete/ignore cache
    compiled = compile_epic_context(N)  # deterministic recompute
    assert compiled exists and non-empty
    load(compiled)
  else
    load(cache_file)
else
  compiled = compile_epic_context(N)
  assert compiled exists and non-empty
  load(compiled)
fi
```

Also ensure you only apply these rules where the system actually caches. If something is reloaded fresh every run (e.g., prompt/step files read at execution time), don’t treat it as cached state and don’t add cache-migration guidance to it.