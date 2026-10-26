---
title: Canonical naming consistency
description: Use a single canonical form for any named identifier (command names,
  paths, component/icon identifiers) and make all code paths use the same representation.
repository: cline/cline#v28
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70893
---

Use a single canonical form for any named identifier (command names, paths, component/icon identifiers) and make all code paths use the same representation.

Apply two checks:
1) Normalize consistently across the full lifecycle. If the runtime/runner normalizes a name (e.g., trims whitespace), apply the same normalization wherever the name is produced, stored, displayed, inspected, and executed. Avoid adding extra validation in only one stage that would make inspection/registration disagree with execution.
2) Use consistent sources for repeated identifiers. For common icons/components, prefer the shared imported component (same symbol/component name and usage pattern) rather than inline or ad-hoc variants, so reviewers can easily verify the intended identifier.

Example (canonical normalization across stages):
```ts
// Ensure menu-path/inspection/execution all use the same canonicalization
function canonicalCommandName(name: string) {
  return name.trim();
}

// Use canonicalCommandName when registering, inspecting, and executing
const canonical = canonicalCommandName(rawName);
registerCommand(canonical, handler);
inspectCommand(canonical);
executeCommand(canonical, args);
```

Example (consistent identifier source for icons):
```tsx
// Prefer the shared icon component/import so it’s verifiable
import { X } from 'lucide-react';

export function CloseButton({ onClick }: { onClick: () => void }) {
  return <X className="h-4 w-4" onClick={onClick} aria-hidden="true" />;
}
```