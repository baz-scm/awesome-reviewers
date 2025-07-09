---
title: Meaningful consistent identifiers
description: 'Choose descriptive, semantically accurate names for variables, types,
  and components that clearly communicate their purpose. Maintain consistency throughout
  your codebase by:'
repository: shadcn-ui/ui
label: Naming Conventions
language: TSX
comments_count: 5
repository_stars: 90568
---

Choose descriptive, semantically accurate names for variables, types, and components that clearly communicate their purpose. Maintain consistency throughout your codebase by:

1. Using established naming patterns for similar concepts (e.g., `ComponentNameProps` for interface props)
2. Avoiding duplicate type/interface names that cause confusion
3. Reusing defined types instead of redefining them
4. Using specific type definitions rather than generic indexing to preserve IDE autocompletion

```typescript
// ❌ Poor naming practices
import { Slot } from "radix-ui"
// Duplicate interface name causes confusion
interface TimelineConent extends React.HTMLAttributes<HTMLParagraphElement> {}
// Generic typing disables autocompletion
type IconComponents = { [key: string]: (props: IconProps) => JSX.Element }
// Type redefinition instead of reuse
interface MultiSelectProps {
  options: Record<"value" | "label", string>[]
}

// ✅ Better naming practices
import { Slot as SlotPrimitive } from "radix-ui"
// Consistent naming pattern
interface TimelineHeadingProps extends React.HTMLAttributes<HTMLParagraphElement> {}
// Specific typing enables autocompletion
type IconComponents = {
  logo: (props: IconProps) => JSX.Element;
  // other specific icon components...
}
// Reusing defined types
export type OptionType = Record<"value" | "label", string>
interface MultiSelectProps {
  options: OptionType[]
}
```

When choosing between similar terms (like "mode" vs "theme"), select the one that most accurately represents the concept's purpose in your codebase, and document the distinction to maintain consistency.