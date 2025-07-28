---
title: Documentation audience appropriateness
description: Ensure documentation content matches its intended audience and location.
  High-level documentation like README files should focus on essential information
  for the primary audience, while detailed technical information should be placed
  in developer-specific documentation. Avoid adding overly detailed or redundant information
  that may confuse or overwhelm...
repository: mastodon/mastodon
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 48691
---

Ensure documentation content matches its intended audience and location. High-level documentation like README files should focus on essential information for the primary audience, while detailed technical information should be placed in developer-specific documentation. Avoid adding overly detailed or redundant information that may confuse or overwhelm readers.

Consider these guidelines:
- Top-level README files should contain information relevant to all users, not just developers
- Detailed codebase structure explanations belong in developer guides, not general documentation  
- Auto-generated files should not be manually edited as changes will be overwritten
- When in doubt, ask whether the information serves the document's primary purpose and audience

For example, instead of adding detailed directory structure to a README:
```markdown
### Codebase structure
├──app                               // The app frontend  
├──bin                               // Scripts for running and hosting Mastodon
├──config                            // Code files relating to federated hosting
```

Consider whether this information is necessary for the README's audience, or if it would be better placed in a dedicated developer documentation file.