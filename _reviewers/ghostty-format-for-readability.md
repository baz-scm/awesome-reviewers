---
title: Format for readability
description: 'Documentation should be formatted to optimize readability and information
  retention. Apply these principles to make documentation more user-friendly:

  '
repository: ghostty-org/ghostty
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 32864
---

Documentation should be formatted to optimize readability and information retention. Apply these principles to make documentation more user-friendly:

1. Place explanatory text close to related code examples, avoiding isolated sentences that break the flow of information.

2. Use text formatting (especially **bold**) to highlight key terms and important concepts that readers might need when skimming the document.

3. Structure information logically, with explanations preceding code examples when they provide context for understanding the example.

Example of good formatting:

```markdown
Add a line to the CODEOWNERS file (where `xx_YY` is your locale):

```diff
 # Localization
 /po/README_TRANSLATORS.md @ghostty-org/localization
 /po/com.mitchellh.ghostty.pot @ghostty-org/localization
 /po/zh_CN.UTF-8.po @ghostty-org/zh_CN
+/po/xx_YY.UTF-8.po @ghostty-org/xx_YY
```
```

This standard helps documentation serve both careful readers and those quickly scanning for specific information.