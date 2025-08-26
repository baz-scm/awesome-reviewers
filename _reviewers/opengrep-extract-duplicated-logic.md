---
title: Extract duplicated logic
description: When you notice the same code pattern appearing in multiple places, extract
  it into a reusable function rather than copy-pasting. Duplicated code is error-prone
  and harder to maintain. Look for repeated logic, data structure creation patterns,
  or similar operations that can be abstracted.
repository: opengrep/opengrep
label: Code Style
language: Other
comments_count: 2
repository_stars: 1546
---

When you notice the same code pattern appearing in multiple places, extract it into a reusable function rather than copy-pasting. Duplicated code is error-prone and harder to maintain. Look for repeated logic, data structure creation patterns, or similar operations that can be abstracted.

For example, instead of repeating fold operations:
```ocaml
(* Duplicated pattern *)
taints_and_shapes
|> List.fold_left (fun acc (taints, shape) ->
     acc |> Taints.union taints |> Taints.union (Shape.gather_all_taints_in_shape shape))
```

Extract it into a helper function that can be reused across multiple locations.

Similarly, instead of copy-pasting record definitions:
```ocaml
(* Instead of duplicating this structure *)
{
  source_kind = "semgrepignore";
  filename = custom_filename;
  format = Gitignore.Legacy_semgrepignore;
}
```

Create a parameterized function:
```ocaml
let semgrepignore_files ~filename = {
  source_kind = "semgrepignore";
  filename;
  format = Gitignore.Legacy_semgrepignore;
}
```

This approach improves code organization, reduces maintenance burden, and prevents inconsistencies that arise from manual copying.