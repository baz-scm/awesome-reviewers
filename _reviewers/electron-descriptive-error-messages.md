---
title: Descriptive error messages
description: Error messages should be descriptive, contextual, and self-identifying
  to aid debugging and user understanding. Include relevant context like method names,
  parameter values, or identifiers that help locate the source of the error.
repository: electron/electron
label: Error Handling
language: Other
comments_count: 5
repository_stars: 117644
---

Error messages should be descriptive, contextual, and self-identifying to aid debugging and user understanding. Include relevant context like method names, parameter values, or identifiers that help locate the source of the error.

Key principles:
- Make error messages actionable by suggesting workarounds or next steps when possible
- Include context that identifies where the error originated (method name, component, etc.)
- Add relevant parameter values or identifiers to help with debugging
- Use appropriate logging levels (LOG(ERROR) vs DLOG(ERROR)) based on error severity

Examples:

```cpp
// Poor: Generic error without context
LOG(ERROR) << "Unable to initialize logging from handle.";

// Better: Descriptive with context and actionable guidance
LOG(FATAL) << "Unable to open nul device needed for initialization, aborting startup. "
           << "As a workaround, try starting with --" << switches::kNoStdioInit;

// Poor: Missing context
isolate->ThrowException(v8::Exception::Error(
    gin::StringToV8(isolate, "Unknown error")));

// Better: Self-identifying with context
isolate->ThrowException(v8::Exception::Error(
    gin::StringToV8(isolate, "Failed to retrieve target context for world ID: " + std::to_string(world_id))));

// Poor: Generic error
gin_helper::internal::ReplyChannel::Create(isolate, std::move(callback))
    ->SendError("WebContents does not exist");

// Better: Include channel context for debugging
gin_helper::internal::ReplyChannel::Create(isolate, std::move(callback))
    ->SendError("WebContents does not exist for channel: " + channel);
```

This approach transforms cryptic errors into meaningful diagnostics that developers can act upon, reducing debugging time and improving the overall development experience.