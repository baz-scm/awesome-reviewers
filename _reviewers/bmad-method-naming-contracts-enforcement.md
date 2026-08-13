---
title: Naming contracts enforcement
description: 'Treat IDs, artifact filenames, and command invocation strings as part
  of a naming contract: they must be deterministic for dispatch, glob matching, and
  resume/compatibility.'
repository: bmad-code-org/bmad-method
label: Naming Conventions
language: Markdown
comments_count: 5
repository_stars: 51859
---

Treat IDs, artifact filenames, and command invocation strings as part of a naming contract: they must be deterministic for dispatch, glob matching, and resume/compatibility.

Rules
1) Constrain stable identifiers
- IDs that are compared/equality-checked must be YAML strings (not numbers), always quoted.
- Use a restricted charset that’s safe in paths/globs: letters, digits, and dashes.
- Never renumber or reuse an assigned ID.

2) Preserve glob/dispatch landing targets
- If the system writes results based on a `stories/<id>-*.md` (or similar) glob, every possible outcome (including early halts) must land on a filename that still matches that glob.
- Use fixed sentinel suffixes that are inside the glob (e.g., `-unresolved`, `-ambiguous`) rather than changing the target path scheme.

3) Avoid “naive concatenation” artifact names
- Don’t derive output filenames by concatenating arbitrary user/provided names that can create double-suffixes or invalid paths (e.g., `prfaq.md-distillate.md`).
- Prefer one canonical artifact name for new flow, and an explicit legacy name only when needed for resume compatibility.

4) Use canonical invocation strings
- When routing depends on exact command phrasing, use the established form consistently (e.g., always “Invoke skill {skill-name}”). Do not mix alternative phrasings that some tools may not recognize.

Example (ID + sentinel filename)
```yaml
# stories.yaml entry
- id: "3-2"  # always quoted; letters/digits/dashes only
```
```text
# For dispatch-driven write-back, keep within stories/<id>-*.md
{spec_folder}/stories/{story_id}-unresolved.md
{spec_folder}/stories/{story_id}-ambiguous.md
{spec_folder}/stories/{story_id}-{slug}.md
```