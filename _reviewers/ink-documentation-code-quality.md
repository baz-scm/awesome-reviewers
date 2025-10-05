---
title: Documentation code quality
description: Ensure documentation code blocks use appropriate syntax highlighting
  and provide comprehensive, functional examples. For shell commands in markdown,
  use `sh` syntax highlighting rather than `console` for better highlighting accuracy
  and copy functionality. When documenting APIs or components, provide multiple complete
  examples that demonstrate different...
repository: vadimdemedes/ink
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 31825
---

Ensure documentation code blocks use appropriate syntax highlighting and provide comprehensive, functional examples. For shell commands in markdown, use `sh` syntax highlighting rather than `console` for better highlighting accuracy and copy functionality. When documenting APIs or components, provide multiple complete examples that demonstrate different usage patterns rather than incomplete snippets.

Example of proper shell command formatting:
```sh
$ npm install ink@next react
```

Example of comprehensive API documentation:
```jsx
import { Text } from "ink"

// Basic usage
<Text color="red">Error message</Text>

// Background color
<Text bgRed>Alert</Text>

// RGB colors
<Text rgb={[255, 255, 255]}>Custom color</Text>
```

This approach improves code readability in documentation and helps developers understand the full scope of available options through practical, working examples.