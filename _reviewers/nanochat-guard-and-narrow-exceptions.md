---
title: Guard and narrow exceptions
description: 'When an operation can fail in a known way (edge-case inputs, risky math,
  I/O/parsing, optional capabilities), handle it explicitly:

  - Add targeted guards before risky computations (e.g., avoid dividing/normalizing
  by an empty denominator).'
repository: karpathy/nanochat
label: Error Handling
language: Python
comments_count: 7
repository_stars: 53189
---

When an operation can fail in a known way (edge-case inputs, risky math, I/O/parsing, optional capabilities), handle it explicitly:
- Add targeted guards before risky computations (e.g., avoid dividing/normalizing by an empty denominator).
- Use narrow exception handling for the *actual* API you call (don’t add `except Exception` that unintentionally swallows the error you meant to surface).
- On failure, clean up partial/corrupted artifacts so the next run can retry, and prefer graceful recovery (skip/continue, warn+cap) when continuing is safe.

Example (defensive guard + clean recovery):
```python
num_tokens = torch.tensor(0, device=device)
steps = [next(train_loader) for _ in range(grad_accum_steps)]
num_tokens += sum((targets >= 0).sum() for _, targets in steps)

# (optional) sync across ranks
if ddp:
    dist.all_reduce(num_tokens, op=dist.ReduceOp.SUM)

# prevent NaN loss
if num_tokens.item() == 0:
    model.zero_grad(set_to_none=True)
    # skip this accumulation window
    return

for train_inputs, train_targets in steps:
    loss = model(train_inputs, train_targets, loss_reduction='sum')
    loss = loss / num_tokens
    loss.backward()
```

Example (don’t swallow intended errors):
```python
# WRONG: throws, then immediately swallows everything
try:
    raise RuntimeError("something important")
except Exception:
    pass

# RIGHT: either remove the throw/silencing, or narrow the exception
try:
    import torch._dynamo
    if torch._dynamo.is_compiling():
        raise RuntimeError("RoPE cache too small during torch.compile")
except ImportError:
    # only ignore the missing module case
    pass
```

Example (cleanup on integrity failure):
- If checksum verification fails, delete the bad file (and optionally the temp file), then retry or fail cleanly—don’t leave a corrupt artifact that prevents future re-download/re-verify.

Apply this consistently across training loops, dataset download/verification, and state load paths.