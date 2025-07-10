---
title: Clear error recovery paths
description: 'Implement error handling that provides both clear recovery paths for
  users and graceful degradation for the system. This includes:


  1. Clear, actionable error messages that guide users to resolution'
repository: Homebrew/brew
label: Error Handling
language: Ruby
comments_count: 6
repository_stars: 44168
---

Implement error handling that provides both clear recovery paths for users and graceful degradation for the system. This includes:

1. Clear, actionable error messages that guide users to resolution
2. Graceful fallbacks when operations fail
3. Retry mechanisms for transient failures
4. Early returns to simplify error flows

Example:
```ruby
def handle_api_request
  return unless result.status.success?

  begin
    json = JSON.parse(result.stdout)
  rescue JSON::ParserError
    nil
  end
rescue AuthenticationError => e
  message = case credentials_type
  when :github_cli_token
    "Your GitHub CLI login session may be invalid.\n" \
    "Refresh it with: gh auth login"
  else
    "Token may be invalid or expired.\n" \
    "Check: https://github.com/settings/tokens"
  end
  raise UserError.new(message)
rescue TemporaryFailure => e
  @retry_count ||= 0
  raise if @retry_count >= MAX_RETRIES

  sleep_time = 2 ** @retry_count
  @retry_count += 1
  retry
end
```

This approach ensures systems degrade gracefully while providing users clear paths to resolve issues.