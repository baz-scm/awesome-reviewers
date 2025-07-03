---
title: Structured documentation with examples
description: 'Create comprehensive documentation with clear structure and practical
  examples. Documentation should include:


  1. **Standard documentation files** like README.md, CHANGELOG.md, and CONTRIBUTING.md,
  even if they primarily link to external resources. Search engines index these standard
  files, improving project discoverability.'
repository: kubeflow/kubeflow
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 15064
---

Create comprehensive documentation with clear structure and practical examples. Documentation should include:

1. **Standard documentation files** like README.md, CHANGELOG.md, and CONTRIBUTING.md, even if they primarily link to external resources. Search engines index these standard files, improving project discoverability.

2. **Well-organized content** with clear headings, tables for related information, and consistent formatting. For complex projects, organize information hierarchically:

```markdown
# Component Name

## About
Brief description of the component's purpose.

## Table of Components
| Component | Source Repository |
|-----------|-------------------|
| Component A | [`org/repo-a`](https://github.com/org/repo-a) |
| Component B | [`org/repo-b`](https://github.com/org/repo-b) |

## Usage Examples
```

3. **Usage examples** demonstrating common tasks. For instance, when documenting test procedures:

```markdown
**Run all tests**
`make run`

**Run component-specific tests**
`make run-kfp`  # Run Kubeflow Pipelines tests
`make run-katib` # Run Katib tests
```

4. **Active voice** rather than passive voice to improve clarity and directness.

5. **Links to stable versions** rather than development branches to prevent users from accidentally using unstable code.

Following these practices makes documentation more useful, accessible, and maintainable while improving the overall user experience.
