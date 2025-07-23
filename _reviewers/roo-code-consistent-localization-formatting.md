---
title: Consistent localization formatting
description: 'Ensure all localization strings maintain consistent formatting patterns
  within each locale file. This includes:


  1. **Terminal punctuation**: All similar messages should consistently end with appropriate
  punctuation marks for the locale (periods in English/French, "।" in Hindi, etc.).'
repository: RooCodeInc/Roo-Code
label: Code Style
language: Json
comments_count: 7
repository_stars: 17288
---

Ensure all localization strings maintain consistent formatting patterns within each locale file. This includes:

1. **Terminal punctuation**: All similar messages should consistently end with appropriate punctuation marks for the locale (periods in English/French, "।" in Hindi, etc.).

2. **Locale-specific punctuation**: Use the correct width/style of punctuation marks for each language (e.g., full-width colons "：" in Chinese and Japanese, not ASCII colons ":").

3. **Variable interpolation syntax**: Maintain consistent variable placeholder syntax. Use double curly braces for all variables: `{{variableName}}` not `{variableName}`.

Example (incorrect):
```json
{
  "errors": {
    "invalidApiKey": "Invalid API key. Please check your API key configuration.",
    "apiKeyRequired": "An API key is required for this embedder",
    "vectorDimensionMismatch": "Failed to update vector index. Details: {errorMessage}"
  }
}
```

Example (correct):
```json
{
  "errors": {
    "invalidApiKey": "Invalid API key. Please check your API key configuration.",
    "apiKeyRequired": "An API key is required for this embedder.",
    "vectorDimensionMismatch": "Failed to update vector index. Details: {{errorMessage}}"
  }
}
```

Consistent formatting makes localization files more maintainable and ensures a uniform appearance throughout the application.