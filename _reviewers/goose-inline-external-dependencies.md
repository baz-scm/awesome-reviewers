---
title: inline external dependencies
description: For security-critical applications, prefer inlining external dependencies
  (JavaScript libraries, CSS frameworks) rather than loading them from CDNs or external
  sources at runtime. This approach eliminates risks from compromised external sources,
  network-based attacks, and supply chain vulnerabilities.
repository: block/goose
label: Security
language: Html
comments_count: 1
repository_stars: 19037
---

For security-critical applications, prefer inlining external dependencies (JavaScript libraries, CSS frameworks) rather than loading them from CDNs or external sources at runtime. This approach eliminates risks from compromised external sources, network-based attacks, and supply chain vulnerabilities.

Inlining dependencies provides "zero risk" by ensuring complete control over the code being executed and removing external attack vectors. This is especially important for core functionality and recommended features that users rely on.

Example:
```html
<!-- Preferred: Inline the minified library -->
<script>
    {{CHART_MIN}}
    // Minified D3.js or other library code here
</script>

<!-- Avoid: External CDN dependency -->
<script src="https://cdn.example.com/d3.min.js"></script>
```

Consider external dependencies acceptable for optional third-party extensions where users make explicit choices about trust, but default to inlined dependencies for built-in functionality.