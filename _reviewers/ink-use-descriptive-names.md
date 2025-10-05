---
title: Use descriptive names
description: Choose variable, function, and export names that clearly communicate
  their purpose and content. Avoid abbreviations and ambiguous terms that could mislead
  other developers about what the identifier represents.
repository: vadimdemedes/ink
label: Naming Conventions
language: JavaScript
comments_count: 3
repository_stars: 31825
---

Choose variable, function, and export names that clearly communicate their purpose and content. Avoid abbreviations and ambiguous terms that could mislead other developers about what the identifier represents.

Key principles:
- Variable names should accurately reflect what they contain, not just their general category
- Avoid abbreviations when full words improve clarity (e.g., `previousCounter` instead of `prevCounter`)
- Export names should be specific enough to understand their purpose (e.g., `ProgressBar` instead of `Bar`)

Example of unclear naming:
```javascript
const subProcess = childProcess.spawn('ping', ['8.8.8.8']).stdout;
// Misleading: subProcess actually contains stdout, not the process

exports.Bar = Bar; // Too ambiguous
```

Example of clear naming:
```javascript
const subProcess = childProcess.spawn('ping', ['8.8.8.8']);
const stdout = subProcess.stdout;
// Clear: each variable accurately represents what it contains

exports.ProgressBar = ProgressBar; // Specific and clear
```

This practice prevents confusion during code reviews and maintenance, making the codebase more self-documenting and easier to understand.