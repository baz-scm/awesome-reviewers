---
title: Intentful Comments And Limits
description: Add comments that explain *why* the code behaves as it does—especially
  for platform-specific/terminal/UI quirks—and explicitly document any partial implementation.
repository: earendil-works/pi
label: Documentation
language: TypeScript
comments_count: 2
repository_stars: 79783
---

Add comments that explain *why* the code behaves as it does—especially for platform-specific/terminal/UI quirks—and explicitly document any partial implementation.

Apply this standard:
- **Prefer intent over noise:** If logic isn’t obvious from the code (e.g., OS/terminal intercept behavior), add a brief inline comment stating the rationale.
- **Document limitations/tradeoffs:** If you can’t fully implement a feature due to an existing mechanism or tracker/state model, record:
  1) what’s supported today,
  2) what isn’t,
  3) why (the blocker/constraint),
  4) a reasonable follow-up direction.
- **Keep it actionable:** Comments should help the next developer understand and extend the code without reverse-engineering.

Example pattern:
```ts
// On Windows Terminal (including WSL), Ctrl+V is intercepted by the terminal.
const pasteKey = process.platform === "win32" ? "alt+v" : "ctrl+v";

// Wrap link text in OSC 8 hyperlink sequences for terminal click support.
const osc8Open = `\x1b]8;;${url}\x07`;
const osc8Close = `\x1b]8;;\x07`;
result += osc8Open + linkText + osc8Close;

// Limitation: only SGR is tracked for styling state.
// OSC 8 state isn’t tracked yet, so only the first segment is clickable.
// Follow-up: extend the ANSI/terminal wrapping logic to include OSC 8 boundaries.
```