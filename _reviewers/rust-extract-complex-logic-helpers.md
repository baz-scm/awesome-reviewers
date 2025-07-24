---
title: Extract complex logic helpers
description: 'Complex or duplicated logic should be extracted into well-named helper
  functions to improve code readability and maintainability. This applies to:


  1. Large blocks of code in functions that handle a specific subtask'
repository: rust-lang/rust
label: Code Style
language: Rust
comments_count: 4
repository_stars: 105254
---

Complex or duplicated logic should be extracted into well-named helper functions to improve code readability and maintainability. This applies to:

1. Large blocks of code in functions that handle a specific subtask
2. Similar logic repeated in multiple places
3. Complex conditional logic that can be given a descriptive name

Example:

Instead of:
```rust
fn handle_options(early_dcx: &EarlyDiagCtxt, args: &[String]) -> Option<getopts::Matches> {
    // ... other code ...
    
    if let Some(name) = matches.opt_str("o")
        && let Some(suspect) = args.iter().find(|arg| arg.starts_with("-o") && *arg != "-o")
    {
        let confusables = ["optimize", "o0", "o1", "o2", "o3", "ofast", "og", "os", "oz"];
        if let Some(confusable) = check_confusables(&suspect, &confusables) {
            early_dcx.early_warn(
                "option `-o` has no space between flag name and value, which can be confusing",
            );
            early_dcx.early_note(format!(
                "option `-o {}` is applied instead of a flag named `o{}` to specify output filename `{}`",
                name, name, name
            ));
            if !confusable.is_empty() {
                early_dcx.early_note(format!("Do you mean `{}`?", confusable));
            }
        }
    }
}
```

Better:
```rust
fn handle_options(early_dcx: &EarlyDiagCtxt, args: &[String]) -> Option<getopts::Matches> {
    // ... other code ...
    warn_on_confusing_output_filename_flag(early_dcx, &matches, args);
}

fn warn_on_confusing_output_filename_flag(early_dcx: &EarlyDiagCtxt, matches: &Matches, args: &[String]) {
    if let Some(name) = matches.opt_str("o")
        && let Some(suspect) = args.iter().find(|arg| arg.starts_with("-o") && *arg != "-o")
    {
        let confusables = ["optimize", "o0", "o1", "o2", "o3", "ofast", "og", "os", "oz"];
        if let Some(confusable) = check_confusables(&suspect, &confusables) {
            early_dcx.early_warn(
                "option `-o` has no space between flag name and value, which can be confusing",
            );
            early_dcx.early_note(format!(
                "option `-o {}` is applied instead of a flag named `o{}` to specify output filename `{}`",
                name, name, name
            ));
            if !confusable.is_empty() {
                early_dcx.early_note(format!("Do you mean `{}`?", confusable));
            }
        }
    }
}
```

This improves code by:
- Making the main function clearer and more focused
- Giving complex logic a descriptive name that explains its purpose
- Making the code easier to test and modify
- Reducing cognitive load when reading the code