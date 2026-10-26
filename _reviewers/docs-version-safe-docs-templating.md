---
title: Version-safe Docs Templating
description: 'Ensure documentation that uses Liquid/templating renders correctly across
  all supported doc versions and doesn’t break code samples.


  Apply these rules when authoring or updating docs:'
repository: github/docs
label: Documentation
language: Markdown
comments_count: 8
repository_stars: 21111
---

Ensure documentation that uses Liquid/templating renders correctly across all supported doc versions and doesn’t break code samples.

Apply these rules when authoring or updating docs:
- Use `ifversion`/product variables so text and tables match the target platform(s) (for example, FPT vs GHEC), instead of hardcoding one variant.
- Keep Markdown structure valid so UI elements render as intended (for example, add required blank lines before headings).
- Escape templating tokens inside code blocks so the docs build/linter doesn’t interpret them as Liquid. For GitHub Actions examples, wrap `${{ ... }}` content in `{% raw %}...{% endraw %}`.

Example (escaping `${{ ... }}` in a workflow YAML code block):
```markdown
```yaml
key: {% raw %}${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}{% endraw %}
```
```

This reduces broken previews/builds, avoids inconsistent multi-version content, and prevents readers from seeing incorrect or truncated code samples.