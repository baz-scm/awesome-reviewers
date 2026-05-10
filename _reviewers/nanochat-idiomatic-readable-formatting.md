---
title: Idiomatic Readable Formatting
description: 'When touching code that formats output or builds paths, keep it idiomatic
  and repo-consistent:

  - Avoid inline conditionals inside large f-strings; precompute conditional fragments
  and interpolate them.'
repository: karpathy/nanochat
label: Code Style
language: Python
comments_count: 5
repository_stars: 53189
---

When touching code that formats output or builds paths, keep it idiomatic and repo-consistent:
- Avoid inline conditionals inside large f-strings; precompute conditional fragments and interpolate them.
- If the value is already a `Path`, build derived paths with `Path` operators (`base / name`, `with_name`) instead of `os.path.join`.
- Don’t add redundant casts/conversions (e.g., `int(round(x))` when `round(x)` already returns an `int`).
- Add/remove type annotations consistently with the repo’s style (don’t introduce isolated type hints that the rest of the file/project doesn’t follow).

Example (readable conditional print):
```python
print_grad_norm = ""
if grad_clip > 0.0:
    print_grad_norm = f"grad_norm: {grad_norm.item():.5f} | "

print0(
    f"step {step:05d}/{num_iterations:05d} ({pct_done:.2f}%) | "
    f"loss: {debiased_smooth_loss:.6f} | "
    f"{print_grad_norm}"
    f"lrm: {lrm:.2f} | dt: {dt * 1000:.2f}ms | tok/sec: {tok_per_sec:,} | "
    f"mfu: {mfu:.2f} | total time: {total_training_time/60:.2f}m"
)
```

Example (Path composition):
```python
checkpoints_dir = base_dir / model_dir  # when base_dir is a Path
lock_path = file_path.with_name(f"{file_path.name}.lock")
```