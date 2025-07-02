---
title: Configure at proper scope
description: Place configuration options at their proper scope within the framework
  hierarchy. Avoid tight coupling between components and ensure user configurations
  aren't accidentally overridden.
repository: rails/rails
label: Configurations
language: Ruby
comments_count: 7
repository_stars: 57027
---

Place configuration options at their proper scope within the framework hierarchy. Avoid tight coupling between components and ensure user configurations aren't accidentally overridden.

When working with configurations:

1. **Avoid direct framework references in components**
   
   Instead of accessing global constants directly:
   ```ruby
   def perform(event)
     ex = event.payload[:exception_object]
     if ex
       cleaned_backtrace = Rails.backtrace_cleaner.clean(ex.backtrace)
       # ...
     end
   end
   ```
   
   Pass dependencies through proper configuration channels:
   ```ruby
   # In the railtie
   initializer "active_job.backtrace_cleaner" do
     ActiveJob::LogSubscriber.backtrace_cleaner = Rails.backtrace_cleaner
   end
   
   # In the component
   def perform(event)
     ex = event.payload[:exception_object]
     if ex
       cleaned_backtrace = self.class.backtrace_cleaner.clean(ex.backtrace)
       # ...
     end
   end
   ```

2. **Respect user configuration**
   
   Check if user has already set a configuration before applying defaults:
   ```ruby
   # Bad: Overwrites user configuration
   initializer "active_record.attributes_for_inspect" do |app|
     ActiveRecord::Base.attributes_for_inspect = :all if app.config.consider_all_requests_local
   end
   
   # Good: Respects user configuration
   initializer "active_record.attributes_for_inspect" do |app|
     if app.config.consider_all_requests_local && app.config.active_record.attributes_for_inspect.nil?
       ActiveRecord::Base.attributes_for_inspect = :all
     end
   end
   ```

3. **Avoid mutating shared configuration objects**

   Always duplicate default configuration objects before modification:
   ```ruby
   # Bad: Mutates shared constant
   route_set_config = DEFAULT_CONFIG
   route_set_config[:some_setting] = value
   
   # Good: Works with a copy
   route_set_config = DEFAULT_CONFIG.dup
   route_set_config[:some_setting] = value
   ```

4. **Use environment-specific configuration via config, not conditionals**

   Instead of hardcoding environment checks:
   ```ruby
   # Bad: Direct environment checking in middleware
   if (Rails.env.development? || Rails.env.test?) && logger(request)
     # ...
   end
   ```
   
   Make behavior configurable:
   ```ruby
   # Good: Configurable behavior
   def initialize(app, warn_on_no_content_security_policy = false)
     @app = app
     @warn_on_no_content_security_policy = warn_on_no_content_security_policy
   end
   
   # Later in code
   if @warn_on_no_content_security_policy && logger(request)
     # ...
   end
   ```

Following these practices ensures components remain properly isolated and configurations behave predictably across different environments and application setups.


[
  {
    "discussion_id": "1904669769",
    "pr_number": 54129,
    "pr_file": "actionview/lib/action_view/cache_expiry.rb",
    "created_at": "2025-01-06T21:45:56+00:00",
    "commented_code": "if @watched_dirs != dirs_to_watch\n              @watched_dirs = dirs_to_watch\n              new_watcher = @watcher_class.new([], @watched_dirs) do\n              new_watcher = @watcher_class.new([], @watched_dirs, filter_path: Rails.root.to_s) do",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1904669769",
        "repo_full_name": "rails/rails",
        "pr_number": 54129,
        "pr_file": "actionview/lib/action_view/cache_expiry.rb",
        "discussion_id": "1904669769",
        "commented_code": "@@ -40,7 +40,7 @@ def build_watcher\n \n             if @watched_dirs != dirs_to_watch\n               @watched_dirs = dirs_to_watch\n-              new_watcher = @watcher_class.new([], @watched_dirs) do\n+              new_watcher = @watcher_class.new([], @watched_dirs, filter_path: Rails.root.to_s) do",
        "comment_created_at": "2025-01-06T21:45:56+00:00",
        "comment_author": "rafaelfranca",
        "comment_body": "This is coupling Action View with Railties in the wrong place.\r\n\r\nWe should pass a configuration to ActionView in its Railtie and use it here.",
        "pr_file_module": null
      },
      {
        "comment_id": "1905515638",
        "repo_full_name": "rails/rails",
        "pr_number": 54129,
        "pr_file": "actionview/lib/action_view/cache_expiry.rb",
        "discussion_id": "1904669769",
        "commented_code": "@@ -40,7 +40,7 @@ def build_watcher\n \n             if @watched_dirs != dirs_to_watch\n               @watched_dirs = dirs_to_watch\n-              new_watcher = @watcher_class.new([], @watched_dirs) do\n+              new_watcher = @watcher_class.new([], @watched_dirs, filter_path: Rails.root.to_s) do",
        "comment_created_at": "2025-01-07T14:12:50+00:00",
        "comment_author": "ermolaev",
        "comment_body": "agree, rewrote the code, also added `filter_path` to `EventedFileUpdateChecker`, and added tests",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1374948225",
    "pr_number": 49765,
    "pr_file": "activerecord/lib/active_record/railtie.rb",
    "created_at": "2023-10-27T18:59:39+00:00",
    "commented_code": "end\n      end\n    end\n\n    initializer \"active_record.attributes_for_inspect\" do |app|\n      ActiveSupport.on_load(:active_record) do\n        if app.config.consider_all_requests_local\n          ActiveRecord::Base.attributes_for_inspect = :all",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1374948225",
        "repo_full_name": "rails/rails",
        "pr_number": 49765,
        "pr_file": "activerecord/lib/active_record/railtie.rb",
        "discussion_id": "1374948225",
        "commented_code": "@@ -458,5 +458,13 @@ class Railtie < Rails::Railtie # :nodoc:\n         end\n       end\n     end\n+\n+    initializer \"active_record.attributes_for_inspect\" do |app|\n+      ActiveSupport.on_load(:active_record) do\n+        if app.config.consider_all_requests_local\n+          ActiveRecord::Base.attributes_for_inspect = :all",
        "comment_created_at": "2023-10-27T18:59:39+00:00",
        "comment_author": "rafaelfranca",
        "comment_body": "This will override any config the user set, no?",
        "pr_file_module": null
      },
      {
        "comment_id": "1387061473",
        "repo_full_name": "rails/rails",
        "pr_number": 49765,
        "pr_file": "activerecord/lib/active_record/railtie.rb",
        "discussion_id": "1374948225",
        "commented_code": "@@ -458,5 +458,13 @@ class Railtie < Rails::Railtie # :nodoc:\n         end\n       end\n     end\n+\n+    initializer \"active_record.attributes_for_inspect\" do |app|\n+      ActiveSupport.on_load(:active_record) do\n+        if app.config.consider_all_requests_local\n+          ActiveRecord::Base.attributes_for_inspect = :all",
        "comment_created_at": "2023-11-08T18:48:00+00:00",
        "comment_author": "andrewn617",
        "comment_body": "I don't think so, since it is run in the `:active_record` load hook, it will be set before `Base` is inherited by anything. I tested in my app and it worked as expected. But I will add a test like you suggested in your other comment.",
        "pr_file_module": null
      },
      {
        "comment_id": "1387073788",
        "repo_full_name": "rails/rails",
        "pr_number": 49765,
        "pr_file": "activerecord/lib/active_record/railtie.rb",
        "discussion_id": "1374948225",
        "commented_code": "@@ -458,5 +458,13 @@ class Railtie < Rails::Railtie # :nodoc:\n         end\n       end\n     end\n+\n+    initializer \"active_record.attributes_for_inspect\" do |app|\n+      ActiveSupport.on_load(:active_record) do\n+        if app.config.consider_all_requests_local\n+          ActiveRecord::Base.attributes_for_inspect = :all",
        "comment_created_at": "2023-11-08T18:59:43+00:00",
        "comment_author": "rafaelfranca",
        "comment_body": "What I mean is setting `config.active_record.attributes_for_inspect = [:uuid]`",
        "pr_file_module": null
      },
      {
        "comment_id": "1387092660",
        "repo_full_name": "rails/rails",
        "pr_number": 49765,
        "pr_file": "activerecord/lib/active_record/railtie.rb",
        "discussion_id": "1374948225",
        "commented_code": "@@ -458,5 +458,13 @@ class Railtie < Rails::Railtie # :nodoc:\n         end\n       end\n     end\n+\n+    initializer \"active_record.attributes_for_inspect\" do |app|\n+      ActiveSupport.on_load(:active_record) do\n+        if app.config.consider_all_requests_local\n+          ActiveRecord::Base.attributes_for_inspect = :all",
        "comment_created_at": "2023-11-08T19:16:04+00:00",
        "comment_author": "andrewn617",
        "comment_body": "Ah sorry, wasn't thinking of that angle. Fixed it and added a test. Thanks!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1761869122",
    "pr_number": 52297,
    "pr_file": "actionpack/lib/action_dispatch/routing/mapper.rb",
    "created_at": "2024-09-16T20:21:05+00:00",
    "commented_code": "end\n          else\n            def route_source_location\n              if Mapper.route_source_locations\n              if Mapper.route_source_locations || ActionDispatch.verbose_redirect_logs",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1761869122",
        "repo_full_name": "rails/rails",
        "pr_number": 52297,
        "pr_file": "actionpack/lib/action_dispatch/routing/mapper.rb",
        "discussion_id": "1761869122",
        "commented_code": "@@ -392,7 +392,7 @@ def route_source_location\n             end\n           else\n             def route_source_location\n-              if Mapper.route_source_locations\n+              if Mapper.route_source_locations || ActionDispatch.verbose_redirect_logs",
        "comment_created_at": "2024-09-16T20:21:05+00:00",
        "comment_author": "p8",
        "comment_body": "If we are going to return \"route source locations\", we might as well change how `Mapper.route_source_locations` is set and avoid `Mapper` having to know about `verbose_redirect_logs`.\r\n\r\n```suggestion\r\n             if Mapper.route_source_locations\r\n```\r\n\r\nWe could set it here instead:\r\nhttps://github.com/rails/rails/blob/d0f830033b2ea27bc1e66683ce5b16bd9ca55df1/actionpack/lib/action_dispatch/railtie.rb#L71\r\n\r\n```ruby\r\n      ActionDispatch::Routing::Mapper.route_source_locations = Rails.env.development? || ActionDispatch.verbose_redirect_logs\r\n```\r\n\r\nOr could we just leave it out?\r\nNot sure what the result would be.\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "1781095922",
        "repo_full_name": "rails/rails",
        "pr_number": 52297,
        "pr_file": "actionpack/lib/action_dispatch/routing/mapper.rb",
        "discussion_id": "1761869122",
        "commented_code": "@@ -392,7 +392,7 @@ def route_source_location\n             end\n           else\n             def route_source_location\n-              if Mapper.route_source_locations\n+              if Mapper.route_source_locations || ActionDispatch.verbose_redirect_logs",
        "comment_created_at": "2024-09-30T13:05:27+00:00",
        "comment_author": "dennispaagman",
        "comment_body": "Yeah that's a better place! \r\n\r\nI think leaving it out will make it that if you enable `verbose_redirect_logs` in a different environment than development the source locations won't be there for redirects from routes.\r\n\r\nI'm not sure if anyone wants to, or should, run this setting in different environments though, but it's possible.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "508997606",
    "pr_number": 39398,
    "pr_file": "actionpack/lib/action_dispatch/http/content_security_policy.rb",
    "created_at": "2020-10-21T05:25:18+00:00",
    "commented_code": "POLICY = \"Content-Security-Policy\"\n      POLICY_REPORT_ONLY = \"Content-Security-Policy-Report-Only\"\n\n      def initialize(app)\n      def initialize(app, warn_on_no_content_security_policy = false)\n        @app = app\n        @warn_on_no_content_security_policy = warn_on_no_content_security_policy\n      end\n\n      def call(env)\n        request = ActionDispatch::Request.new env\n        _, headers, _ = response = @app.call(env)\n\n        return response unless html_response?(headers)\n        return response if policy_present?(headers)\n\n        if policy = request.content_security_policy\n          nonce = request.content_security_policy_nonce\n          nonce_directives = request.content_security_policy_nonce_directives\n          context = request.controller_instance || request\n          headers[header_name(request)] = policy.build(context, nonce, nonce_directives)\n          headers[header_name(request)] = policy.build(context, nonce, nonce_directives, headers[CONTENT_TYPE])\n        else\n          if (Rails.env.development? || Rails.env.test?) && logger(request) && @warn_on_no_content_security_policy",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "508997606",
        "repo_full_name": "rails/rails",
        "pr_number": 39398,
        "pr_file": "actionpack/lib/action_dispatch/http/content_security_policy.rb",
        "discussion_id": "508997606",
        "commented_code": "@@ -9,34 +9,32 @@ class Middleware\n       POLICY = \"Content-Security-Policy\"\n       POLICY_REPORT_ONLY = \"Content-Security-Policy-Report-Only\"\n \n-      def initialize(app)\n+      def initialize(app, warn_on_no_content_security_policy = false)\n         @app = app\n+        @warn_on_no_content_security_policy = warn_on_no_content_security_policy\n       end\n \n       def call(env)\n         request = ActionDispatch::Request.new env\n         _, headers, _ = response = @app.call(env)\n \n-        return response unless html_response?(headers)\n         return response if policy_present?(headers)\n \n         if policy = request.content_security_policy\n           nonce = request.content_security_policy_nonce\n           nonce_directives = request.content_security_policy_nonce_directives\n           context = request.controller_instance || request\n-          headers[header_name(request)] = policy.build(context, nonce, nonce_directives)\n+          headers[header_name(request)] = policy.build(context, nonce, nonce_directives, headers[CONTENT_TYPE])\n+        else\n+          if (Rails.env.development? || Rails.env.test?) && logger(request) && @warn_on_no_content_security_policy",
        "comment_created_at": "2020-10-21T05:25:18+00:00",
        "comment_author": "rafaelfranca",
        "comment_body": "Checks for environment can't enter the action pack code. If we want different behavior per environment this should be a config on this class.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1030612902",
    "pr_number": 46555,
    "pr_file": "activejob/lib/active_job/log_subscriber.rb",
    "created_at": "2022-11-23T15:54:29+00:00",
    "commented_code": "job = event.payload[:job]\n      ex = event.payload[:exception_object]\n      if ex\n        cleaned_backtrace = Rails.backtrace_cleaner.clean(ex.backtrace)",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1030612902",
        "repo_full_name": "rails/rails",
        "pr_number": 46555,
        "pr_file": "activejob/lib/active_job/log_subscriber.rb",
        "discussion_id": "1030612902",
        "commented_code": "@@ -57,8 +57,9 @@ def perform(event)\n       job = event.payload[:job]\n       ex = event.payload[:exception_object]\n       if ex\n+        cleaned_backtrace = Rails.backtrace_cleaner.clean(ex.backtrace)",
        "comment_created_at": "2022-11-23T15:54:29+00:00",
        "comment_author": "rafaelfranca",
        "comment_body": "No Rails framework should have access to the `Rails` constant inside it since they can be used outside of a Rails application. We should be doing the same as `ActiveRecord::LogSubscriber`:\r\n\r\nhttps://github.com/rails/rails/blob/40563a3ab457f5b1d8a5defaecb7375c55bc3fd5/activerecord/lib/active_record/railtie.rb#L97-L99\r\nhttps://github.com/rails/rails/blob/40563a3ab457f5b1d8a5defaecb7375c55bc3fd5/activerecord/lib/active_record/log_subscriber.rb#L7",
        "pr_file_module": null
      },
      {
        "comment_id": "1030725259",
        "repo_full_name": "rails/rails",
        "pr_number": 46555,
        "pr_file": "activejob/lib/active_job/log_subscriber.rb",
        "discussion_id": "1030612902",
        "commented_code": "@@ -57,8 +57,9 @@ def perform(event)\n       job = event.payload[:job]\n       ex = event.payload[:exception_object]\n       if ex\n+        cleaned_backtrace = Rails.backtrace_cleaner.clean(ex.backtrace)",
        "comment_created_at": "2022-11-23T17:36:19+00:00",
        "comment_author": "warrenbhw",
        "comment_body": "Hey @rafaelfranca, thanks for taking a look.\r\nI'll address this and fix the tests soon\r\nCheers!",
        "pr_file_module": null
      },
      {
        "comment_id": "1034174603",
        "repo_full_name": "rails/rails",
        "pr_number": 46555,
        "pr_file": "activejob/lib/active_job/log_subscriber.rb",
        "discussion_id": "1030612902",
        "commented_code": "@@ -57,8 +57,9 @@ def perform(event)\n       job = event.payload[:job]\n       ex = event.payload[:exception_object]\n       if ex\n+        cleaned_backtrace = Rails.backtrace_cleaner.clean(ex.backtrace)",
        "comment_created_at": "2022-11-29T00:10:17+00:00",
        "comment_author": "warrenbhw",
        "comment_body": "@rafaelfranca the changes that you suggested are made. CI seems to be failing on a flaky test. Is there a way for me to queue another build another than pushing some whitespace changes?",
        "pr_file_module": null
      },
      {
        "comment_id": "1034245869",
        "repo_full_name": "rails/rails",
        "pr_number": 46555,
        "pr_file": "activejob/lib/active_job/log_subscriber.rb",
        "discussion_id": "1030612902",
        "commented_code": "@@ -57,8 +57,9 @@ def perform(event)\n       job = event.payload[:job]\n       ex = event.payload[:exception_object]\n       if ex\n+        cleaned_backtrace = Rails.backtrace_cleaner.clean(ex.backtrace)",
        "comment_created_at": "2022-11-29T02:41:52+00:00",
        "comment_author": "warrenbhw",
        "comment_body": "@rafaelfranca CI tests are passing. Lmk if there's anything else that I need to address here to get this merged!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1706409109",
    "pr_number": 52353,
    "pr_file": "actionpack/lib/action_dispatch/routing/route_set.rb",
    "created_at": "2024-08-07T05:39:52+00:00",
    "commented_code": "end\n\n      def self.new_with_config(config)\n        route_set_config = DEFAULT_CONFIG\n        route_set_config = DEFAULT_CONFIG.dup",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1706409109",
        "repo_full_name": "rails/rails",
        "pr_number": 52353,
        "pr_file": "actionpack/lib/action_dispatch/routing/route_set.rb",
        "discussion_id": "1706409109",
        "commented_code": "@@ -363,7 +363,7 @@ def self.default_resources_path_names\n       end\n \n       def self.new_with_config(config)\n-        route_set_config = DEFAULT_CONFIG\n+        route_set_config = DEFAULT_CONFIG.dup",
        "comment_created_at": "2024-08-07T05:39:52+00:00",
        "comment_author": "gmcgibbon",
        "comment_body": "This has to be a bug. We mutate a constant in the next few lines which changes the config of future route sets. Duping the constant prevents this.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1478393815",
    "pr_number": 50969,
    "pr_file": "activerecord/lib/active_record/query_logs.rb",
    "created_at": "2024-02-05T15:02:15+00:00",
    "commented_code": "#\n  #    config.active_record.cache_query_log_tags = true\n  module QueryLogs\n    mattr_accessor :taggings, instance_accessor: false, default: {}\n    mattr_accessor :taggings, instance_accessor: false, default: {\n      line: -> { query_source_location }",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1478393815",
        "repo_full_name": "rails/rails",
        "pr_number": 50969,
        "pr_file": "activerecord/lib/active_record/query_logs.rb",
        "discussion_id": "1478393815",
        "commented_code": "@@ -71,7 +72,10 @@ module ActiveRecord\n   #\n   #    config.active_record.cache_query_log_tags = true\n   module QueryLogs\n-    mattr_accessor :taggings, instance_accessor: false, default: {}\n+    mattr_accessor :taggings, instance_accessor: false, default: {\n+      line: -> { query_source_location }",
        "comment_created_at": "2024-02-05T15:02:15+00:00",
        "comment_author": "byroot",
        "comment_body": "This should be set in `activerecord/railtie.rb` like the others, otherwise it risks being overidden by users.",
        "pr_file_module": null
      }
    ]
  }
]
