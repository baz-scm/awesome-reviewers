---
title: Correct Matching And Parsing
description: 'When writing installers/transformers/validators that search, rewrite,
  or regenerate files, require *matching/parsing correctness*: only operate on the
  exact structure you intend, and avoid ambiguous substring/position matches.'
repository: bmad-code-org/bmad-method
label: Algorithms
language: JavaScript
comments_count: 6
repository_stars: 51859
---

When writing installers/transformers/validators that search, rewrite, or regenerate files, require *matching/parsing correctness*: only operate on the exact structure you intend, and avoid ambiguous substring/position matches.

Practical rules:
- Prefer structured, schema-aware parsing (e.g., header-based CSV parsing) over positional splitting.
- For path logic, use boundary-safe matching (e.g., match `folder + "/"` rather than a raw substring) and validate dot-segments (`.`/`..`) explicitly.
- For text rewrites, match the target syntax (e.g., Markdown link destinations) using regex, not raw substring replacement.
- For filesystem scans, anchor derived relative paths to the original scan root (pass `rootDir` through recursive scanners).
- For guard/validation tests, use filename-aware patterns to prevent collisions (`workflow.xml` vs `validate-workflow.xml`).

Example pattern (transform guards + boundary-safe matching):
```js
// 1) Boundary-safe path insertion
const folder = output_folder.replace(/[\\/]+$/, '');
for (const key of ['planning_artifacts', 'implementation_artifacts']) {
  if (finalConfig[key]?.includes(folder + '/')) {
    finalConfig[key] = finalConfig[key].replace(folder, `${folder}/${scope}`);
  }
}

// 2) Syntax-scoped rewrite (Markdown link destinations)
const mdLinkRegex = /\]\((?:\.\/)?workflow\.md\)/g;
content = content.replaceAll(mdLinkRegex, `]({project-root}/${relPath}/workflow.md)`);

// 3) Filename-aware guard
const forbiddenRegex = /(^|\/|\\)workflow\.xml(\b|$)/;
if (forbiddenRegex.test(content)) offenders.push(path.relative(projectRoot, fullPath));
```

Outcome: fewer false positives/negatives, safer regeneration (don’t overwrite user edits unless the generator-shaped pattern matches), and transformations that remain correct as content and directory structure evolve.