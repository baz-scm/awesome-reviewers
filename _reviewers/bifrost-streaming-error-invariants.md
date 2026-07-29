---
title: Streaming error invariants
description: 'Adopt a single, consistent error-handling strategy for streaming (and
  other multi-step flows): define retry semantics, tolerate isolated decode/parse
  errors, enforce terminal/completion invariants, and preserve the failure context
  needed by downstream billing/logging.'
repository: maximhq/bifrost
label: Error Handling
language: Go
comments_count: 8
repository_stars: 6862
---

Adopt a single, consistent error-handling strategy for streaming (and other multi-step flows): define retry semantics, tolerate isolated decode/parse errors, enforce terminal/completion invariants, and preserve the failure context needed by downstream billing/logging.

Guidelines:
1) Classify failures at the I/O boundary
- Treat “request failed before the first response byte” as a retriable upstream connection error (so retry logic can kick in). Avoid treating it as a terminal provider/operation failure.

2) Streaming: log-and-continue for local frame issues
- If a single SSE event/chunk is malformed (unmarshal/base64 decode), log and skip that event instead of aborting the whole stream.

3) Streaming: enforce completion invariants
- Don’t assume EOF implies success.
- If the protocol defines a terminal marker (e.g., Cartesia’s `done` event), surface an error when the terminal marker is never observed.

4) Preserve context on ALL error paths
- Before returning errors, attach provider response headers and any accumulated usage/billing data to the error object so post-hooks can charge and trace correctly.

5) Async safety: prevent unrecoverable panics in teardown goroutines
- Any goroutine that can outlive the request (idle timers, readers, cancellation helpers) must be crash-safe (recover panics inside the goroutine if the panic would otherwise be unrecoverable).

Example pattern (Go, streaming):
```go
// Local helper: attach billed usage accumulated in-context to the error.
func attachBilledUsageFromContext(ctx *schemas.BifrostContext, bifrostErr *schemas.BifrostError) {
  usage, ok := ctx.Value(schemas.BifrostContextKeyStreamAccumulatedUsage).(*schemas.BifrostLLMUsage)
  if !ok || usage == nil { return }
  if usage.PromptTokens == 0 && usage.CompletionTokens == 0 && usage.TotalTokens == 0 { return }
  // Important: copy or snapshot if usage will be mutated later.
  u := *usage
  bifrostErr.ExtraFields.BilledUsage = &u
}

// Inside stream read loop:
var sawDone bool
for {
  data, err := sseReader.ReadDataLine()
  if err != nil {
    if errors.Is(err, io.EOF) {
      break
    }
    // pre-first-byte / upstream classification happens at the Do() boundary,
    // but for mid-stream read errors, enrich and send.
    e := providerUtils.NewBifrostOperationError("stream read failed", err)
    attachBilledUsageFromContext(ctx, e)
    providerUtils.ProcessAndSendBifrostError(ctx, postHookRunner, e, responseChan, logger, postHookSpanFinalizer)
    return
  }

  var evt CartesiaSSEEvent
  if err := sonic.Unmarshal(data, &evt); err != nil {
    logger.Warn("Failed to parse SSE event: %v", err)
    continue // log-and-continue
  }

  switch evt.Type {
  case "done":
    sawDone = true
    // optionally process done payload
  case "chunk":
    if evt.Data == "" { continue }
    audio, decErr := base64.StdEncoding.DecodeString(evt.Data)
    if decErr != nil {
      logger.Warn("Failed to decode chunk: %v", decErr)
      continue // keep stream alive on single chunk decode errors
    }
    // send delta chunk...
  case "error":
    // surface terminal provider error
    e := providerUtils.NewBifrostOperationError("cartesia stream error: "+evt.Error, nil)
    attachBilledUsageFromContext(ctx, e)
    providerUtils.ProcessAndSendBifrostError(ctx, postHookRunner, e, responseChan, logger, postHookSpanFinalizer)
    return
  }

  if sawDone { break }
}

// Terminal-invariant guard: EOF without terminal done is truncated.
if !sawDone {
  ctx.SetValue(schemas.BifrostContextKeyStreamEndIndicator, true)
  e := providerUtils.NewBifrostOperationError("stream ended before terminal done", io.ErrUnexpectedEOF)
  attachBilledUsageFromContext(ctx, e)
  providerUtils.ProcessAndSendBifrostError(ctx, postHookRunner, e, responseChan, logger, postHookSpanFinalizer)
  return
}
```

This standard prevents: (a) “empty success” on truncated streams, (b) missing bills/trace data on cancellation/timeout, (c) inconsistent retry behavior, and (d) process crashes from panics in goroutines used for stream teardown/timeouts.