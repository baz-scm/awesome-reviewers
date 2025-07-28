---
title: Write audience-appropriate documentation
description: Documentation should be written from the perspective of its intended
  audience, using language and detail levels appropriate for that audience. Focus
  on what matters most to the reader rather than technical implementation details.
repository: alacritty/alacritty
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 59675
---

Documentation should be written from the perspective of its intended audience, using language and detail levels appropriate for that audience. Focus on what matters most to the reader rather than technical implementation details.

For user-facing documentation (changelogs, READMEs, FAQs):
- Describe effects and outcomes rather than internal mechanisms
- Avoid vague terms like "could", "easily", or "might" 
- Keep explanations concise and practical
- Highlight information that requires user attention (e.g., breaking changes)

For developer documentation:
- Use precise, unambiguous language
- Distinguish between different types of users (end users vs library consumers)
- Ensure grammatical correctness and clarity

Example from changelog entries:
```
❌ Technical: "Shell initialization on macOS to manually check the ~/.hushlogin file"
✅ User-focused: "Hide login message if ~/.hushlogin is present"

❌ Vague: "could be easily done by user"  
✅ Precise: "can be done outside of alacritty_terminal"
```

This approach ensures documentation serves its intended purpose by meeting readers where they are and providing the information they actually need.