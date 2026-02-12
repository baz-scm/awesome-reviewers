---
title: Propagate errors clearly
description: 'Always return and propagate errors; surface them to callers and the
  UI, and clean up resources on error paths.


  Motivation

  - Avoid hiding failures by logging only or encoding errors as special string values.
  Returning errors lets callers decide how to handle, retry, or present failures.
  Ensure resources (files, network streams, conex) are closed with defer...'
repository: wavetermdev/waveterm
label: Error Handling
language: Go
comments_count: 4
repository_stars: 17328
---

Always return and propagate errors; surface them to callers and the UI, and clean up resources on error paths.

Motivation
- Avoid hiding failures by logging only or encoding errors as special string values. Returning errors lets callers decide how to handle, retry, or present failures. Ensure resources (files, network streams, conex) are closed with defer immediately after successful acquisition so early returns and panics don't leak resources.

Rules
- Use idiomatic error returns (value, error). Do not encode errors as sentinel strings in normal return values.
  Example: change parseCopyFileParam(info string) from returning remote=="error" to:
    func parseCopyFileParam(info string) (remote string, path string, err error) {
        if bad { return "", "", fmt.Errorf("bad param: %s", info) }
        return remoteName, path, nil
    }
- Propagate errors upward. Library/logic functions should return errors instead of only logging. Let callers convert errors to user-facing protocol/state or retry.
  Example: instead of log.Printf("Open AI Update packet err: %v"), return the error and let the caller attach it to an update packet or decide recovery.
- Surface errors to the client/UI via explicit fields in protocol/state structures rather than relying on server logs.
  Example: add an Error string (or typed error info) to chat message structs so stream code can send intermediate error messages to the client.
    message := &packet.OpenAICmdInfoChatMessage{Error: err.Error(), MessageID: id}
- Clean up resources on all code paths. After acquiring a resource (file, connection, iterator), call defer Close() immediately.
  Example:
    f, err := os.Open(path)
    if err != nil {
        return err
    }
    defer f.Close()
- Handle errors in loops and streaming paths: when encountering I/O or protocol errors, return or convert the error into a protocol-level update so the UI can display it; avoid silently returning after a log.Printf.

When to log vs return
- Log at top-level handlers where you have context to decide user-visible behavior. Lower-level functions should return errors. Only use log.Printf for unexpected conditions that will be returned/handled at a higher level.

Benefits
- Makes failure handling predictable and testable.
- Enables clients to present useful error information instead of missing failures.
- Prevents resource leaks on error paths.

References: discussions 0, 1, 2, 3.