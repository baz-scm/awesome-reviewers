---
title: Break down complex functions
description: Improve code readability and maintainability by decomposing large, complex
  functions into smaller, focused ones. When a function handles multiple responsibilities
  or becomes difficult to understand at a glance, extract logical parts into well-named
  helper functions.
repository: vitejs/vite
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 74031
---

Improve code readability and maintainability by decomposing large, complex functions into smaller, focused ones. When a function handles multiple responsibilities or becomes difficult to understand at a glance, extract logical parts into well-named helper functions.

For example, instead of a single large function like:

```ts
const getCssTagsForChunk = (chunk, toOutputPath, seen = new Set(), parentImports, circle = new Set()) => {
  const tags = [];
  if (circle.has(chunk)) return tags;
  circle.add(chunk);
  let analyzedChunkImportCss;
  const processImportedCss = (files) => {
    // 20+ lines of processing logic...
  }
  // Another 30+ lines handling imports and more processing...
  return tags;
}
```

Break it down into smaller, focused functions:

```ts
const toStyleSheetLinkTag = (file, toOutputPath) => ({
  tag: 'link',
  attrs: {
    rel: 'stylesheet',
    crossorigin: true,
    href: toOutputPath(file),
  },
});

const getCssFilesForChunk = (chunk, seenChunks = new Set(), seenCss = new Set()) => {
  // Logic to collect CSS files from chunks
}

const getCssTagsForChunk = (chunk, toOutputPath) => 
  getCssFilesForChunk(chunk).map(file => 
    toStyleSheetLinkTag(file, toOutputPath)
  );
```

This approach:
- Makes the code easier to understand and reason about
- Improves testability by isolating specific behaviors
- Allows for better reuse of functionality
- Creates a clearer separation of concerns

When refactoring complex logic, also consider extracting helper functions that handle setup tasks or conditional logic blocks to make the main function flow more obvious.