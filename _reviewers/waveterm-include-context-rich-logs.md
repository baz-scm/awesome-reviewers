---
title: Include context-rich logs
description: 'Ensure logs are actionable: always include relevant context identifiers
  (e.g., full connection name, user or request id) and log any returned errors so
  failures are visible and debuggable. Mask or redact sensitive fields when necessary
  and choose an appropriate log level (info for status changes, warn/error for failures).'
repository: wavetermdev/waveterm
label: Logging
language: Go
comments_count: 2
repository_stars: 17328
---

Ensure logs are actionable: always include relevant context identifiers (e.g., full connection name, user or request id) and log any returned errors so failures are visible and debuggable. Mask or redact sensitive fields when necessary and choose an appropriate log level (info for status changes, warn/error for failures).

How to apply:
- Add identifying context to messages that describe operations or failures so developers and users can trace what happened. Example: include conn.GetName() in connect errors.
- Always capture and log errors returned from helpers and background goroutines instead of ignoring them.
- If a value could be sensitive or overly verbose, mask or redact the sensitive portion before logging.
- Prefer structured logging where available (fields for name, id, error) to aid searching and aggregation.

Code examples (pattern to follow):

// include full connection name and log error
if err := conn.Connect(ctx, connFlags); err != nil {
    // show identifying context and the error
    log.Printf("error connecting to %q (status=%q): %v", conn.GetName(), conn.GetStatus(), err)
    return fmt.Errorf("cannot connect to %q when status is %q: %w", conn.GetName(), conn.GetStatus(), err)
}

// always log helper errors and goroutine results
err := setNoReleaseCheck(ctx, clientData, false)
if err != nil {
    log.Printf("failed updating client no-release-check for client=%q: %v", clientData.ClientID, err)
    return err
}

go func() {
    if err := releasechecker.CheckNewRelease(false); err != nil {
        log.Printf("background release check failed: %v", err)
    }
}()

Notes:
- Use appropriate log levels (error/warn/info) and structured fields where possible.
- Redact sensitive values (tokens, passwords) before logging; prefer logging stable identifiers (ids, names) instead of secrets.
- Logging errors promptly (including from goroutines) prevents silent failures and improves operability.