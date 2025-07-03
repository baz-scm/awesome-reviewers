---
title: Minimize public API surface
description: Design APIs with a minimal public surface area by carefully controlling
  which methods and properties are exposed. Start with a restricted set of public
  methods and expand only when there's clear evidence of need. This approach makes
  APIs easier to maintain and evolve while reducing the risk of breaking changes.
repository: rails/rails
label: API
language: Ruby
comments_count: 6
repository_stars: 57027
---

Design APIs with a minimal public surface area by carefully controlling which methods and properties are exposed. Start with a restricted set of public methods and expand only when there's clear evidence of need. This approach makes APIs easier to maintain and evolve while reducing the risk of breaking changes.

Key principles:
- Expose only methods that are essential for client usage
- Prefer specific, focused public methods over general-purpose ones
- Document the rationale for making methods public

Example:
```ruby
class ErrorReporter
  # BAD: Exposing internal state directly
  attr_accessor :context_middlewares

  # GOOD: Controlled public interface
  def add_middleware(&block)
    context_middlewares << block
  end

  private
    attr_reader :context_middlewares
end
```

When adding new public methods, consider:
1. Is this functionality truly needed by API consumers?
2. Could this be implemented using existing public methods?
3. Are we prepared to support this method long-term?

Remember: It's easier to add methods later than to remove them, as removal requires a deprecation cycle.
