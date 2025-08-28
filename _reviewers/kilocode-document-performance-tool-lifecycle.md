---
title: Document performance tool lifecycle
description: When creating performance optimization tools, especially temporary dev-only
  utilities, clearly document their purpose, scope, and removal criteria in the README
  or documentation. This helps teams make informed decisions about maintenance vs.
  performance benefits over time.
repository: kilo-org/kilocode
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 7302
---

When creating performance optimization tools, especially temporary dev-only utilities, clearly document their purpose, scope, and removal criteria in the README or documentation. This helps teams make informed decisions about maintenance vs. performance benefits over time.

Include these key elements:
- Mark dev-only tools explicitly (e.g., "**Internal dev tool only:**")
- State the performance problem being solved
- Define clear criteria for when the tool should be removed
- Acknowledge the temporary nature of the optimization

Example documentation:
```markdown
# Translation MCP Server

**Kilocode internal dev tool only:** This is a performance optimization to reduce LLM waiting time during translation tasks. Can be deleted when maintenance burden outweighs time saved.
```

This approach prevents performance tools from becoming technical debt by establishing upfront expectations about their lifecycle and making it easier for future developers to evaluate whether the optimization is still worthwhile.