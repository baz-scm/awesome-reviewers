---
title: Use proper URI parsing
description: When working with URLs and URIs in networking code, use proper URI parsing
  libraries and types instead of string manipulation or regex validation. This approach
  is more robust, handles edge cases correctly, and provides better type safety.
repository: semgrep/semgrep
label: Networking
language: Other
comments_count: 2
repository_stars: 12598
---

When working with URLs and URIs in networking code, use proper URI parsing libraries and types instead of string manipulation or regex validation. This approach is more robust, handles edge cases correctly, and provides better type safety.

Instead of using regex patterns like `^https?://` to validate URLs, use the URI library's parsing capabilities:

```ocaml
(* Avoid this *)
let url_regex = Pcre2_.regexp "^https?://"
let is_url config_path = Pcre2_.pmatch_noerr ~rex:url_regex config_path

(* Prefer this *)
let is_url config_path =
  match Option.bind Uri.scheme (of_string_opt config_path) with
  | Some "http"
  | Some "https" -> true
  | Some _
  | None -> false
```

Additionally, use `Uri.t` types instead of strings when representing URLs or URIs in function signatures and data structures. This makes the intent clearer and leverages the type system to catch errors at compile time.