---
title: precise language usage
description: Use precise, natural language in documentation to improve clarity and
  readability. Focus on accurate word choice, proper grammar, and natural phrasing
  that flows well for readers.
repository: nuxt/nuxt
label: Documentation
language: Markdown
comments_count: 11
repository_stars: 57769
---

Use precise, natural language in documentation to improve clarity and readability. Focus on accurate word choice, proper grammar, and natural phrasing that flows well for readers.

Key areas to address:

**Word Choice Precision**: Choose specific, accurate terms over vague ones:
- Use "several" instead of "a number of"
- Use "must" instead of "have to" for requirements
- Use "accessible" instead of "directly served" for clarity

**Natural Phrasing**: Write in a way that sounds natural when read aloud:
- "We recommend using" instead of "We recommend to use"
- "call the API directly" instead of "directly call the API"
- "you can use" instead of "you will need to use" (unless truly required)

**Grammar Accuracy**: Pay attention to conjunctions and sentence structure:
- Use "or" vs "and" correctly: "setup function or lifecycle hooks" (not both required)
- Place commas carefully as they affect meaning: "only works during setup, inside plugins" vs "only works during setup inside plugins"
- Ensure parallel structure in lists: "Moving" vs "Move" - keep consistent verb forms

**Example improvements**:
```diff
- This function can also return a Promise and a value
+ This function can be asynchronous

- Never combine next() callback with a legacy middleware that is async
+ Never combine the next() callback with an async legacy middleware

- We recommend to use useHead() in app.vue
+ We recommend using useHead() in app.vue
```

These language improvements make documentation more professional, easier to understand, and reduce cognitive load for developers reading the content.