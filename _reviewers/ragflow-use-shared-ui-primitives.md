---
title: Use Shared UI Primitives
description: 'When building UI, follow the project’s existing design-system components
  and tokens instead of creating bespoke patterns.


  **Standards**

  1. **Prefer shared form/UI building blocks**: Use existing components like `RAGFlowFormItem`,
  `SimilaritySliderFormField`, and `SearchInput` rather than re-implementing the same
  UI logic/styling.'
repository: infiniflow/ragflow
label: Code Style
language: TSX
comments_count: 6
repository_stars: 80174
---

When building UI, follow the project’s existing design-system components and tokens instead of creating bespoke patterns.

**Standards**
1. **Prefer shared form/UI building blocks**: Use existing components like `RAGFlowFormItem`, `SimilaritySliderFormField`, and `SearchInput` rather than re-implementing the same UI logic/styling.
2. **Use standard shadcn components for complex layouts**: For table-like lists, use the shadcn `Table` component (not a hand-rolled `<table>` with custom class logic).
3. **Extract complex dialogs into standalone components/files**: If a component contains a full `Dialog` implementation (multi-field forms, footers, local state), move it to a dedicated file/component.
4. **Use global design tokens/colors**: Prefer color variables from `tailwind.css` over ad-hoc inline `style={{ backgroundColor: ... }}` so theming stays consistent.

**Example (extraction + token usage)**
```tsx
// skills/components/CreateSpaceDialog.tsx
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export function CreateSpaceDialog(props: {
  open: boolean;
  onOpenChange: (v: boolean) => void;
  value: string;
  onChange: (v: string) => void;
  onCreate: () => void;
  onCancel: () => void;
}) {
  return (
    <Dialog open={props.open} onOpenChange={props.onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create New Skill Space</DialogTitle>
          <DialogDescription>Organize and manage your skills.</DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <label className="text-sm font-medium mb-2 block">Space Name</label>
          <Input value={props.value} onChange={(e) => props.onChange(e.target.value)} />
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={props.onCancel}>Cancel</Button>
          <Button onClick={props.onCreate} disabled={!props.value.trim()}>Create</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

Applying these keeps UI consistent, reduces duplicated styling/behavior, improves readability, and makes future theme/UI updates cheaper.