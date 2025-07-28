---
title: Documentation clarity standards
description: Ensure documentation is clear, precise, and technically accurate to prevent
  confusion and build errors. This includes proper escaping of special characters,
  consistent terminology, version-specific accuracy, and unambiguous language.
repository: prettier/prettier
label: Documentation
language: Markdown
comments_count: 6
repository_stars: 50772
---

Ensure documentation is clear, precise, and technically accurate to prevent confusion and build errors. This includes proper escaping of special characters, consistent terminology, version-specific accuracy, and unambiguous language.

Key practices:
- Escape HTML tags in markdown or wrap them in backticks to prevent parsing errors
- Use consistent terminology throughout (e.g., "MDX v2" not "MDX 2")
- Provide version-specific information when features or paths change between releases
- Choose precise words that reduce ambiguity (e.g., "unless specified" instead of "not specified")
- Add clarifying punctuation like quotes around file names when context could be confusing
- Define technical terms when they might be unfamiliar to readers

Example of proper escaping:
```markdown
<!-- Problematic -->
#### Handle <style> and <pre> tags in Handlebars/Glimmer

<!-- Better -->
#### Handle `<style>` and `<pre>` tags in Handlebars/Glimmer
```

Example of version-specific clarity:
```markdown
<!-- Vague -->
- ES modules: `standalone.mjs`, starting in version 2.2

<!-- Clear -->
- ES modules: `standalone.mjs`, starting in version 3.0 (In version 2, `esm/standalone.mjs`.)
```

This prevents build failures, reduces reader confusion, and maintains professional documentation standards.