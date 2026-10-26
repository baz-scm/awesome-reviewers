---
title: Observability Signal Quality
description: 'When changing or adding metrics/traces, make signals stable, accurate,
  and alert-friendly.


  **Apply these rules before submitting:**


  1) **Preserve metric semantics and document scope**'
repository: kUbernetes/kUbernetes
label: Observability
language: Go
comments_count: 9
repository_stars: 128688
---

When changing or adding metrics/traces, make signals stable, accurate, and alert-friendly.

**Apply these rules before submitting:**

1) **Preserve metric semantics and document scope**
- If a metric is already used for dashboards/alerts, avoid changing what it counts (e.g., whole resource vs only a rolling-update range). If scope must change, either keep the original metric meaning and add a new metric, or add tests that lock semantics.

2) **Use the right labeling approach (avoid redundant series)**
- Prefer a single counter with a `status/result` label when the values are the same logical event (e.g., complete vs incomplete vs error), rather than adding many separate counters.
- Ensure label values reflect the real operation phase (e.g., “terminating” vs “kill” vs “sync”), or queries/alerts will misclassify failures.
- Keep label sets non-redundant and bounded (avoid unnecessary “translated vs tunneled” style duplication unless it’s truly distinct).

3) **Suppress expected/noisy error increments**
- Do not increment “error” metrics for failures that are expected and handled via retry/backoff/crashloop/image-pull-backoff behavior unless you intentionally want node-level alerting noise.
- If you can’t reliably detect retries, at least skip categories that are effectively part of normal backoff loops.

4) **Design duration histograms from meaningful timestamps**
- Choose bucket granularity based on the measurement origin and real variability. If sub-second buckets only capture timestamp truncation noise, drop them or change the start time to something stable (e.g., controller-observed time rather than serialized creation timestamps).

5) **For tracing: always propagate the provided context**
- When starting spans in request/worker flows, use the incoming `ctx` as the parent (don’t start from `context.Background()`), so nested spans are correctly correlated.

**Example pattern (metrics + context propagation):**
```go
func (h *handler) Sync(ctx context.Context, req *Request) {
    // Tracing: use ctx as parent
    ctx, span := h.tracer.Start(ctx, "syncRequest")
    defer span.End()

    // Metrics: measure from a meaningful point
    start := time.Now() // or a controller-observed timestamp

    result := doWork(req)

    // Error metrics: gate expected backoff/retry cases
    if result.Err != nil && !isExpectedBackoff(result.Err) {
        metrics.SyncErrorsTotal.WithLabelValues("sync").Inc()
    }

    // Duration: buckets should match the resolution/intent
    metrics.RequestProcessingDurationSeconds.Observe(time.Since(start).Seconds())
}
```

Following these rules keeps dashboards stable, prevents alert fatigue, and ensures traces and metrics can be trusted together.