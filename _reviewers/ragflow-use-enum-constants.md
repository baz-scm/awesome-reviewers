---
title: Use enum constants
description: When a value represents a named domain concept (e.g., Theme), use the
  corresponding enum type/constant (e.g., `ThemeEnum`) instead of duplicating raw
  string literals (`'light'`, `'dark'`). This keeps identifier naming consistent across
  schema definitions and UI/component logic.
repository: infiniflow/ragflow
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 80174
---

When a value represents a named domain concept (e.g., Theme), use the corresponding enum type/constant (e.g., `ThemeEnum`) instead of duplicating raw string literals (`'light'`, `'dark'`). This keeps identifier naming consistent across schema definitions and UI/component logic.

Example pattern:
```ts
// Prefer a single source of truth
export enum ThemeEnum {
  Light = 'light',
  Dark = 'dark',
}

// Derive schema from the enum rather than retyping literals
import { z } from 'zod';

const FormSchema = z.object({
  theme: z.enum([ThemeEnum.Light, ThemeEnum.Dark] as [string, string]),
});

// And use enum values in UI/selectors
<RadioGroup
  value={field.value}
  onValueChange={field.onChange}
>
  <RadioGroupItem value={ThemeEnum.Light} id="light" />
  <RadioGroupItem value={ThemeEnum.Dark} id="dark" />
</RadioGroup>
```