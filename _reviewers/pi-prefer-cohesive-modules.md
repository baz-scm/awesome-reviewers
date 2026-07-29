---
title: Prefer cohesive modules
description: 'Keep the repository’s module structure and implementations cohesive
  and non-redundant.


  Apply these rules:

  - **Don’t add “single-purpose” files for trivial helpers**: if a function belongs
  next to its call site (or in an existing utility module), move it there instead
  of creating a standalone file.'
repository: earendil-works/pi
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 79783
---

Keep the repository’s module structure and implementations cohesive and non-redundant.

Apply these rules:
- **Don’t add “single-purpose” files for trivial helpers**: if a function belongs next to its call site (or in an existing utility module), move it there instead of creating a standalone file.
- **Avoid unnecessary folder/index boilerplate**: don’t introduce `core/skills/` with only an `index.ts`/`types.ts` that add no navigation or separation value; keep the public surface where it’s simplest.
- **Organize by responsibility**: group related implementations (e.g., image/provider implementations) into dedicated subfolders so readers can find “like with like”.
- **Dedupe identical logic**: when two loaders/parsers differ only by a small input (e.g., `source`), extract a single shared implementation and parameterize the difference.
- **Follow import style constraints**: avoid dynamic imports unless there is a specific, justified requirement.

Example (dedupe loaders by parameterizing the difference):
```ts
function loadSkillsFromDir(dir: string, source: SkillSource): Skill[] {
  // shared parsing + file scanning logic here
}

// instead of two nearly identical functions
const piSkills = loadSkillsFromDir(piDir, "pi");
const claudeSkills = loadSkillsFromDir(claudeDir, "claude");
```