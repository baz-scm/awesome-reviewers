---
title: Prefer clear, semantic code
description: 'Write code that’s easy to read and matches intent (mutability, string
  composition, UI semantics), and remove obvious clutter.


  Apply these rules:


  1) Avoid reassignable variables'
repository: freeCodeCamp/freeCodeCamp
label: Code Style
language: TSX
comments_count: 6
repository_stars: 444449
---

Write code that’s easy to read and matches intent (mutability, string composition, UI semantics), and remove obvious clutter.

Apply these rules:

1) Avoid reassignable variables
- Prefer `const` when a value isn’t reassigned.
```ts
const repository = curriculumLocale === 'english'
  ? 'freeCodeCamp'
  : 'i18n-curriculum';
```

2) Build static paths/strings directly
- For URL/path-like strings made of known segments, prefer array joining (or a single template literal) over nested `join(...)`/extra indirection.
```ts
const challengesFolder = ['blob', 'main', 'curriculum', 'challenges'].join('/');
const gitPath = [repository, challengesFolder, curriculumLocale, 'blocks', block, `${challengeId}.md'].join('/');
gitURL.pathname = gitURL.pathname + gitPath;
```

3) Don’t add redundant conditionals when UI state already guarantees behavior
- If a control is `disabled`, the handler usually doesn’t need guarding.
```tsx
<Button disabled={isClassroomAccount} onClick={updateIsClassroomAccount} />
```

4) Render links as links; actions as buttons
- If the user is navigating to/copying/opening a URL, use a link element/component. Avoid “button that opens a new tab” when a link is available—this improves accessibility and expected browser features.

5) Remove duplicate/unused imports
- Keep imports unique and ensure every import is used (e.g., don’t import the same symbol in multiple places).