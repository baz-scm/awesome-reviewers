---
title: Documentation completeness check
description: 'Ensure all documentation is complete, well-formatted, and maximally
  useful for developers. This includes:


  1. **Use proper markdown syntax** for headings, lists, code blocks, and other formatting
  elements to ensure documents render correctly.'
repository: langchain-ai/langchainjs
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 15004
---

Ensure all documentation is complete, well-formatted, and maximally useful for developers. This includes:

1. **Use proper markdown syntax** for headings, lists, code blocks, and other formatting elements to ensure documents render correctly.

```markdown
# Main Heading
## Subheading
- Bullet point
- Another bullet point

## Code Example
```typescript
const example = "properly formatted";
```

2. **Include external reference links** to relevant resources when mentioning libraries, tools, or APIs so users can easily access additional information.

```markdown
Install the [Oracle JavaScript client driver](https://node-oracledb.readthedocs.io/en/latest/) to get started:

```npm install oracledb```
```

3. **Document all parameters completely** in API references and configuration tables, even those inherited from parent interfaces or less commonly used options.

```markdown
| Parameter | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| `timeout` | number | 60000 | Timeout in milliseconds for the tool call |
| `signal`  | AbortSignal | `undefined` | Optional AbortSignal to cancel the tool call |
```

Complete documentation improves developer experience, reduces questions, and facilitates faster onboarding.
