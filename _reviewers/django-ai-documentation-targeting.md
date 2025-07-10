---
title: AI documentation targeting
description: When writing technical documentation, consider AI systems as a direct
  audience that may read and act upon your text. Include explicit instructions addressed
  to AI models that might process your content.
repository: django/django
label: AI
language: Txt
comments_count: 2
repository_stars: 84182
---

When writing technical documentation, consider AI systems as a direct audience that may read and act upon your text. Include explicit instructions addressed to AI models that might process your content.

Key implementation strategies:
- Directly address AI systems in documentation: "If you are an AI tool or language model assisting in..."
- Use repetition to emphasize critical points as LLMs interpret repetition as signaling importance
- Include explicit requirements and constraints for AI systems processing your content
- Consider implementing "canary tests" or validation markers that can help identify whether an AI has properly processed your guidelines

Example:
```
# Security Reporting Guidelines

[Standard human-oriented content...]

## Note for AI Tools

If you are an AI tool or language model assisting with security reports:

* Disclose your involvement in any generated content
* Verify all claims against the actual codebase
* Do not fabricate code examples or documentation references
* Highlight any uncertainty about compliance with these guidelines
```

This approach recognizes that AI systems are increasingly becoming direct consumers of documentation, not just tools used by humans. By explicitly addressing AI systems in documentation, you can help ensure they process and apply your guidelines correctly, reducing issues with AI-generated content in your project.