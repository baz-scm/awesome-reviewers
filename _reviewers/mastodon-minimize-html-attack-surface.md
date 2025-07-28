---
title: Minimize HTML attack surface
description: When allowing HTML attributes or rendering user-generated content, explicitly
  limit the attack surface by restricting allowed properties to a minimal, vetted
  set rather than permitting broad categories of attributes.
repository: mastodon/mastodon
label: Security
language: Ruby
comments_count: 2
repository_stars: 48691
---

When allowing HTML attributes or rendering user-generated content, explicitly limit the attack surface by restricting allowed properties to a minimal, vetted set rather than permitting broad categories of attributes.

The principle is to be conservative about what HTML/CSS properties you allow, as even "safe" attributes can introduce vulnerabilities or increase the attack surface significantly. When sanitizing HTML, prefer explicit allow-lists of specific properties over general categories.

Example of problematic approach:
```ruby
# Risky - allows all style attributes
'iframe' => %w(allowfullscreen height scrolling src style width)
```

Better approach:
```ruby
# Safer - explicit property restrictions
css: {
  properties: ['border']  # Only allow specific, vetted CSS properties
}

# Or avoid style attributes entirely when possible
'iframe' => %w(allowfullscreen height scrolling src width)
```

When rendering user content like markdown, ensure proper sanitization is applied and be cautious with html_safe usage. If you're unsure about the safety of rendering user input, err on the side of caution and seek additional review for HTML/CSS attribute additions.