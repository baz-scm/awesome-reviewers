---
title: Separate AI instructions
description: Always separate AI model instructions from user input to prevent prompt
  injection vulnerabilities and maintain clear architectural boundaries. Use system
  messages for AI instructions and user messages for actual user content, rather than
  embedding user input directly into instruction templates.
repository: langgenius/dify
label: AI
language: Python
comments_count: 2
repository_stars: 114231
---

Always separate AI model instructions from user input to prevent prompt injection vulnerabilities and maintain clear architectural boundaries. Use system messages for AI instructions and user messages for actual user content, rather than embedding user input directly into instruction templates.

This approach provides two key benefits:
1. **Security**: Prevents prompt injection attacks where malicious user input could override or manipulate the AI's instructions
2. **Clarity**: Maintains clear separation of concerns between what the AI should do (instructions) and what data it should process (user input)

Example of the recommended approach:
```python
# Good: Separate system instructions from user input
prompt_messages = [
    SystemPromptMessage(content="Generate JSON output following this schema: {...}"),
    UserPromptMessage(content=user_provided_content)
]

# Avoid: Embedding user input in instructions
prompt_template = "Generate JSON for: {user_input}"  # Vulnerable to injection
```

Be particularly careful when implementing structured output features, as system prompts may be modified or discarded depending on the model's native capabilities. Always validate that the intended instruction-user separation is preserved throughout the processing pipeline.