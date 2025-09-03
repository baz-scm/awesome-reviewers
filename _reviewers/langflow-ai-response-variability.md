---
title: AI response variability
description: When documenting AI model interactions, account for the non-deterministic
  nature of AI responses and avoid assumptions about specific outputs. AI models can
  produce different responses to identical inputs, and model behavior changes over
  time through updates and improvements.
repository: langflow-ai/langflow
label: AI
language: Markdown
comments_count: 4
repository_stars: 111046
---

When documenting AI model interactions, account for the non-deterministic nature of AI responses and avoid assumptions about specific outputs. AI models can produce different responses to identical inputs, and model behavior changes over time through updates and improvements.

Write documentation that remains accurate regardless of response variations:

```markdown
# Instead of assuming specific responses:
The LLM response is vague, though the Agent does know the current date.

# Use generic descriptions that account for variability:
This query demonstrates how an LLM, by itself, might not have access to 
information or functions designed to address specialized queries. In this 
example, the default OpenAI model provides a vague response, although the 
agent does know the current date by using its internal `get_current_date` function.
```

Avoid describing models with performance or cost specifics that may become outdated. Instead of "this model is a good balance of performance and cost," use "this model is a balanced model" or reference the provider's current recommendations.

Include disclaimers when showing example AI responses: "The following is an example of a response returned from this tutorial's flow. Due to the nature of LLMs and variations in your inputs, your response might be different."

This approach ensures documentation remains useful as AI models evolve and helps users understand the inherent variability in AI systems.