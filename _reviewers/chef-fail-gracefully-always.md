---
title: Fail gracefully always
description: 'Ensure code handles errors robustly by using protective patterns that
  prevent resource leaks, provide clear diagnostics, and degrade gracefully when possible:'
repository: chef/chef
label: Error Handling
language: Ruby
comments_count: 9
repository_stars: 7860
---

Ensure code handles errors robustly by using protective patterns that prevent resource leaks, provide clear diagnostics, and degrade gracefully when possible:

1. **Use resource cleanup patterns** - Prefer block forms for resource management to ensure cleanup happens even during exceptions:

```ruby
# Good: Resources automatically closed after block
TargetIO::File.open(tempname, "w") do |tempfile|
  tempfile.write(crontab)
end

# Bad: Manual cleanup may be missed on exception paths
tempfile = TargetIO::File.open(tempname, "w") 
tempfile.write(crontab)
tempfile.close # Might never execute if an exception occurs
```

2. **Validate related parameters together** - Check parameter dependencies upfront:

```ruby
# Good: Clear validation of dependent parameters
def define_resource_requirements
  requirements.assert(:install, :upgrade) do |a|
    a.assertion { new_resource.proxy_user.nil? == new_resource.proxy_password.nil? }
    a.failure_message("Both proxy_user and proxy_password must be specified together")
  end
end
```

3. **Handle expected failures gracefully** - Catch specific exceptions to provide fallbacks:

```ruby
# Good: Handle missing command gracefully
def loop_mount_points
  @loop_mount_points ||= shell_out!("losetup -a").stdout
rescue Errno::ENOENT
  "" # Return empty string if command doesn't exist
end
```

4. **Use appropriate exception types** - Choose domain-specific exceptions to accurately represent errors:

```ruby
# Good: Domain-specific exception
raise Chef::Exceptions::Service, "systemctl show not reporting status for #{service_name}!"

# Bad: Using generic or misleading exception type
raise Mixlib::ShellOut::ShellCommandFailed, "Error message" # Implies shell command failed
```

5. **Provide clear, actionable error messages** - Check specific conditions and give targeted feedback:

```ruby
# Good: Check existence before permissions
if !File.directory?(File.dirname(file))
  ui.fatal "Directory #{File.dirname(file)} does not exist"
  exit 1
elsif !File.writable?(File.dirname(file))
  ui.fatal "Directory #{File.dirname(file)} is not writable. Check permissions."
  exit 1
end
```

Following these patterns will create more resilient code that fails predictably, provides clear diagnostics, and properly manages resources even during failures.
