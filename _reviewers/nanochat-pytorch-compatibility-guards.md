---
title: PyTorch Compatibility Guards
description: Adopt explicit compatibility guards in PyTorch code to prevent silent
  numeric issues and runtime failures across devices, PyTorch versions, and compilation
  modes.
repository: karpathy/nanochat
label: Pytorch
language: Python
comments_count: 4
repository_stars: 53189
---

Adopt explicit compatibility guards in PyTorch code to prevent silent numeric issues and runtime failures across devices, PyTorch versions, and compilation modes.

Apply these rules:
- Explicitly initialize newly introduced parameters/buffers (don’t rely on defaults).
- Feature-detect PyTorch APIs and provide fallbacks for older versions.
- Avoid backend-incompatible tensor ops (e.g., MPS limitations). Use safer construction paths or backend-specific branches.
- If you dynamically grow/update caches/buffers (e.g., RoPE cos/sin), do it lazily, preserve dtype/device, overwrite existing buffers without re-registering names, and guard against mutation during `torch.compile` tracing.

Example pattern (combine the above):

```python
import torch
import torch.nn.functional as F

# 1) Explicit init
# self.smear_lambda is a Parameter or buffer newly added
# Always initialize deterministically.
torch.nn.init.zeros_(self.smear_lambda)

# 2) Version/API fallback

def norm(x):
    if hasattr(F, "rms_norm"):
        return F.rms_norm(x, (x.size(-1),))
    # fallback implementation (placeholder)
    return x * 1.0

# 3) Safe dynamic cache update with compile guard

def ensure_rope_cache(model, needed_seq_len: int, device: torch.device):
    cur_len = model.cos.size(1)
    if needed_seq_len <= cur_len:
        return

    try:
        import torch._dynamo
        if torch._dynamo.is_compiling():
            raise RuntimeError("RoPE cache growth during torch.compile is unsafe; pre-size or disable compile.")
    except Exception:
        pass

    new_len = 1 << (needed_seq_len - 1).bit_length()
    head_dim = model.config.n_embd // model.config.n_head
    cos, sin = model._precompute_rotary_embeddings(seq_len=new_len, head_dim=head_dim, device=device)

    # preserve invariants and overwrite existing registered tensors
    cos = cos.to(dtype=model.cos.dtype, device=device)
    sin = sin.to(dtype=model.sin.dtype, device=device)
    model.cos = cos
    model.sin = sin
```

This standard reduces runtime surprises (especially on MPS), keeps numerics stable when adding parameters, and prevents compilation/tracing issues when using dynamic tensor caches.