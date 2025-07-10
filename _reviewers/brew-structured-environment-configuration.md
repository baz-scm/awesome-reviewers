---
title: Structured environment configuration
description: Use structured environment variable handling with explicit validation
  instead of directly accessing ENV hash. Implement proper parsing for boolean values,
  default values, and type conversion. Consider making paths user-specific when creating
  temporary configurations.
repository: Homebrew/brew
label: Configurations
language: Ruby
comments_count: 4
repository_stars: 44168
---

Use structured environment variable handling with explicit validation instead of directly accessing ENV hash. Implement proper parsing for boolean values, default values, and type conversion. Consider making paths user-specific when creating temporary configurations.

For boolean environment variables, handle falsy values properly:

```ruby
# Instead of this:
if ENV["HOMEBREW_SOME_FLAG"].present?
  # Do something
end

# Do this:
if Homebrew::EnvConfig.some_flag?
  # Do something
end

# When implementing environment variable handlers:
def env_method_name(env, hash)
  if hash[:boolean]
    define_method(method_name) do
      env_value = ENV.fetch(env, nil)
      
      falsy_values = %w[false no off nil 0]
      if falsy_values.include?(env_value&.downcase)
        false
      else
        ENV[env].present?
      end
    end
  end
end
```

For configuration paths that may be shared across users, add user-specific identifiers:

```ruby
# Instead of this:
zdotdir = Pathname.new(HOMEBREW_TEMP/"brew-zsh-prompt")

# Do this:
zdotdir = Pathname.new(HOMEBREW_TEMP/"brew-zsh-prompt-#{Process.euid}")
```

This approach provides consistent interpretation of configuration values, reduces bugs from unexpected environment variable content, and prevents permission issues with shared configuration paths.