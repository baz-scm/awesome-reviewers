---
title: AI accuracy documentation
description: Ensure accurate representation of AI model capabilities, proper attribution,
  and honest claims about functionality. When documenting AI systems, focus on the
  underlying model capabilities rather than just pipeline descriptions, provide clear
  explanations of model variants (distilled vs full models), attribute models to their
  actual creators, and avoid...
repository: menloresearch/jan
label: AI
language: Other
comments_count: 4
repository_stars: 37620
---

Ensure accurate representation of AI model capabilities, proper attribution, and honest claims about functionality. When documenting AI systems, focus on the underlying model capabilities rather than just pipeline descriptions, provide clear explanations of model variants (distilled vs full models), attribute models to their actual creators, and avoid overstating what has been achieved.

Key practices:
- Explain that AI functionality depends on "the model and its capabilities" to use tools effectively, not just the pipeline architecture
- Clarify model relationships (e.g., "why these say qwen vs llama" when discussing model variants)
- Set proper attribution: "Meta for Llama2 and Mistral for mixtral-8x7b-32768" rather than generic authors
- Use honest language: "created our own flavor of it" rather than claiming to have "replicated" proprietary systems
- Explain technical distinctions like "distilled model versus the full one" so users understand what they're actually downloading

Example model.json with proper attribution:
```json
{
  "metadata": {
    "author": "Meta", // Actual model creator, not generic name
    "description": "Llama 2 integration with Jan - our implementation of chat functionality"
  }
}
```

This prevents misleading users about AI capabilities while ensuring proper credit and technical accuracy.