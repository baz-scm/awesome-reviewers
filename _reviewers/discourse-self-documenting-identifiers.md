---
title: Self-documenting identifiers
description: Choose names that are immediately understandable without requiring additional
  context, documentation lookup, or guessing. Identifiers should clearly communicate
  their purpose, units, and behavior to reduce cognitive load for developers.
repository: discourse/discourse
label: Naming Conventions
language: Yaml
comments_count: 2
repository_stars: 44898
---

Choose names that are immediately understandable without requiring additional context, documentation lookup, or guessing. Identifiers should clearly communicate their purpose, units, and behavior to reduce cognitive load for developers.

For configuration settings and labels, prioritize descriptive language over technical jargon. When technical terms are necessary, pair them with plain language explanations. For time-based or measurement settings, include units directly in the name to eliminate ambiguity.

Examples:
- Prefer `pending_users_reminder_delay_minutes` over `pending_users_reminder_delay` 
- Prefer "Allow editing options after posting (dynamic poll)" over "Enable dynamic mode (allow editing options after posting)"

This approach prevents developers from having to guess units, look up documentation, or decipher technical terminology, leading to more maintainable and accessible code.