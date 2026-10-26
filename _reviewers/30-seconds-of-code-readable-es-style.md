---
title: Readable ES style
description: 'Use a consistent, readable JavaScript style that favors early exits,
  standard APIs, and lint-safe expressions—without sacrificing clarity.


  - Prefer guard clauses: if a branch returns, don’t wrap the rest in `else`.'
repository: 30-seconds/30-seconds-of-code
label: Code Style
language: Markdown
comments_count: 8
repository_stars: 129334
---

Use a consistent, readable JavaScript style that favors early exits, standard APIs, and lint-safe expressions—without sacrificing clarity.

- Prefer guard clauses: if a branch returns, don’t wrap the rest in `else`.
- Prefer portable, standard checks: e.g. use `Array.isArray(arr)` instead of `arr instanceof Array`.
- Keep expressions readable: don’t hide complex logic in inline assignments; split into clear statements when it improves understanding.
- Use concise expressions (one-liners/implicit returns) only when they remain clear; don’t force “minified” patterns.
- Avoid lint-breaking constructs (e.g., comma-operator debug tricks) and respect the project’s lint rules.
- Always declare variables (`const`/`let`) to prevent accidental globals.

Example (guard clause + standard API + clear return):
```js
const last = arr => (Array.isArray(arr) ? arr[arr.length - 1] : undefined);

const goobox = url => {
  const dropbox = /(http(s)*:\/\/)*(www\.)*(dropbox.com)/;
  const drive = /(http(s)*:\/\/)*(www\.)*(drive.google.com\/file\/d\/)/;

  if (url.match(dropbox)) {
    return url.replace(/(http(s)*:\/\/)*(www\.)*/, 'https://dl.');
  }

  if (url.match(drive)) {
    const fileId = url.replace(drive, '').match(/[\w]*\//)[0].replace(/\//, '');
    return `https://drive.google.com/uc?id=${fileId}`;
  }

  return null;
};
```