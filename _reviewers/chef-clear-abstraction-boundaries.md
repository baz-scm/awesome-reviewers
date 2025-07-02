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


[
  {
    "discussion_id": "934839822",
    "pr_number": 13105,
    "pr_file": "knife/lib/chef/knife/cookbook_upload.rb",
    "created_at": "2022-08-01T19:18:38+00:00",
    "commented_code": "end\n          end\n        end\n        { \"status\" => 200, \"message\" => \"Success\" } if @calling_request != \"CLI\"",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "934839822",
        "repo_full_name": "chef/chef",
        "pr_number": 13105,
        "pr_file": "knife/lib/chef/knife/cookbook_upload.rb",
        "discussion_id": "934839822",
        "commented_code": "@@ -163,6 +163,13 @@ def run\n             end\n           end\n         end\n+        { \"status\" => 200, \"message\" => \"Success\" } if @calling_request != \"CLI\"",
        "comment_created_at": "2022-08-01T19:18:38+00:00",
        "comment_author": "marcparadise",
        "comment_body": "\r\nThis isn't core to the knife cookbook upload command, so it seems very odd to have a CLI tool returning json  as if it were a single HTTP request handler.\r\n\r\nWould it make more sense to have a command that wraps cookbook upload, and adds the necessary return information and error handling behavior? \r\n\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "935854812",
        "repo_full_name": "chef/chef",
        "pr_number": 13105,
        "pr_file": "knife/lib/chef/knife/cookbook_upload.rb",
        "discussion_id": "934839822",
        "commented_code": "@@ -163,6 +163,13 @@ def run\n             end\n           end\n         end\n+        { \"status\" => 200, \"message\" => \"Success\" } if @calling_request != \"CLI\"",
        "comment_created_at": "2022-08-02T17:32:10+00:00",
        "comment_author": "sanjain-progress",
        "comment_body": "Yeah agree, CLI tool returning JSON looks odd to me also. Thanks for pointing it out.\r\n\r\nI will make further changes accordingly.\r\n\r\n\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "719579329",
    "pr_number": 11984,
    "pr_file": "lib/chef/mixin/powershell_exec.rb",
    "created_at": "2021-09-30T16:36:22+00:00",
    "commented_code": "#\n      # @param script [String] script to run\n      # @param interpreter [Symbol] the interpreter type, `:powershell` or `:pwsh`\n      # @param timeout [Integer, nil] timeout in seconds.\n      # @return [Chef::PowerShell] output\n      def powershell_exec(script, interpreter = :powershell)\n        case interpreter\n      def powershell_exec(script, options = {})\n        timeout = options.fetch(:timeout, nil)\n        case options.fetch(:interpreter, :powershell)\n        when :powershell\n          Chef::PowerShell.new(script)\n          Chef::PowerShell.new(script, timeout: timeout)\n        when :pwsh\n          Chef::Pwsh.new(script)\n          Chef::Pwsh.new(script, timeout: timeout)\n        else\n          raise ArgumentError, \"Expected interpreter of :powershell or :pwsh\"\n        end\n      end\n\n      # The same as the #powershell_exec method except this will raise\n      # Chef::PowerShell::CommandFailed if the command fails\n      def powershell_exec!(script, interpreter = :powershell)",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "719579329",
        "repo_full_name": "chef/chef",
        "pr_number": 11984,
        "pr_file": "lib/chef/mixin/powershell_exec.rb",
        "discussion_id": "719579329",
        "commented_code": "@@ -104,22 +104,24 @@ module PowershellExec\n       #\n       # @param script [String] script to run\n       # @param interpreter [Symbol] the interpreter type, `:powershell` or `:pwsh`\n+      # @param timeout [Integer, nil] timeout in seconds.\n       # @return [Chef::PowerShell] output\n-      def powershell_exec(script, interpreter = :powershell)\n-        case interpreter\n+      def powershell_exec(script, options = {})\n+        timeout = options.fetch(:timeout, nil)\n+        case options.fetch(:interpreter, :powershell)\n         when :powershell\n-          Chef::PowerShell.new(script)\n+          Chef::PowerShell.new(script, timeout: timeout)\n         when :pwsh\n-          Chef::Pwsh.new(script)\n+          Chef::Pwsh.new(script, timeout: timeout)\n         else\n           raise ArgumentError, \"Expected interpreter of :powershell or :pwsh\"\n         end\n       end\n \n       # The same as the #powershell_exec method except this will raise\n       # Chef::PowerShell::CommandFailed if the command fails\n-      def powershell_exec!(script, interpreter = :powershell)",
        "comment_created_at": "2021-09-30T16:36:22+00:00",
        "comment_author": "tas50",
        "comment_body": "don't we still want the ps interpreter?",
        "pr_file_module": null
      },
      {
        "comment_id": "719592189",
        "repo_full_name": "chef/chef",
        "pr_number": 11984,
        "pr_file": "lib/chef/mixin/powershell_exec.rb",
        "discussion_id": "719579329",
        "commented_code": "@@ -104,22 +104,24 @@ module PowershellExec\n       #\n       # @param script [String] script to run\n       # @param interpreter [Symbol] the interpreter type, `:powershell` or `:pwsh`\n+      # @param timeout [Integer, nil] timeout in seconds.\n       # @return [Chef::PowerShell] output\n-      def powershell_exec(script, interpreter = :powershell)\n-        case interpreter\n+      def powershell_exec(script, options = {})\n+        timeout = options.fetch(:timeout, nil)\n+        case options.fetch(:interpreter, :powershell)\n         when :powershell\n-          Chef::PowerShell.new(script)\n+          Chef::PowerShell.new(script, timeout: timeout)\n         when :pwsh\n-          Chef::Pwsh.new(script)\n+          Chef::Pwsh.new(script, timeout: timeout)\n         else\n           raise ArgumentError, \"Expected interpreter of :powershell or :pwsh\"\n         end\n       end\n \n       # The same as the #powershell_exec method except this will raise\n       # Chef::PowerShell::CommandFailed if the command fails\n-      def powershell_exec!(script, interpreter = :powershell)",
        "comment_created_at": "2021-09-30T16:53:33+00:00",
        "comment_author": "rishichawda",
        "comment_body": "yep it is available. the options here get pass directly to `powershell_exec` call instead of individually writing down all parameters and then again passing them to the method call. https://github.com/chef/chef/blob/b2d46ab518ae79c892ff14c6e78a09acae03883a/lib/chef/mixin/powershell_exec.rb#L123-L124\r\nthis looked cleaner than doing\r\n```ruby\r\ndef powershell_exec!(script, interpreter: :powershell, timeout: -1)\r\n         cmd = powershell_exec(script,  interpreter: interpreter, timeout: timeout)\r\n```\r\nwe only read the values in `powershell_exec` so passing It as a hash argument made it a bit cleaner https://github.com/chef/chef/blob/b2d46ab518ae79c892ff14c6e78a09acae03883a/lib/chef/mixin/powershell_exec.rb#L109-L112",
        "pr_file_module": null
      },
      {
        "comment_id": "741380411",
        "repo_full_name": "chef/chef",
        "pr_number": 11984,
        "pr_file": "lib/chef/mixin/powershell_exec.rb",
        "discussion_id": "719579329",
        "commented_code": "@@ -104,22 +104,24 @@ module PowershellExec\n       #\n       # @param script [String] script to run\n       # @param interpreter [Symbol] the interpreter type, `:powershell` or `:pwsh`\n+      # @param timeout [Integer, nil] timeout in seconds.\n       # @return [Chef::PowerShell] output\n-      def powershell_exec(script, interpreter = :powershell)\n-        case interpreter\n+      def powershell_exec(script, options = {})\n+        timeout = options.fetch(:timeout, nil)\n+        case options.fetch(:interpreter, :powershell)\n         when :powershell\n-          Chef::PowerShell.new(script)\n+          Chef::PowerShell.new(script, timeout: timeout)\n         when :pwsh\n-          Chef::Pwsh.new(script)\n+          Chef::Pwsh.new(script, timeout: timeout)\n         else\n           raise ArgumentError, \"Expected interpreter of :powershell or :pwsh\"\n         end\n       end\n \n       # The same as the #powershell_exec method except this will raise\n       # Chef::PowerShell::CommandFailed if the command fails\n-      def powershell_exec!(script, interpreter = :powershell)",
        "comment_created_at": "2021-11-02T18:55:34+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "I think the switch from `interpreter = :powershell` to `interpreter: :powershell` is likely a breaking change.\r\n\r\nI'm going to see if I can revert that change and ship it quickly since this is now blocking john's work.",
        "pr_file_module": null
      },
      {
        "comment_id": "741384407",
        "repo_full_name": "chef/chef",
        "pr_number": 11984,
        "pr_file": "lib/chef/mixin/powershell_exec.rb",
        "discussion_id": "719579329",
        "commented_code": "@@ -104,22 +104,24 @@ module PowershellExec\n       #\n       # @param script [String] script to run\n       # @param interpreter [Symbol] the interpreter type, `:powershell` or `:pwsh`\n+      # @param timeout [Integer, nil] timeout in seconds.\n       # @return [Chef::PowerShell] output\n-      def powershell_exec(script, interpreter = :powershell)\n-        case interpreter\n+      def powershell_exec(script, options = {})\n+        timeout = options.fetch(:timeout, nil)\n+        case options.fetch(:interpreter, :powershell)\n         when :powershell\n-          Chef::PowerShell.new(script)\n+          Chef::PowerShell.new(script, timeout: timeout)\n         when :pwsh\n-          Chef::Pwsh.new(script)\n+          Chef::Pwsh.new(script, timeout: timeout)\n         else\n           raise ArgumentError, \"Expected interpreter of :powershell or :pwsh\"\n         end\n       end\n \n       # The same as the #powershell_exec method except this will raise\n       # Chef::PowerShell::CommandFailed if the command fails\n-      def powershell_exec!(script, interpreter = :powershell)",
        "comment_created_at": "2021-11-02T19:01:11+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "Also the `options = {}` shouldn't be used any more in favor of proper kwargs since it behaves differently on ruby-3.0 I think.  It is also a lot easier to see the API on the method signature rather than having to look through the code (and messy method signatures are good feedback on the API being messy -- although a lot of times there's just nothing we can do about that).",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "687990671",
    "pr_number": 11905,
    "pr_file": "lib/chef/resource.rb",
    "created_at": "2021-08-12T18:34:07+00:00",
    "commented_code": "def suppress_up_to_date_messages?\n      false\n    end\n\n    private\n\n    def http_request_errors\n      source.map do |msg|\n        uri = URI.parse(msg)\n        \"Error connecting to #{msg} - Failed to open TCP connection to #{uri.host}:#{uri.port}\"\n      end\n    end",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "687990671",
        "repo_full_name": "chef/chef",
        "pr_number": 11905,
        "pr_file": "lib/chef/resource.rb",
        "discussion_id": "687990671",
        "commented_code": "@@ -1627,6 +1635,15 @@ def lookup_provider_constant(name, action = :nothing)\n     def suppress_up_to_date_messages?\n       false\n     end\n+\n+    private\n+\n+    def http_request_errors\n+      source.map do |msg|\n+        uri = URI.parse(msg)\n+        \"Error connecting to #{msg} - Failed to open TCP connection to #{uri.host}:#{uri.port}\"\n+      end\n+    end",
        "comment_created_at": "2021-08-12T18:34:07+00:00",
        "comment_author": "lamont-granquist",
        "comment_body": "all the code here in the resource class should go away.  i know the user request was to magically have the retries + retry_delay resource properties wired up to the Chef::HTTP object but that's the wrong abstraction and the wrong API.  those properties have a different meaning and the control of the HTTP settings needs to be done via a different API.",
        "pr_file_module": null
      },
      {
        "comment_id": "688369331",
        "repo_full_name": "chef/chef",
        "pr_number": 11905,
        "pr_file": "lib/chef/resource.rb",
        "discussion_id": "687990671",
        "commented_code": "@@ -1627,6 +1635,15 @@ def lookup_provider_constant(name, action = :nothing)\n     def suppress_up_to_date_messages?\n       false\n     end\n+\n+    private\n+\n+    def http_request_errors\n+      source.map do |msg|\n+        uri = URI.parse(msg)\n+        \"Error connecting to #{msg} - Failed to open TCP connection to #{uri.host}:#{uri.port}\"\n+      end\n+    end",
        "comment_created_at": "2021-08-13T09:16:41+00:00",
        "comment_author": "antima-gupta",
        "comment_body": "Moved this code to remote_file resource.",
        "pr_file_module": null
      }
    ]
  }
]
