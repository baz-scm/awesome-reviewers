---
title: Fail Safe Input Handling
description: When processing security-relevant external inputs (URIs/hosts, file paths/content,
  auth tokens, and tool-call metadata), validate and constrain early, then ensure
  failure modes are non-recoverable in ways that could cause retries or duplicate
  effects.
repository: aaif-goose/goose
label: Security
language: Rust
comments_count: 6
repository_stars: 51876
---

When processing security-relevant external inputs (URIs/hosts, file paths/content, auth tokens, and tool-call metadata), validate and constrain early, then ensure failure modes are non-recoverable in ways that could cause retries or duplicate effects.

Apply this pattern:
1) Validate trust boundaries
- Enforce scheme/host allowlists (e.g., only HTTPS; host must match or be a subdomain of the discovery target).
- Normalize/parse rather than rely on raw string equality.
- Verify OAuth/token/discovery endpoints and auth state; never accept mismatched state.

2) Constrain filesystem operations
- Accept only regular files (reject FIFOs/symlink tricks); canonicalize then re-check via metadata on opened descriptors.
- Enforce byte limits with bounded reads (read at most limit+1 and error if exceeded).
- Copy/write only after validation; on failure, remove partial destinations and set restrictive permissions.

3) Make tool execution idempotent and policy-deny non-retryable
- Require tool_call_id uniqueness per session/turn; deduplicate repeated provider tool requests before execution.
- When a plugin denies a tool call, return a failure that does NOT use retry-friendly error semantics (avoid INVALID_REQUEST-style “fix and retry” behavior). Prefer representing the denial as a tool result/error that the model treats as final, not a malformed request.

4) Use safe auth handling
- Compare secrets/tokens in constant time.
- For websocket auth, validate the expected auth protocol/subprotocol and also accept only properly extracted bearer tokens.

Example (pattern sketch):
```rust
// 1) Constant-time token check
fn tokens_equal_ct(expected: &str, actual: &str) -> bool {
    expected.as_bytes().ct_eq(actual.as_bytes()).into()
}

// 2) Bounded read after regular-file validation
const MAX: u64 = 1024 * 1024;
fn read_bounded(mut f: std::fs::File) -> Result<Vec<u8>, anyhow::Error> {
    let mut buf = Vec::new();
    f.take(MAX + 1).read_to_end(&mut buf)?;
    if (buf.len() as u64) > MAX {
        anyhow::bail!("file exceeds limit");
    }
    Ok(buf)
}

// 3) Policy denial should not invite retries
// Prefer a “final tool outcome” representation over returning an MCP Err
// that could trigger a retry path.
fn deny_tool_call_final(plugin: &str, reason: &str) -> ToolCallResult {
    ToolCallResult { is_error: true, final_message: format!("blocked by {plugin}: {reason}") }
}
```

Net: validate/normalize untrusted inputs at the boundary, strictly limit side effects (IO size/type, tool execution), use constant-time auth comparisons, and make authorization/policy denials non-retryable to prevent retry storms or duplicate execution.