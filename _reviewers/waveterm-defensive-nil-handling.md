---
title: defensive nil handling
description: Always validate values and short-circuit on errors; guard uses of possibly
  nil/empty values while avoiding redundant checks when types guarantee non-nil.
repository: wavetermdev/waveterm
label: Null Handling
language: Go
comments_count: 6
repository_stars: 17328
---

Always validate values and short-circuit on errors; guard uses of possibly nil/empty values while avoiding redundant checks when types guarantee non-nil.

Motivation:
- Prevent nil-pointer dereferences and logic bugs by validating inputs and return early on errors.
- Only add nil checks where the value may be absent/untrusted; don’t clutter code with checks that duplicate the type/API contract.
- Prefer correct, non-indirected types (e.g., []byte) to reduce nil-handling complexity.

Practices to follow:
- Validate external/untrusted inputs and parse results before use and return early on error.
  Example: check parse errors and avoid using a possibly nil value:

  // wrong: may deref newPk when parsing failed
  newPk, rtnErr := EvalMetaCommand(ctxWithHistory, pk)
  if rtnErr == nil {
      update, rtnErr = HandleCommand(ctxWithHistory, newPk)
  }

  // correct: short-circuit on error
  newPk, rtnErr := EvalMetaCommand(ctxWithHistory, pk)
  if rtnErr != nil {
      return nil, rtnErr
  }
  update, rtnErr = HandleCommand(ctxWithHistory, newPk)

- Guard resource operations that may be nil (files, sockets, interfaces) before calling methods like Close.
  Example:

  defer func() {
      for _, extraFile := range cw.Cmd.ExtraFiles {
          if extraFile != nil {
              extraFile.Close()
          }
      }
  }()

- Validate numeric/string inputs (use helpers) to enforce expected ranges and avoid later checks:
  Example: use a helper for positive integers

  idx, err := resolvePosInt(newScreenIdxStr, 1)
  if err != nil {
      return nil, err
  }

- Prefer using slices directly instead of pointers to slices; a nil slice expresses absence without extra indirection.
  Example: use sudoPw []byte instead of sudoPw *[]byte

- Do not add nil checks when the API/type guarantees non-nil; rely on that contract to keep code clear. If the contract changes or is unclear, update the type or document it rather than peppering checks.

When in doubt, ask: is the value coming from external/untrusted input or can it legitimately be nil? If external or ambiguous: validate and short-circuit. If internal and the type guarantees non-nil: omit redundant checks.

References: discussions [0,2,3,4,5,1]