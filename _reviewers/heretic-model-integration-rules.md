---
title: Model integration rules
description: When adding or changing model loading, quantization, LoRA/abliteration
  logic, or merging behavior, follow these explicit rules to ensure correctness, compatibility
  and reproducibility.
repository: p-e-w/heretic
label: AI
language: Python
comments_count: 16
repository_stars: 5002
---

When adding or changing model loading, quantization, LoRA/abliteration logic, or merging behavior, follow these explicit rules to ensure correctness, compatibility and reproducibility.

1) Explicit quantization and dtype handling
- Provide a single helper that builds BitsAndBytesConfig from settings and the chosen dtype. For 4-bit require an explicit compute dtype (e.g., torch.bfloat16) and document why (bnb dequantizes to compute_dtype each forward).
- Print clear messages when a model is loaded in 4/8-bit and when compute_dtype is chosen.
- Keep a documented dtype cascade (e.g., ["auto","float16","bfloat16","float32"]) and explain fallback rationale in code comments.

Example:
quant_cfg = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16, ...)

2) LoRA adapter configuration and scaling
- Store/reuse a single peft_config object rather than duplicating LoRA construction logic.
- If you compute target weight deltas directly (instead of training), set lora_alpha == r to avoid extra scaling: lora_alpha must equal LoRA rank so alpha/r == 1.
- Initialize PEFT with explicit targets (leaf names) and document that extra adapters on unrelated modules are harmless if unused.

3) Row normalization / magnitude preservation modes
- Expose an enum (NONE/PRE/FULL) and implement each mode explicitly:
  - PRE: apply row norms to LoRA_B so adapters act on original W
  - FULL: apply update, normalize rows, restore original row norms, compute delta, then extract low-rank approximation via svd_lowrank
  - NONE: apply low-rank update directly
- When forming LoRA components from SVD, balance singular values across A and B for numerical stability (e.g., use sqrt(S) into both sides) and document why.

Snippet (FULL flow outline):
W = W_org.view(W.shape[0], -1)
W = W + lora_B @ lora_A
W = F.normalize(W, p=2, dim=1)
W = W * W_row_norms
W = W - W_org
U, S, Vh = torch.svd_lowrank(W, q=2*r+4)
# split sqrt(S) across U and V
lora_B = U[:, :r] @ diag(sqrt_S)
lora_A = diag(sqrt_S) @ Vh[:r, :]

4) Compatibility & hybrid fallback
- When inspecting model layers, unwrap PeftModel (e.g., model.base_model.model) to find language layers.
- Use a hybrid path: if a module has LoRA adapters (hasattr(module, 'lora_A')), perform LoRA-based abliteration; otherwise fall back to direct weight modification on nn.Parameter tensors. This ensures support for non-standard implementations (e.g., GPT-OSS) without breaking standard models.
- Flatten weight matrices for conv/4D tensors to (out_features, in_features) when constructing LoRA components, so LoRA storage matches PEFT expectations.

5) Safe merging for quantized models
- Before merging adapters into a quantized model, copy adapter parameters to CPU:
adapter_state = {name: param.data.clone().cpu() for name, param in peft_model.named_parameters() if 'lora_' in name}
- Reload base model on CPU (device_map='cpu', appropriate torch_dtype), create a peft wrapper with the same peft_config, copy adapter_state into it, then call merge_and_unload() on that CPU model. Warn users about memory usage and provide an "adapter-only" save option.
- After merge_and_unload, mark that the running process may need a full reload if further LoRA operations are expected.

6) Data processing and diagnostics
- Implement winsorization/clamping per-layer (and per-prompt if desired) but document axes and intent clearly. Add explanatory comments in code about the chosen axis.
- Avoid redundant safety guards that mask underlying bugs (e.g., negative KL indicates a calculation bug and should not be silently clamped).

7) UX, tests, and diagnostics
- Prompt users clearly when requiring trust_remote_code; set trusted_models[model] only after a successful load that required confirmation.
- Enumerate all detected devices (GPU count and names) for clearer logs.
- Use small toy models in unit/CI tests to avoid large downloads and flakiness.

Why this matters (motivation)
- Generative AI stacks mix many moving parts: quantization, PEFT/LoRA, architecture variations (modules vs raw parameters), and numerical normalization. Making integration rules explicit prevents subtle bugs (incorrect scaling, broken merges, unsupported layers), ensures reproducible experiments, and avoids user/system-level failures (OOM during CPU merges).

References: discussions about LoRA scaling, normalization and merging, quantization config and compute dtype, hybrid compatibility and PEFT unwrapping, winsorization axis and testing guidance (see source discussions).