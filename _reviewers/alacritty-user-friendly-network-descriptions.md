---
title: User-friendly network descriptions
description: When documenting network-related features like URL handling, hyperlinks,
  or web protocols, prioritize user-understandable descriptions over technical implementation
  details. Users care about what functionality they gain, not the internal mechanics
  of how it works.
repository: alacritty/alacritty
label: Networking
language: Markdown
comments_count: 2
repository_stars: 59675
---

When documenting network-related features like URL handling, hyperlinks, or web protocols, prioritize user-understandable descriptions over technical implementation details. Users care about what functionality they gain, not the internal mechanics of how it works.

Instead of technical descriptions like "Removal of characters before the URL scheme now take UTF8 byte sizes into account", use user-focused language like "Unicode characters at the beginning of URLs are now ignored". This helps users understand the practical impact of network-related changes.

For network protocol features, focus on the capability being added rather than the protocol specifics. For example, "Escape sequence to set hyperlinks" is clearer than detailing the exact OSC sequence format in user-facing documentation.