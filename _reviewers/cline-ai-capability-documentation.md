---
title: AI capability documentation
description: When documenting AI systems, models, or assistants, ensure technical
  terminology is precise and capabilities are clearly scoped. Use consistent language
  to describe what the AI can and cannot do, avoiding vague or overstated claims.
  For AI agents or assistants, explicitly detail their tools, permissions, and limitations.
repository: cline/cline
label: AI
language: Markdown
comments_count: 2
repository_stars: 48299
---

When documenting AI systems, models, or assistants, ensure technical terminology is precise and capabilities are clearly scoped. Use consistent language to describe what the AI can and cannot do, avoiding vague or overstated claims. For AI agents or assistants, explicitly detail their tools, permissions, and limitations.

For example, instead of vague descriptions like "AI helper that can code," use specific language:
```markdown
# Clear AI Capability Documentation
Powered by Claude 3.7 Sonnet's agentic coding capabilities, this AI assistant can:
- Create and edit files with linter/compiler error monitoring
- Execute terminal commands (with user authorization)  
- Browse projects and analyze code structure via AST parsing
- Use headless browser for web development tasks

Limitations: Requires human approval for each file change and terminal command.
```

This approach helps users understand exactly what to expect from AI tools and prevents misaligned expectations. When localizing AI documentation, maintain technical accuracy while adapting language for cultural context. Consistent terminology across all documentation languages ensures users have the same understanding regardless of their preferred language.