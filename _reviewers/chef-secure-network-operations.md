---
title: Secure network operations
description: 'When performing network operations, prioritize security and configurability
  to ensure robustness across different environments. This includes:


  1. **Use explicit command patterns**: When executing shell commands that involve
  network operations, avoid string interpolation and use argument arrays instead to
  prevent command injection vulnerabilities.'
repository: chef/chef
label: Networking
language: Ruby
comments_count: 4
repository_stars: 7860
---

When performing network operations, prioritize security and configurability to ensure robustness across different environments. This includes:

1. **Use explicit command patterns**: When executing shell commands that involve network operations, avoid string interpolation and use argument arrays instead to prevent command injection vulnerabilities.

```ruby
# Avoid - potential command injection risk
shell_out!("semodule --install '#{selinux_module_filepath('pp')}'")

# Prefer - safer argument passing without shell interpretation
shell_out!("semodule", "--install", selinux_module_filepath('pp'))
```

2. **Make network operations transparent**: When downloading and executing content from the network, clearly document what's happening to avoid confusion and potential security issues.

```ruby
# Unclear - abbreviation hides the operation being performed
powershell_exec("iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))").error!

# Clear - explicitly states what's happening with a clarifying comment
# note that Invoke-Expression is being called on the downloaded script (outer parens)
powershell_exec("Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))").error!
```

3. **Use configurable HTTP options**: When making HTTP requests, provide configurable options through a hash instead of individual properties to allow for flexible and extensible client configuration.

```ruby
# Add to your resource
property :http_options, Hash,
  description: "Configuration options for the HTTP client"

# Then in your provider
def http_client_opts
  defaults = { retries: 5, retry_delay: 2 }
  defaults.merge(new_resource.http_options || {})
end
```

These practices ensure network operations are secure against injection attacks, clearly documented for maintainers, and configurable for different network environments.
