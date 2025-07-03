---
title: Clear abstraction boundaries
description: "Design APIs with clear and consistent abstraction boundaries to maintain\
  \ code quality and prevent interface leakage between different system layers. \n"
repository: chef/chef
label: API
language: Ruby
comments_count: 3
repository_stars: 7860
---

Design APIs with clear and consistent abstraction boundaries to maintain code quality and prevent interface leakage between different system layers. 

Key principles:

1. **Separate CLI and API interfaces**: CLI tools should not return API-style responses, and API endpoints should not handle CLI-specific concerns.
   ```ruby
   # Incorrect - CLI tool returning HTTP-like response
   { "status" => 200, "message" => "Success" } if @calling_request != "CLI"
   
   # Better approach - wrap the functionality with appropriate interfaces
   def perform_upload
     # Upload functionality here
     return true # Simple boolean for CLI
   end
   
   def api_upload
     perform_upload
     { "status" => 200, "message" => "Success" } # HTTP-style response for API
   end
   ```

2. **Use proper method signatures**: Prefer explicit keyword arguments over option hashes for better readability, documentation, and forward compatibility.
   ```ruby
   # Avoid this pattern - hard to document, using a generic options hash
   def powershell_exec(script, options = {})
     timeout = options.fetch(:timeout, nil)
     # ...
   end
   
   # Better pattern - explicit keyword arguments with defaults
   def powershell_exec(script, interpreter: :powershell, timeout: nil)
     # Implementation...
   end
   ```

3. **Place functionality at the appropriate abstraction level**: Methods and properties should exist at the level where they are most logically connected.
   ```ruby
   # Avoid adding HTTP-specific error handling in generic resources
   class Resource
     # This doesn't belong here - too specific
     private
     def http_request_errors
       source.map do |msg|
         uri = URI.parse(msg)
         "Error connecting to #{msg} - Failed to open TCP connection to #{uri.host}:#{uri.port}"
       end
     end
   end
   
   # Better: Place in the specific resource that needs it
   class RemoteFileResource < Resource
     private
     def http_request_errors
       # Implementation...
     end
   end
   ```

Following these principles creates more maintainable, testable, and adaptable code by ensuring that each component has a clear, focused responsibility.
