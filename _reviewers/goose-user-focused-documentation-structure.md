---
title: User-focused documentation structure
description: Documentation should prioritize user needs and problems over technical
  implementation details. Start with the "why" - what problem does this solve and
  when would users need it? Provide clear use cases and benefits before diving into
  technical specifics.
repository: block/goose
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 19037
---

Documentation should prioritize user needs and problems over technical implementation details. Start with the "why" - what problem does this solve and when would users need it? Provide clear use cases and benefits before diving into technical specifics.

Structure documentation to guide users through their journey:
1. **Problem statement**: What user problem does this solve?
2. **Use cases**: When would someone use this feature?
3. **Simple examples**: Basic usage with expected outcomes
4. **Benefits**: What can users accomplish after following the guide?
5. **Platform-specific details**: Clearly distinguish between UI and CLI instructions

Move implementation details, technical architecture, and contributing guidelines to separate technical documentation when they don't directly serve user goals.

Example structure:
```markdown
# Feature Name

## What problem does this solve?
Help users understand when they need this feature...

## Use cases
- Run this when you want to...
- Use this for...

## Quick start
Simple example with expected output...

## Benefits
What you can accomplish after setup...
```

Avoid documentation that "reads more like internal technical documentation than a user guide" by consistently asking: "Does this help users accomplish their goals?"