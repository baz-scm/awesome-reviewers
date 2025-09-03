---
title: Optimize AI interactions
description: When working with AI models and LLMs, optimize both prompts and input
  data to improve model performance and reduce token usage. For prompts, be specific
  about the AI's role, requirements, and expected output format rather than using
  vague instructions. For input data, preprocess and clean content to remove unnecessary
  elements that could confuse the model...
repository: ChatGPTBox-dev/chatGPTBox
label: AI
language: Other
comments_count: 2
repository_stars: 10660
---

When working with AI models and LLMs, optimize both prompts and input data to improve model performance and reduce token usage. For prompts, be specific about the AI's role, requirements, and expected output format rather than using vague instructions. For input data, preprocess and clean content to remove unnecessary elements that could confuse the model or waste tokens.

Example of improved prompt specificity:
```javascript
// Instead of vague prompts:
const prompt = `Translate the following into ${language} and only show me the translated content`

// Use specific, role-based prompts:
const prompt = `You are a professional translator. Translate the following text into ${language}, preserving meaning, tone, and formatting. Only provide the translated result.`
```

Example of input data cleaning:
```javascript
// Clean subtitle data before sending to AI
subtitleContent = replaceHtmlEntities(subtitleContent.replace(",", " "))
```

This approach reduces confusion, improves output quality, and optimizes token usage when interacting with AI models.