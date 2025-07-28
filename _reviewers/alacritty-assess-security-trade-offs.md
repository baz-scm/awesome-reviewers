---
title: Assess security trade-offs
description: When introducing dependencies or features that have security implications,
  explicitly evaluate whether the benefits justify the potential risks. Prefer safer
  alternatives when available, and clearly document security considerations.
repository: alacritty/alacritty
label: Security
language: Other
comments_count: 2
repository_stars: 59675
---

When introducing dependencies or features that have security implications, explicitly evaluate whether the benefits justify the potential risks. Prefer safer alternatives when available, and clearly document security considerations.

For dependencies, favor native implementations over transpiled code from memory-unsafe languages. For example, choose a "small safe rust parser" over a "massive transpilation of a C library" that could introduce security vulnerabilities.

For features that access system resources (like clipboard, filesystem, network), be explicit about potential abuse scenarios in documentation. Instead of downplaying risks with phrases like "not that necessary," clearly state that "allowing any application to read from the clipboard can be easily abused while not providing significant benefits."

Always consider: Does this dependency/feature introduce unnecessary attack surface? Are there safer alternatives? Have we clearly communicated the security implications to users?