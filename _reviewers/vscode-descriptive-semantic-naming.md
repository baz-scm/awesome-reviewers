---
title: Descriptive semantic naming
description: Names should accurately reflect their purpose and behavior, providing
  users and developers with clear expectations. For identifiers, use specific qualifiers
  that indicate their intended context rather than generic terms. For UI elements
  like commands, ensure the name accurately represents the behavior (e.g., only use
  ellipsis '...' when additional input...
repository: microsoft/vscode
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 174887
---

Names should accurately reflect their purpose and behavior, providing users and developers with clear expectations. For identifiers, use specific qualifiers that indicate their intended context rather than generic terms. For UI elements like commands, ensure the name accurately represents the behavior (e.g., only use ellipsis '...' when additional input will be requested).

Good example:
```json
{
  "id": "chat-instructions",  // Qualified to show specific purpose
  "command": "Delete Worktree"  // No ellipsis as no picker is shown
}
```

Poor example:
```json
{
  "id": "instructions",  // Too generic, lacks context
  "command": "Delete Worktree..."  // Misleading ellipsis suggests a picker
}
```