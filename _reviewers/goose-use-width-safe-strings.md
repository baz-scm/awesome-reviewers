---
title: Use width-safe strings
description: When implementing string operations that depend on the environment (terminal/UI
  rendering or filesystem paths), avoid naive `.length`/single-separator logic. Use
  algorithms that are correct for Unicode/code points and for the actual width/splitting
  rules of the runtime.
repository: aaif-goose/goose
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 51876
---

When implementing string operations that depend on the environment (terminal/UI rendering or filesystem paths), avoid naive `.length`/single-separator logic. Use algorithms that are correct for Unicode/code points and for the actual width/splitting rules of the runtime.

Apply:
- Terminal/UI truncation: truncate by display width (terminal cells), not by JavaScript string length. Ensure truncation is code-point safe (so astral/Unicode characters aren’t cut into replacement glyphs) and make any “pre-reservation” math match what will actually render.
- Path parsing: split filesystem paths using both `/` and `\` (after trimming trailing separators), so Windows and POSIX paths behave the same.

Example patterns:
```ts
// Width-safe truncation (prefer established libs)
import stringWidth from 'string-width';
import cliTruncate from 'cli-truncate';

function truncateForTerminal(label: string, maxCells: number) {
  // Truncates by terminal cells; avoids naive .length truncation.
  // (Use/align with the same render-side truncation approach.)
  return cliTruncate(label, maxCells, { ellipsis: '…' });
}

// Cross-platform path splitting
function splitDirPath(dir: string): { name: string; parent: string } {
  const trimmed = dir.replace(/[\\/]+$/, '');
  const parts = trimmed.split(/[\\/]/);
  const name = parts.pop() ?? '';
  const parent = parts.join('/');
  return { name, parent };
}
```

Checklist:
- Do not use `.length` to decide visual fit in terminal/UI.
- Do not truncate Unicode strings in ways that can split code points.
- Normalize inputs (e.g., trim trailing separators) before splitting.
- Support both common separators for filesystem paths.