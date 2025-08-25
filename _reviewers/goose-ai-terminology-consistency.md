---
title: AI terminology consistency
description: Maintain consistent terminology when describing AI systems, capabilities,
  and workflows throughout documentation and content. This includes using standardized
  terms for AI entities (consistently choosing between "AI", "assistant", "model",
  or "agent"), technical processes, and capability descriptions.
repository: block/goose
label: AI
language: Markdown
comments_count: 4
repository_stars: 19037
---

Maintain consistent terminology when describing AI systems, capabilities, and workflows throughout documentation and content. This includes using standardized terms for AI entities (consistently choosing between "AI", "assistant", "model", or "agent"), technical processes, and capability descriptions.

Key areas to standardize:
- **AI entity references**: Choose consistent terms like "assistant" rather than mixing "AI", "model", and "agent" within the same context
- **Technical processes**: Use precise terminology like "spawn subagents" instead of "span subagents"  
- **Capability descriptions**: Consistently describe what AI systems are "designed for" vs "not designed for"

Example of inconsistent terminology:
```markdown
The AI can help with data analysis. The model explores data through execution. 
The assistant understands and builds upon existing state.
```

Example of consistent terminology:
```markdown
The assistant can help with data analysis. The assistant explores data through execution.
The assistant understands and builds upon existing state.
```

This consistency helps readers better understand AI system capabilities and creates more professional, trustworthy documentation. It's particularly important when describing AI workflows, limitations, and collaborative processes between humans and AI systems.