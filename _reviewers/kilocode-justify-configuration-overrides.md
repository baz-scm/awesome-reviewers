---
title: Justify configuration overrides
description: Before adding manual configuration entries, verify that the tool doesn't
  already provide the desired behavior automatically. Document why the override is
  necessary and what specific problem it solves.
repository: kilo-org/kilocode
label: Configurations
language: Json
comments_count: 2
repository_stars: 7302
---

Before adding manual configuration entries, verify that the tool doesn't already provide the desired behavior automatically. Document why the override is necessary and what specific problem it solves.

Many development tools have intelligent defaults and auto-discovery features. Adding unnecessary configurations can create maintenance overhead and potential conflicts.

When proposing configuration changes:
1. Research the tool's default behavior and auto-discovery capabilities
2. Clearly explain what problem the configuration solves
3. Consider potential conflicts with other extensions or tools
4. Document any environment-specific exclusions with clear reasoning

Example from VS Code keybindings:
```json
{
  "command": "editor.action.inlineSuggest.commit",
  "key": "tab",
  "when": "inlineSuggestionVisible && editorTextFocus && !editorTabMovesFocus && !inSnippetMode && !suggestWidgetVisible"
}
```

Instead of complex conditions, first verify if the desired behavior can be achieved through simpler means or if the tool already supports it in certain contexts.