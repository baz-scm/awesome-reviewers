---
title: Secure Scope and Input Validation
description: All security-relevant authorization/receipt logic must be (1) scope-correct
  and precondition-correct, and (2) fed only strictly validated/sanitized inputs—especially
  when values are used to render/parse audit logs, build regexes, or mutate the filesystem.
repository: awslabs/aidlc-workflows
label: Security
language: TypeScript
comments_count: 6
repository_stars: 3849
---

All security-relevant authorization/receipt logic must be (1) scope-correct and precondition-correct, and (2) fed only strictly validated/sanitized inputs—especially when values are used to render/parse audit logs, build regexes, or mutate the filesystem.

Rules to apply
1) Don’t let global state “prove” per-entity review
- If receipts are per-unit/per-scope, verification must prove each unit’s current artifacts against that unit’s own evidence. Never treat “newest fingerprint matches current workspace” as equivalent to “every unit’s current source was reviewed.”

2) Protect authority-bearing events and gates
- Block direct emission of authority-bearing audit event types from generic CLI paths; only the owning tool/hook may write them.
- Enforce required preconditions before recording gate decisions (e.g., require a human presence/turn before committing approvals/rejections that are later treated as authority).

3) Validate audit/event fields to prevent injection/forgery
- Reject control characters in field names (and generally enforce a single-line, strict grammar for any key that can be rendered into audit text or matched by multiline parsers).
- Never accept arbitrary strings that can be interpreted as additional `Event:` lines or alter block parsing.

4) Validate identifiers against the authoritative model
- For lifecycle/receipt commands, only accept unit identifiers that exist in the authoritative DAG/state model; reject newline/path traversal and other characters that can corrupt state-mirrored values.

5) Escape or avoid dynamic regex construction
- If any anchor/user-provided token is interpolated into `new RegExp`, always `escapeRegExp` first and validate the token against an allowlist grammar.
- Prefer “skip-and-log” for malformed inputs over throwing and failing partially-composed runs.

6) Guard destructive filesystem operations in CLI
- Refuse to recursively delete an arbitrary `outDir` unless it is a known safe target (e.g., contains a projection marker) or the user explicitly passes `--force`.

Example patterns
- Regex escaping + grammar validation:
```ts
function escapeRegExp(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function locateAnchor(content: string, anchor: string): number {
  if (!/^after-step:\d+$/.test(anchor)) return -1; // strict grammar
  const n = anchor.slice("after-step:".length);
  const re = new RegExp(`^### Step ${escapeRegExp(n)}\\b.*$`, "m");
  // ... use re
}
```
- OutDir guard for destructive builds:
```ts
if (existsSync(outDir) && readdirSync(outDir).length > 0) {
  const marker = join(outDir, "<projection-marker>");
  if (!existsSync(marker) && !argv.includes("--force")) {
    throw new Error("Refusing to delete non-projection outDir; use --force");
  }
}
```

Impact
Following this standard prevents: scope confusion in receipt verification, authority forgery via audit parsing quirks, regex-based mis-parsing/splicing, state corruption from unsafe identifiers, and accidental/hostile filesystem deletion—directly addressing the security risks raised in these discussions.