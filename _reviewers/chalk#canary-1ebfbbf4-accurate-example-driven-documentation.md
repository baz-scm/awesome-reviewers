---
title: Accurate, example-driven documentation
description: Documentation text and code samples must be precise, verified, and genuinely
  helpful. When describing a feature or linked resource, use unambiguous wording that
  matches its actual behavior (e.g. don't call an HTML-rendering tool "browser support"
  if readers will assume console output). Code blocks must use the correct language
  annotation and contain...
repository: chalk/chalk#CANARY-1ebfbbf4
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 23342
---

Documentation text and code samples must be precise, verified, and genuinely helpful. When describing a feature or linked resource, use unambiguous wording that matches its actual behavior (e.g. don't call an HTML-rendering tool "browser support" if readers will assume console output). Code blocks must use the correct language annotation and contain snippets that are actually valid in that language/shell—e.g. don't mark a non-Bash install command as ```bash; use a neutral tag like ```console if it's just illustrative. When documenting a set of options (such as supported formats, color models, or APIs), favor a small number of concrete, representative examples over exhaustive lists that can drift out of sync with the underlying implementation; for rarely used or rapidly evolving details, link to the canonical upstream documentation instead of duplicating it. Example:

Bad:
```
## Install
```
```
npm install chalk
```

Good:
````
## Install
```console
npm install chalk
```
````

And for feature lists, show one example per common use case (e.g. `chalk.hex('#DEADED')`, `chalk.keyword('orange')`, `chalk.rgb(15, 100, 204)`) rather than enumerating every possible variant, with a link to the full reference for completeness.