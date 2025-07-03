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
