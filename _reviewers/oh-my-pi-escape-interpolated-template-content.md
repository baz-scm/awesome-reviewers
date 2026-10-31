---
title: Escape interpolated template content
description: When building structured templates that embed untrusted or dynamically
  generated content (e.g., model output inserted into tag-delimited LLM prompts, or
  user input inserted into HTML/XML), always escape special characters before interpolation.
  Failing to do so lets the embedded content break out of its intended boundary—closing
  a wrapper tag and injecting...
repository: can1357/oh-my-pi
label: Security
language: Markdown
comments_count: 1
repository_stars: 37317
---

When building structured templates that embed untrusted or dynamically generated content (e.g., model output inserted into tag-delimited LLM prompts, or user input inserted into HTML/XML), always escape special characters before interpolation. Failing to do so lets the embedded content break out of its intended boundary—closing a wrapper tag and injecting new instructions or markup—enabling prompt-injection or markup-injection attacks.

Apply an escaping function (e.g., `escapeXml`/`escapeHtml`) to any variable substituted into a tagged template, and add a regression test that feeds a payload containing the delimiter sequence (e.g., a closing tag) to verify it is rendered as literal text and the surrounding wrapper tags appear exactly once.

Example fix:
```
<work-already-shown>
{{escapeXml partialText}}
</work-already-shown>
```
Never interpolate raw, untrusted text directly into prompt or markup templates—escape it first so it cannot terminate the enclosing tag or inject a new `<system-injection>`-style directive.</description>
</invoke>
