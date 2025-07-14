---
title: Format docs for readability
description: 'Documentation should follow consistent formatting and structural patterns
  to maximize readability and maintainability. Key guidelines:


  1. Keep line lengths to 80 characters maximum'
repository: nodejs/node
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 112178
---

Documentation should follow consistent formatting and structural patterns to maximize readability and maintainability. Key guidelines:

1. Keep line lengths to 80 characters maximum
2. Place all document links at the bottom of the file and use in-doc references
3. Document default behaviors before introducing exceptions
4. Use proper spacing and indentation for examples and code blocks

Example of proper documentation formatting:

```markdown
# Feature Name

Default behavior description first, followed by any exceptions or special cases.

## Usage

```js
// Code example with proper indentation
const example = require('node:example');
example.doSomething();
```

## Options

* `option1` {string} Description fits within 80 chars, continues on next
  line with proper indentation.
* `option2` {Object} Another option description.

[link-reference]: #section-name
```

This format ensures consistency across documentation and makes it easier for users to find and understand information.