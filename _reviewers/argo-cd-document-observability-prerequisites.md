---
title: Document observability prerequisites
description: When documenting observability features such as metrics, debugging capabilities,
  or monitoring tools, always include clear information about their prerequisites,
  enabling conditions, and limitations. This ensures developers understand when these
  features are available and how to access them.
repository: argoproj/argo-cd
label: Observability
language: Markdown
comments_count: 2
repository_stars: 20149
---

When documenting observability features such as metrics, debugging capabilities, or monitoring tools, always include clear information about their prerequisites, enabling conditions, and limitations. This ensures developers understand when these features are available and how to access them.

For metrics, specify any configuration flags or settings required:
```markdown
| `argocd_github_api_requests_total` | counter | Number of Github API calls. |

> **Note**: All `argocd_github_api` metrics are only enabled when the corresponding feature flag is configured.
```

For debugging features, document the conditions that affect their availability:
```markdown
## Debugging Options
- **IDE debugging**: Requires running components separately with proper build configuration
- **Process attachment**: Works with normally built binaries but not with `go run` processes (no debug symbols)
```

This practice prevents confusion and helps developers choose the appropriate observability approach for their specific setup and requirements.