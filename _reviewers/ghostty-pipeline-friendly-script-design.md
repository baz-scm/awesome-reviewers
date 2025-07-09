---
title: Pipeline-friendly script design
description: Design scripts to be easily integrated into build pipelines and CI/CD
  workflows by using standard I/O streams instead of hardcoded file paths. Scripts
  that read from stdin and write to stdout can be easily composed in pipelines, redirected,
  and incorporated into various build systems without modification.
repository: ghostty-org/ghostty
label: CI/CD
language: Python
comments_count: 2
repository_stars: 32864
---

Design scripts to be easily integrated into build pipelines and CI/CD workflows by using standard I/O streams instead of hardcoded file paths. Scripts that read from stdin and write to stdout can be easily composed in pipelines, redirected, and incorporated into various build systems without modification.

Example - Before:
```python
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    
    patcher_path = project_root / "vendor" / "nerd-fonts" / "font-patcher.py"
    source = patcher_path.read_text(encoding="utf-8")
    patch_set = extract_patch_set_values(source)
    
    out_path = project_root / "src" / "font" / "nerd_font_attributes.zig"
    # Write results to out_path
```

Example - After:
```python
import sys

if __name__ == "__main__":
    # Read from stdin if no arguments provided
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            source = f.read()
    else:
        source = sys.stdin.read()
        
    patch_set = extract_patch_set_values(source)
    
    # Write results to stdout
    print(generate_zig_output(patch_set))
```

This approach allows the script to be used in various CI contexts: `cat input.txt | python script.py > output.zig` or as part of more complex build rules without requiring code changes.