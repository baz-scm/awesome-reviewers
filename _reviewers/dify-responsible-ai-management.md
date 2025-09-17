---
title: Responsible AI management
description: Ensure AI models are managed responsibly throughout their lifecycle and
  have appropriate boundaries on their decision-making authority. When deprecating
  AI models, maintain backward compatibility by marking old models as deprecated rather
  than removing them entirely. Additionally, prevent AI models from controlling sensitive
  parameters that could lead to...
repository: langgenius/dify
label: AI
language: Yaml
comments_count: 2
repository_stars: 114231
---

Ensure AI models are managed responsibly throughout their lifecycle and have appropriate boundaries on their decision-making authority. When deprecating AI models, maintain backward compatibility by marking old models as deprecated rather than removing them entirely. Additionally, prevent AI models from controlling sensitive parameters that could lead to security risks or unintended consequences.

For model deprecation, create new model files while preserving old ones:
```yaml
# Old model file: cohere.command-r-16k.yaml
model: cohere.command-r-16k
deprecated: true

# New model file: cohere.command-r-08-2024.yaml  
model: cohere.command-r-08-2024
```

For tool parameters, ensure AI models don't control sensitive values:
```yaml
# Dangerous - AI decides the key
parameters:
  - name: key
    form: llm

# Safe - User provides the key
parameters:
  - name: key
    form: form
```

This approach prevents breaking existing configurations while maintaining security boundaries around AI decision-making capabilities.