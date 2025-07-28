---
title: use optional types safely
description: When functions may not return valid values, use `std::optional` or `absl::optional`
  instead of raw types that could represent invalid states. Always check the validity
  of optional values before accessing them to prevent null pointer dereferences and
  invalid value usage.
repository: electron/electron
label: Null Handling
language: Other
comments_count: 8
repository_stars: 117644
---

When functions may not return valid values, use `std::optional` or `absl::optional` instead of raw types that could represent invalid states. Always check the validity of optional values before accessing them to prevent null pointer dereferences and invalid value usage.

For functions that might fail or return invalid data, prefer optional return types:

```cpp
// Instead of returning 0 or invalid values on failure
std::optional<DWORD> GetAccentColor() {
  // ... implementation that may fail
  if (RegOpenKeyEx(...) != ERROR_SUCCESS) {
    return std::nullopt;  // Explicit failure indication
  }
  return accent_color;
}

// Always check validity before use
std::optional<DWORD> system_accent_color = GetAccentColor();
if (system_accent_color.has_value()) {
  border_color = RGB(GetRValue(system_accent_color.value()),
                     GetGValue(system_accent_color.value()),
                     GetBValue(system_accent_color.value()));
} else {
  should_apply_accent = false;
}
```

For pointer returns, check for null before dereferencing:

```cpp
auto* contents = electron::api::WebContents::From(web_contents);
return contents ? contents->ID() : -1;

// For optional pointers, use both checks
if (frame && frame.value()) {
  auto* frame_rfh = frame->render_frame_host();
  auto* rfh = frame_rfh ? frame_rfh->GetOutermostMainFrameOrEmbedder() : nullptr;
  if (rfh) {
    // Safe to use rfh
  }
}
```

This pattern prevents crashes from accessing invalid pointers or using sentinel values that could lead to unexpected behavior. Note that `base::Optional` has been deprecated in favor of `absl::optional` in newer codebases.