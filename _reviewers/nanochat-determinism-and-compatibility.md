---
title: Determinism and compatibility
description: When working on LLM inference/engines, ensure (1) determinism tests actually
  test the intended invariants, (2) optional GPU-accelerated kernels are only loaded
  when the hardware supports them (with a safe fallback), and (3) KV-cache shape assumptions
  are documented accurately.
repository: karpathy/nanochat
label: AI
language: Python
comments_count: 3
repository_stars: 53189
---

When working on LLM inference/engines, ensure (1) determinism tests actually test the intended invariants, (2) optional GPU-accelerated kernels are only loaded when the hardware supports them (with a safe fallback), and (3) KV-cache shape assumptions are documented accurately.

- Determinism tests: structure assertions so the generation invariants change *only* by the parameters you intend.
  - Example (temperature=0 should ignore randomness; outputs should match across different seeds for the same prompt):
    ```python
    prompt = [261, 72, 101, 108, 108, 111]
    engine = Engine(MockModel(), ByteTokenizer())

    r1, _ = engine.generate_batch(prompt, temperature=0.0, max_tokens=5, seed=1)
    r2, _ = engine.generate_batch(prompt, temperature=0.0, max_tokens=5, seed=42)
    r3, _ = engine.generate_batch(prompt, temperature=0.0, max_tokens=5, seed=123)
    assert r1 == r2 == r3
    ```

- Hardware compatibility: gate kernel loading by compute capability to avoid runtime “no kernel image” crashes; optionally fall back to a compatible import/wheel.
  - Example:
    ```python
    flash_attn = None
    if torch.cuda.is_available():
        if torch.cuda.get_device_capability()[0] >= 9:
            flash_attn = get_kernel('varunneal/flash-attention-3').flash_attn_interface
        else:
            import flash_attn_interface as flash_attn  # fallback
    ```

- KV-cache invariants: ensure assertions/comments match the real dimension constraints used by prefill/attention (e.g., remove incorrect dimension references and explicitly note fixed indices like the K/V pair dimension when applicable).