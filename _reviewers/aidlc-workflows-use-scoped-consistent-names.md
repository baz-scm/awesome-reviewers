---
title: Use scoped, consistent names
description: 'When naming identifiers (results, commands, spaces) in shared systems,
  make names **unambiguous, consistent, and context-aware**.


  Apply these rules:

  1) **Qualify by namespace/scope to avoid collisions**'
repository: awslabs/aidlc-workflows
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 3849
---

When naming identifiers (results, commands, spaces) in shared systems, make names **unambiguous, consistent, and context-aware**.

Apply these rules:
1) **Qualify by namespace/scope to avoid collisions**
- Don’t key metadata/result files by a bare basename when multiple owners can supply the same filename.
- Prefer a qualified name that includes the owner (e.g., plugin dir) and the stem.

Example (pattern):
```ts
// BAD: collisions if multiple plugins ship the same file basename
const base = basename(file); // e.g. plugin.test.ts
const resultName = base.replace(/\.test\.ts$/, '');

// GOOD: qualify with plugin directory + stem
const plugin = dirnameRelativeToPluginsRoot(file); // e.g. "test-pro"
const stem = basename(file).replace(/\.test\.ts$/, '');
const resultName = `plugin-${plugin}-${stem}`;
```

2) **Keep command/name tokens identical across integrations**
- If a shared directive says ` /aidlc `, every harness skill should accept/emit the same command token (e.g., Codex using `$aidlc` must be represented consistently wherever the directive is consumed).
- Treat command strings as part of your naming contract: update *all* harness-specific variants together.

3) **Validate reserved/semantic tokens before normalization**
- If an input is semantically meaningful (`-h`, `help`) and you transform it (e.g., `slugify`), check the **raw** value first.

Example (pattern):
```ts
function handleCreateSpace(raw: string) {
  if (raw === "-h" || raw === "help") {
    die("Did you mean /aidlc --help? To create a space, pass a name.");
  }
  const name = slugify(raw);
  // ...rest
}
```

Net effect: no accidental overwrites/masking, fewer integration regressions, and reserved semantics can’t slip through via normalization edge cases.