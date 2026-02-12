---
title: Explicit API shapes
description: Require API surfaces (payloads, function contracts, and compact descriptor
  grammars) to be explicit, well-documented, and normalized at the boundary. This
  reduces client/server surprises, clarifies intent (single vs collection), and ensures
  deterministic parsing.
repository: wavetermdev/waveterm
label: API
language: TypeScript
comments_count: 5
repository_stars: 17328
---

Require API surfaces (payloads, function contracts, and compact descriptor grammars) to be explicit, well-documented, and normalized at the boundary. This reduces client/server surprises, clarifies intent (single vs collection), and ensures deterministic parsing.

Guidelines
- Names and shapes: use names that reveal type and multiplicity. Prefer pluralized fields for arrays (and document element type). Example: change a singular ambiguous field:
  // before
  if ("screenstatusindicator" in update) { /* ... */ }
  // after
  if ("screenstatusindicators" in update) {
    for (const indicator of update.screenstatusindicators) { /* ... */ }
  }
  Rationale: clients and servers immediately know to expect a list; use const in iteration to avoid accidental reassignment.

- Method contracts and side effects: document whether higher-level calls encapsulate sub-operations and whether they early-return. If a wrapper may return early and skip sub-effects, provide an explicit API to perform the sub-effect or call that explicit API when you require it. Example:
  // If setActiveAuxView may return early and not call setAuxViewFocus, call setAuxViewFocus explicitly
  this.setActiveAuxView(appconst.InputAuxView_AIChat);
  this.setAuxViewFocus(true);
  Or, if the higher-level API guarantees the behavior, prefer the single call that documents the intent:
  this.inputModel.setAuxViewFocus(false); // if it calls giveFocus internally

- Input grammar & normalization: design compact descriptor formats (e.g., keyboard descriptions) with a small formal grammar, parse to structured objects, and normalize values at the boundary. Document the grammar and make parsing Unicode-aware.
  Example grammar idea (from discussions):
  - Use ':' to separate ordered sequence, and '|' to express alternatives for modifier groups.
  - ctrl:shift:c  -> ["ctrl","shift","c"]
  - ctrl|opt:c    -> [["ctrl","opt"], "c"]
  Parsing should return structured shapes (arrays/nested arrays) and normalize key names (e.g., accept " "/"Space" and map to "Space"). Use Unicode-aware checks for letter casing (e.g., /\p{Lu}/u or with the 'v' flag where supported) when inferring Shift.

- Documentation and tests: document contract, examples, and edge cases in the API docs. Add tests for: plural vs singular payloads, early-return behavior, descriptor parsing (including Unicode characters), and normalization rules.

Why this matters
- Clear shapes reduce client/server mismatch and versioning confusion.
- Explicit side-effect contracts prevent subtle bugs where callers assume sub-actions run but they do not.
- Formalized grammars and normalization produce deterministic behavior across locales and platforms.

Apply this rule when defining REST/IPC payloads, library public methods, or compact descriptor syntaxes so client code can rely on stable, well-documented interfaces.