---
title: Context-aware React State
description: In React components, make UI state transitions and DOM identity depend
  on the *current* rendered context (route/view/filter) and the *current component
  instance*. This prevents stale navigation, incorrect optimistic updates, and broken
  label/control associations.
repository: aaif-goose/goose
label: React
language: TSX
comments_count: 3
repository_stars: 51876
---

In React components, make UI state transitions and DOM identity depend on the *current* rendered context (route/view/filter) and the *current component instance*. This prevents stale navigation, incorrect optimistic updates, and broken label/control associations.

Apply this as a rule of thumb:
- **Route-aware changes:** When mutating an entity that may be currently open, ensure navigation updates match what the UI is showing (e.g., avoid leaving route params that would cause stale re-renders).
- **Filter-aware optimistic updates:** When you optimistically update/delete/toggle an item, decide whether to update in-place or remove from the list based on the active filter/view that determines whether it should still be visible.
- **Instance-unique form IDs:** When rendering labeled controls in reusable components that can mount multiple times, namespace `id`/`htmlFor` using `useId()`.

Example patterns:
```tsx
// 1) Route-aware transition (concept)
function leaveRouteIfCurrent(currentId: string, nextPath = '/') {
  if (getCurrentOpenSessionId() === currentId) navigate(nextPath);
}

// 2) Filter-aware optimistic update
const handleToggleArchive = async (session: SessionListItem) => {
  const isArchived = !!session.archivedAt;
  setSessions(prev => {
    if (activeFilter === 'all') {
      // keep row; it still matches
      return prev.map(s => (s.id === session.id ? { ...s, archivedAt: isArchived ? null : new Date().toISOString() } : s));
    }
    // active/archived views: toggle may move it out of scope
    return prev.filter(s => s.id !== session.id);
  });
};

// 3) Instance-unique label/control pairing
function ParameterInputModal({ parameters }: { parameters: { key: string }[] }) {
  const reactId = React.useId();
  const fieldId = (key: string) => `${reactId}-${key}`;

  return (
    <div>
      {parameters.map((param) => (
        <div key={param.key}>
          <label htmlFor={fieldId(param.key)}>{param.key}</label>
          <input id={fieldId(param.key)} />
        </div>
      ))}
    </div>
  );
}
```
Use this checklist whenever you change data that affects (1) what’s open on the screen, (2) what’s included in the current list/filter, or (3) how inputs are labeled/identified in the DOM.