---
title: Capability-Aware Interface Contracts
description: When designing client-facing interfaces (request payloads, component
  props, or render-slot “host action” APIs), treat optional features and host-provided
  children as contracts—not assumptions.
repository: QwenLM/qwen-code
label: API
language: TSX
comments_count: 5
repository_stars: 26407
---

When designing client-facing interfaces (request payloads, component props, or render-slot “host action” APIs), treat optional features and host-provided children as contracts—not assumptions.

Apply these rules:
1) Capability-gate request fields: Only send optional parameters when the server/daemon advertises support. Keep gating consistent across all call sites.
2) Don’t rely on opaque host forwarding: If your component needs to identify/trigger host actions after re-parenting (e.g., overflow menu), don’t depend on injected props/selectors being forwarded by arbitrary ReactNodes. Use wrappers, structured action descriptors (id/label/callback), or require/tightly type a forwarding contract (documented + enforced).
3) Keep shared state props consistent: If sibling controls are disabled/enabled based on the same state (e.g., approval pending), pass the computed value through—avoid hardcoded props.
4) Make UX fallbacks explicit: Avoid hardcoded non-localized labels and ensure accessible naming is produced from contract inputs (e.g., prefer `aria-label`/`title`, and don’t create unlabeled menu items from icon-only children).

Example (capability-gated request param):
```ts
const params: any = {
  pageSize: SESSION_LIST_PAGE_SIZE,
  archiveState: 'active',
};
if (capabilities.session_source_metadata) {
  params.sourceType = WEB_SHELL_SESSION_SOURCE_TYPE;
}
await listWorkspaceSessions(params);
```

Example (avoid opaque render-slot assumptions—use descriptors instead of ReactNode host actions):
```ts
type PaneAction = { id: string; label: string; onSelect: () => void };

function PaneHeaderActions({ actions }: { actions: PaneAction[] }) {
  return (
    <DropdownMenu>
      {actions.map(a => (
        <DropdownMenuItem key={a.id} onSelect={a.onSelect}>
          {a.label}
        </DropdownMenuItem>
      ))}
    </DropdownMenu>
  );
}
```