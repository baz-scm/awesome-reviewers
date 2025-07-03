---
title: Document with examples
description: 'Always include comprehensive documentation with clear examples for properties,
  methods, and code patterns. Documentation should include:


  1. **Property descriptions**: Use the `description:` attribute to explain what each
  property does'
repository: chef/chef
label: Documentation
language: Ruby
comments_count: 7
repository_stars: 7860
---

Always include comprehensive documentation with clear examples for properties, methods, and code patterns. Documentation should include:

1. **Property descriptions**: Use the `description:` attribute to explain what each property does
   ```ruby
   property :source_location, introduced: "17.6", String,
     description: "The location where the package source resides."
   ```

2. **Version information**: Add `@since` tags and `introduced:` attributes to track when features were introduced
   ```ruby
   # @since 17.9
   property :only_record_changes, [TrueClass, FalseClass], default: false,
     description: "Only record changes to the registry key."
   ```

3. **Usage examples**: Provide concrete examples, especially for complex features
   ```ruby
   # For command options:
   option :connection_protocol,
     short: "-o PROTOCOL",
     long: "--connection-protocol PROTOCOL",
     description: "The protocol to use to connect to the target node (such as 'ssh' or 'winrm')."
   ```

4. **Pattern matching examples**: When documenting pattern matching or regular expressions, include example lines that would match the pattern
   ```ruby
   # This matches mount points like "/mnt/volume"
   when /\A#{Regexp.escape(real_mount_point)}\s+#{device_mount_regex}\s/
   ```

5. **Accessible language**: Use plain language descriptions over technical jargon when possible, and spell out "regular expression" instead of "regex" in user-facing documentation

Comprehensive documentation reduces the learning curve for new developers and makes the codebase more maintainable.
