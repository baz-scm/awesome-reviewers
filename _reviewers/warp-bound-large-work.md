---
title: Bound Large Work
description: When code performs expensive IO/compute or reacts to frequent events,
  (1) gate side effects to meaningful state changes, (2) bound or chunk large inputs/outputs
  before allocation or heavy processing, and (3) cache/share to avoid repeated recomputation
  and deep clones.
repository: warpdotdev/warp
label: Performance Optimization
language: Rust
comments_count: 8
repository_stars: 56893
---

When code performs expensive IO/compute or reacts to frequent events, (1) gate side effects to meaningful state changes, (2) bound or chunk large inputs/outputs before allocation or heavy processing, and (3) cache/share to avoid repeated recomputation and deep clones.

Apply this standard:
- Event-driven gating: only do PTY/UI work when the result would actually change (e.g., dark/light classification changed), and prefer granular events or unsubscribe once the relevant phase is reached.
- Input bounding: add explicit max sizes and reject early (prefer stat-first) before reading entire payloads; for media/file inspection, sniff only a small prefix rather than loading whole files.
- Large IO chunking: when a subsystem has practical buffer limits (e.g., PTY proxy), write in conservative chunk sizes with appropriate delays.
- Computation caps: before expensive semantic/entity processing, skip for known large/unsupported cases and cap content size.
- Avoid repeated expensive rebuilds/clones: use caching to avoid per-frame data-structure rebuilds and use Arc (or similar sharing) for expensive-to-clone payloads.

Example patterns (adapt as needed):
```rust
// 1) Gate side effects on meaningful state changes.
let is_dark = theme.inferred_color_scheme() == ColorScheme::LightOnDark;
let should_notify = {
    let mut model = self.model.lock();
    let changed = model.is_dark_mode() != is_dark;
    model.update_colors(colors);
    model.set_color_scheme(is_dark);
    changed && model.is_term_mode_set(TermMode::DARK_LIGHT_NOTIFICATIONS)
};
if should_notify {
    self.write_to_pty(format!("\x1b[?997;{}n", if is_dark { 1 } else { 2 }).into_bytes(), ctx);
}

// 2) Chunk large writes for constrained transports.
const CHUNK_SIZE: usize = 4096;
for (i, chunk) in bootstrap_bytes.chunks(CHUNK_SIZE).enumerate() {
    // spawn/send with a small delay if needed to avoid buffer drops
    send_chunk_with_delay(chunk, i * 50, ctx);
}

// 3) Stat-first size cap before reading full payloads.
let meta = std::fs::metadata(&path_str)?;
if meta.len() > MAX_IMAGE_SIZE_BYTES_FOR_CLI_AGENT {
    show_toast(format!("{} is too large", filename), ctx);
    continue;
}

// 4) Prefix-only sniffing.
let prefix = read_prefix(&path, MIME_SNIFF_BYTES)?;
let mime = infer_mime_type(&path, &prefix);

// 5) Compute caps/guards.
let entity_diff = if content_is_small_enough && !is_large_or_unrenderable {
    compute_entity_diff(&content)
} else {
    None
};
```

Result: fewer wasted computations, less memory churn, and fewer correctness/performance issues caused by oversized payloads or high-frequency event handling.