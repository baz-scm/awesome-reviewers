---
title: Use descriptive contextual names
description: Choose variable, method, and property names that clearly communicate
  their purpose and context to avoid confusion and misinterpretation. Names should
  be self-explanatory and specific enough that their meaning is unambiguous within
  their usage context.
repository: SigNoz/signoz
label: Naming Conventions
language: TSX
comments_count: 3
repository_stars: 23369
---

Choose variable, method, and property names that clearly communicate their purpose and context to avoid confusion and misinterpretation. Names should be self-explanatory and specific enough that their meaning is unambiguous within their usage context.

Avoid generic or ambiguous names that could have different meanings depending on the context. Instead, use descriptive names that explain both what the identifier represents and how it's intended to be used.

Consider future extensibility when naming - avoid names that are too specific to current implementation details that might change.

Examples of improvements:
- `HasRunOnExplorer` → `calledFromHandleRunQuery` (explains the source/context of the call)
- `hasEditPermission` → `isEditorOrAdmin` (specifies the exact permission level)
- `isTenMinutesTracesTimeRange` → `useFocusedTracesTimeRange` (describes the behavior, not the specific time constraint)

This practice reduces cognitive load during code reviews and maintenance, making the codebase more self-documenting and less prone to misunderstandings.