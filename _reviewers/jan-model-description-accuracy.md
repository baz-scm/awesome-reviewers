---
title: model description accuracy
description: Ensure AI model descriptions are specific, capability-focused, and avoid
  marketing language or temporal references like "latest". Descriptions should clearly
  communicate what the model excels at and its intended use cases to help users make
  informed selection decisions.
repository: menloresearch/jan
label: AI
language: Json
comments_count: 4
repository_stars: 37620
---

Ensure AI model descriptions are specific, capability-focused, and avoid marketing language or temporal references like "latest". Descriptions should clearly communicate what the model excels at and its intended use cases to help users make informed selection decisions.

Replace placeholder or generic text with meaningful descriptions that highlight actual capabilities. Avoid hyperbolic statements and focus on practical information.

Example of good description:
```json
{
  "description": "Meta's Llama 3 excels at general usage situations, including chat, general world knowledge, and coding."
}
```

Instead of:
```json
{
  "description": "The latest model from MetaAI"
}
```

Be concise and pragmatic - "CodeNinja is finetuned on openchat/openchat-3.5-1210. Good for coding." is better than "CodeNinja is an enhanced version of the renowned model... designed to be an indispensable tool for coders".