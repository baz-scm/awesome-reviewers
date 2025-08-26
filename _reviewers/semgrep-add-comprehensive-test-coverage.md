---
title: Add comprehensive test coverage
description: 'Ensure all code changes include appropriate unit tests and address any
  identified testing gaps immediately. When reviewing code, verify that:


  1. **New functionality has corresponding tests**: Every new feature or significant
  code change should include unit tests that exercise the new behavior.'
repository: semgrep/semgrep
label: Testing
language: Other
comments_count: 3
repository_stars: 12598
---

Ensure all code changes include appropriate unit tests and address any identified testing gaps immediately. When reviewing code, verify that:

1. **New functionality has corresponding tests**: Every new feature or significant code change should include unit tests that exercise the new behavior.

2. **Existing untested code gets tests when modified**: If you're working on code that lacks test coverage, add tests as part of your changes rather than deferring them.

3. **Test TODOs are addressed, not accumulated**: Don't leave comments like "TODO: This has a bug!!!" in test code. Either fix the issue immediately or create a proper ticket to track it.

4. **Mark missing test areas explicitly**: When you identify code that needs tests but can't add them immediately, add clear TODO comments like `(* TODO: test this *)` to acknowledge the gap and help future developers.

Example from the discussions:
```ocaml
(* Instead of leaving this unaddressed: *)
(* TODO: This has a bug!!!
   Suppose we exclude `test.py` and are given `tests2/test.py`.
   This code will not exclude properly... *)

(* Do this: *)
(* Add unit test for path exclusion edge cases - see issue #1234 *)
let test_path_exclusion_with_nested_dirs () = 
  (* Test the specific bug case mentioned *)
  assert (excludes_file "test.py" "tests2/test.py" = true)
```

The goal is to build confidence in code changes through comprehensive testing rather than relying on manual verification like "run -cfg_il and looks like it's ok".