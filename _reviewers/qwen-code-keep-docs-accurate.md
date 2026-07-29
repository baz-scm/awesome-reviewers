---
title: Keep Docs Accurate
description: Adopt a rule that comments/JSDoc/API docs must be both *correct* and
  *useful at the point of use*—never misleading, stale, or attached to the wrong symbol.
repository: QwenLM/qwen-code
label: Documentation
language: TypeScript
comments_count: 11
repository_stars: 26407
---

Adopt a rule that comments/JSDoc/API docs must be both *correct* and *useful at the point of use*—never misleading, stale, or attached to the wrong symbol.

Apply this checklist:
- **Behavior parity:** If code changes behavior/outputs, update *all* related docs/comments/examples/tags to match emitted formats and success/failure conditions.
- **Security/contract truth:** Never document validation or guarantees that the code doesn’t actually enforce; if validation happens at a different boundary, say so.
- **Attach-to-right-declaration:** Ensure each `/** ... */` block is positioned so TypeScript attaches it to the intended declaration; avoid duplicate/orphaned JSDoc blocks.
- **Document the real contract at risk boundaries:** If an implementation relies on a consumption pattern (e.g., synchronous consumption of a reused buffer view), state it at the `yield`/API boundary.
- **No stale summaries or historical narrative:** Keep comments about *why/semantics* (especially non-obvious choices). Don’t embed commit-message history in code comments; remove or reword.
- **UI/i18n parity (where relevant):** Any new `t('...')` keys must be added to all locales.
- **Avoid redundant rationales:** Don’t duplicate wording already present in higher-level JSDoc/rules unless it cannot drift.

Example: document generator consumption when yielding views into a reused buffer
```ts
async function* readFileHandleChunks(fileHandle: FileHandle, sourceSize: number): AsyncGenerator<Buffer> {
  const highWaterMark = 512 * 1024;
  const buffer = Buffer.allocUnsafe(highWaterMark);
  let position = 0;
  while (position < sourceSize) {
    const bytesRead = (await fileHandle.read(buffer, 0, Math.min(highWaterMark, sourceSize - position), position)).bytesRead;
    if (bytesRead === 0) return;
    position += bytesRead;

    // CONTRACT: This is a view into a reused underlying buffer.
    // Consumers must synchronously copy/consume the bytes before the next `yield`.
    yield buffer.subarray(0, bytesRead);
  }
}
```

If you make a behavioral change (output strings, semantics, validation rules, or i18n keys), treat documentation/comment updates as part of the same change set—otherwise the next developer will be guided by false information.