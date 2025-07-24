---
title: Provide comprehensive explanations
description: Documentation should provide thorough technical explanations that define
  key concepts, explain behaviors, and include necessary context for users to properly
  understand and use features. Avoid leaving users to guess what terms mean or how
  features differ from similar functionality.
repository: argoproj/argo-cd
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 20149
---

Documentation should provide thorough technical explanations that define key concepts, explain behaviors, and include necessary context for users to properly understand and use features. Avoid leaving users to guess what terms mean or how features differ from similar functionality.

Key practices:
- Define technical terms and concepts clearly (e.g., "What 'desired state' means")
- Explain how features differ from related functionality (e.g., "how it differs from normal diff - Live vs desired vs desired vs desired")
- Include important caveats and limitations that affect usage (e.g., "conflict with an HPA, or conflict when auto-sync is enabled")
- Preserve valuable technical details even when simplifying language
- Link to or define related concepts that users need to understand

Example of insufficient explanation:
```markdown
--compare-desired    Compare revision with desired state instead of live state
```

Example of comprehensive explanation:
```markdown
--compare-desired    Compare revision with desired state instead of live state
                     
"Desired state" refers to the configuration stored in Git that Argo CD should apply.
This differs from the normal diff behavior which compares:
- Live state (current cluster state) vs desired state (Git configuration)
Instead, this flag compares:
- Desired state (Git configuration) vs desired state (Git configuration at different revision)
```