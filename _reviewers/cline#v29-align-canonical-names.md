---
title: Align Canonical Names
description: 'Adopt a single canonical naming scheme for identifiers that cross product
  boundaries (API fields, event names, payload keys, and configuration keys). If product
  variants drift, treat it as a defect: align the canonical names, deprecate legacy
  names, and keep an explicit mapping layer so older clients keep working.'
repository: cline/cline#v29
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 70893
---

Adopt a single canonical naming scheme for identifiers that cross product boundaries (API fields, event names, payload keys, and configuration keys). If product variants drift, treat it as a defect: align the canonical names, deprecate legacy names, and keep an explicit mapping layer so older clients keep working.

Apply it as follows:
- **Define canonical names** (the one true spelling for field/key names and config namespaces).
- **When you find mismatches, file bugs** for each specific drift (don’t fix ad-hoc only in one doc/tool).
- **Deprecate legacy names with a compatibility window**: continue accepting/producing old names for a defined period while migrating callers to the canonical ones.
- **Use explicit mapping tables/shims** at integration boundaries (parsers/serializers) and add tests that validate both shapes map to the same internal model.
- **Namespace config keys by build identity** when behavior truly differs (e.g., rollout/bundle selection) so Nightly/legacy settings don’t silently target the wrong bundle.

Example (canonical payload naming with compatibility mapping):
```js
// Internal model uses canonical names.
function normalizeHookPayload(raw) {
  // Canonical: preToolUse.toolName / preToolUse.parameters
  // Legacy: tool_call / tool_result style or different casing.
  if (raw.hookName === 'tool_call' && raw.tool_call) {
    return {
      hookName: 'PreToolUse',
      toolName: raw.tool_call.name,
      parameters: raw.tool_call.input,
    };
  }
  if (raw.preToolUse?.toolName) {
    return {
      hookName: 'PreToolUse',
      toolName: raw.preToolUse.toolName,
      parameters: raw.preToolUse.parameters,
    };
  }
  return null;
}
```
This keeps naming consistent for developers and prevents docs/settings from becoming silently wrong across product variants.