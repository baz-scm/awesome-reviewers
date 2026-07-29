---
title: Accurate Recovery Error Handling
description: 'Coding standard for recovery/error paths: make failure and recovery
  behavior truthful, gated, and user-consistent.


  Apply this rule set:

  1) Ground messages and state on authoritative runtime outcomes (avoid predicates/flags
  that can drift from behavior). If the only way to know is to attempt (e.g., reset/clear),
  attempt and then report based on the result.'
repository: aaif-goose/goose
label: Error Handling
language: Rust
comments_count: 10
repository_stars: 51876
---

Coding standard for recovery/error paths: make failure and recovery behavior truthful, gated, and user-consistent.

Apply this rule set:
1) Ground messages and state on authoritative runtime outcomes (avoid predicates/flags that can drift from behavior). If the only way to know is to attempt (e.g., reset/clear), attempt and then report based on the result.
2) Choose degradation vs failure by comparing which one is less misleading to the user/UI.
   - If returning Err would claim an operation failed but the system state/token accounting already advanced (or would be irrecoverably misleading), prefer best-effort + warn.
3) Retry only when it won’t produce incoherent duplication.
   - Gate retries on cancellation and on whether any visible assistant content already streamed (text/reasoning/images). If something was already shown, surface the error instead of retrying.
   - If a higher-level retry mechanism (e.g., recipe retry) is present, let it own the turn; don’t shadow it with generic retry/fallback.
   - Add bounded retries for ambiguous/empty provider responses, and after the bound, surface a concrete user-visible message (never silently end).
4) Keep the “surface” and “persist” paths aligned.
   - Don’t mutate hidden conversation buffers without also yielding/saving the same message the user should see.
5) When parsing/transforming (e.g., tool arguments), use strict parse first.
   - Never silently repair data that may be truncated; detect truncation and return/route an actionable error with guidance.

Illustrative pattern (retry gating + bounded empty fallback):
```rust
if provider_errored || cancel_token.is_cancelled() {
    surface_error(provider_err);
    return;
}

let visible_content_streamed = last_assistant_text_not_empty || surfaced_thinking_in_turn || streamed_images;
if visible_content_streamed {
    // Avoid duplicate/incoherent resend.
    surface_error(provider_err);
    return;
}

let empty_response = no_tools_called && last_assistant_text.is_empty();
if empty_response {
    if empty_turn_retries < MAX_EMPTY_TURN_RETRIES {
        empty_turn_retries += 1;
        warn!("Empty provider response; retrying {}/{}", empty_turn_retries, MAX_EMPTY_TURN_RETRIES);
        messages_to_add.clear(); // don’t persist empty turn
        continue;
    }
    // After retries, surface a real message.
    let msg = Message::assistant().with_text(EMPTY_TURN_MESSAGE);
    yield AgentEvent::Message(msg.clone());
    messages_to_add.push(msg);
}
```
