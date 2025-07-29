---
title: comprehensive validated examples
description: Documentation examples should be self-sufficient, comprehensive, and
  use proper syntax tags to enable automated validation. Examples must include all
  necessary context and demonstrate multiple related features rather than isolated
  snippets. Use `v` syntax tags instead of generic ones like `codeblock` to ensure
  examples are validated by `v check-md` during...
repository: vlang/v
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 36582
---

Documentation examples should be self-sufficient, comprehensive, and use proper syntax tags to enable automated validation. Examples must include all necessary context and demonstrate multiple related features rather than isolated snippets. Use `v` syntax tags instead of generic ones like `codeblock` to ensure examples are validated by `v check-md` during CI, keeping them current and consistent.

For example, instead of a minimal snippet:
```v
ch.try_push(42)
```

Provide a complete, informative example:
```v
ch := chan int{cap: 2}
println(ch.try_push(42)) // `.success` if pushed, `.not_ready` if full, `.closed` if closed
println(ch.len) // Number of items in the buffer
println(ch.cap) // Buffer capacity
println(ch.closed) // Whether the channel is closed
```

This approach makes examples immediately usable for learning and ensures they remain valid through automated testing, while providing comprehensive coverage of related functionality.