---
title: Optimization algorithm compatibility
description: When implementing or changing optimization code (samplers, objectives,
  and result selection), ensure algorithmic correctness, preserve sampler assumptions,
  and prefer explicit post-processing over ad‑hoc objective hacks.
repository: p-e-w/heretic
label: Algorithms
language: Python
comments_count: 5
repository_stars: 5002
---

When implementing or changing optimization code (samplers, objectives, and result selection), ensure algorithmic correctness, preserve sampler assumptions, and prefer explicit post-processing over ad‑hoc objective hacks.

Why: Incorrect assumptions about samplers, unclear trial counting, off-by-one indexing, or hidden objective tweaks can silently break search quality or produce confusing results. The rule reduces bugs and makes behavior auditable.

Checklist (practical actions):
- Validate sampler constraints before changing parameter conditioning
  - If using multivariate TPE, avoid introducing conditional/variable-range params that the sampler does not support, or adjust sampler options (e.g., grouping) deliberately and consistently.
  - Example: do not move from unconditional sampling to conditional sampling without ensuring the sampler remains valid.

- Compute trial counts and statuses in one clear place
  - Count completed trials once and use that to adjust remaining trials rather than maintaining ad-hoc "extra" counters.
  - Example:
    completed_trials = [t for t in study.trials if t.state == TrialState.COMPLETE]
    remaining = max(0, desired_n_trials - len(completed_trials))

- Don't change the objective to fix selection/display issues; post-process instead
  - Keep the objective function simple and theoretically justified. If the Pareto/front presentation shows ties or ambiguity, resolve those when selecting best trials rather than altering the objective scoring.
  - Example post-processing (derive Pareto front from completed trials):
    sorted_trials = sorted(
        completed_trials,
        key=lambda t: (t.user_attrs['refusals'], t.user_attrs['kl_divergence'])
    )
    best = []
    min_div = float('inf')
    for t in sorted_trials:
        kld = t.user_attrs['kl_divergence']
        if kld < min_div:
            min_div = kld
            best.append(t)

- Be explicit about indexing and distances (avoid fenceposts)
  - When expressing distances or ranges over indices, document whether you mean count (n) or last index (n-1). Prefer using clear names (num_layers, last_layer_index) and compute derived values using the correct base.
  - Example: if n = number of layers, largest index distance = n - 1; use 0.6 * (n - 1) if you intend a fraction of the index span.

- Prefer simple, well-justified changes over complex heuristics
  - If smoothing or interpolation is proposed to "improve" optimizer behavior, require theoretical justification or strong, reproducible experimental evidence; prefer linear/simple approaches and clearly note any new tuning parameters.

When to apply: any change touching sampling logic, objective computation, trial bookkeeping, or final selection of best trials. Following this guidance improves correctness, reproducibility, and debuggability of optimization code.