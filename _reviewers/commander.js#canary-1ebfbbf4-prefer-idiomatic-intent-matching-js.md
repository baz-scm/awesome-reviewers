---
title: Prefer idiomatic, intent-matching JS
description: Favor built-in, idiomatic JavaScript constructs over manual or legacy
  equivalents, and make sure the construct you choose actually matches the intent
  of the check. For example, use `str.endsWith('...')` instead of `str.slice(-3) ===
  '...'`, `str.startsWith('--no-')` instead of `flags.indexOf('-no-') !== -1` or `~flags.indexOf(...)`,
  `Array.isArray(x)`...
repository: tj/commander.js#CANARY-1ebfbbf4
label: Code Style
language: JavaScript
comments_count: 11
repository_stars: 28444
---

Favor built-in, idiomatic JavaScript constructs over manual or legacy equivalents, and make sure the construct you choose actually matches the intent of the check. For example, use `str.endsWith('...')` instead of `str.slice(-3) === '...'`, `str.startsWith('--no-')` instead of `flags.indexOf('-no-') !== -1` or `~flags.indexOf(...)`, `Array.isArray(x)` instead of a hand-rolled `isArray` helper, and ES2015 default parameters (`function foo(allowExcess = true)`) instead of manually checking for `undefined`. When replacing `indexOf` checks, pick the method that preserves the original semantics — e.g. use `startsWith` rather than `includes` if the original check was for a prefix (`arg.indexOf('--inspect') === 0` should become `arg.startsWith('--inspect')`, not `arg.includes('--inspect')`). Beyond individual expressions, keep code easy to follow: group related conditions/logic that share the same guard instead of splitting them apart, pull repeated or complex inline expressions into a clearly named temporary variable before using them, and avoid "clever" tricks (such as crafting strings with trailing spaces to dodge an extra join delimiter) in favor of a straightforward loop or well-named helper. These choices reduce redundancy, make the code's intent obvious at a glance, and are easier for future readers to maintain.</description>
</invoke>
