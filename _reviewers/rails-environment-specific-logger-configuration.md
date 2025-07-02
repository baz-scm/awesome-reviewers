---
title: Environment-specific logger configuration
description: Configure loggers in environment-specific files rather than in application.rb
  or initializers. Different environments (development, test, production) typically
  require different logging levels and configurations, and Rails is designed to support
  this pattern.
repository: rails/rails
label: Logging
language: Markdown
comments_count: 3
repository_stars: 57027
---

Configure loggers in environment-specific files rather than in application.rb or initializers. Different environments (development, test, production) typically require different logging levels and configurations, and Rails is designed to support this pattern.

When setting up loggers or modifying logging levels, place the configuration in the appropriate environment file:

```ruby
# AVOID
# config/application.rb
config.logger = Logger.new(STDOUT)
config.log_level = :warn

# PREFER
# config/environments/production.rb
config.logger = Logger.new(STDOUT)
config.log_level = :warn
```

This approach ensures that each environment can have tailored logging settings appropriate for its context (e.g., verbose in development, minimal in production). It also follows Rails conventions, making your codebase more maintainable and aligned with standard practices.


[
  {
    "discussion_id": "1909430804",
    "pr_number": 54066,
    "pr_file": "guides/source/debugging_rails_applications.md",
    "created_at": "2025-01-09T21:03:46+00:00",
    "commented_code": "### What is the Logger?\n\nRails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may also be substituted.\n\nYou can specify an alternative logger in `config/application.rb` or any other environment file, for example:\nRails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may be substituted:\n\n```ruby\n# config/application.rb",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1909430804",
        "repo_full_name": "rails/rails",
        "pr_number": 54066,
        "pr_file": "guides/source/debugging_rails_applications.md",
        "discussion_id": "1909430804",
        "commented_code": "@@ -107,16 +107,15 @@ It can also be useful to save information to log files at runtime. Rails maintai\n \n ### What is the Logger?\n \n-Rails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may also be substituted.\n-\n-You can specify an alternative logger in `config/application.rb` or any other environment file, for example:\n+Rails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may be substituted:\n \n ```ruby\n+# config/application.rb",
        "comment_created_at": "2025-01-09T21:03:46+00:00",
        "comment_author": "p8",
        "comment_body": "Most of the time, a different logger and level is used per environment.\r\nThe default production environment config specifically [mentions](https://github.com/rails/rails/blob/86312f5dc05b96d9c1c71ef03d257c155622f00e/railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt#L42) it.\r\nMaybe use that instead?\r\n```suggestion\r\n# config/environments/production.rb\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1920908928",
        "repo_full_name": "rails/rails",
        "pr_number": 54066,
        "pr_file": "guides/source/debugging_rails_applications.md",
        "discussion_id": "1909430804",
        "commented_code": "@@ -107,16 +107,15 @@ It can also be useful to save information to log files at runtime. Rails maintai\n \n ### What is the Logger?\n \n-Rails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may also be substituted.\n-\n-You can specify an alternative logger in `config/application.rb` or any other environment file, for example:\n+Rails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may be substituted:\n \n ```ruby\n+# config/application.rb",
        "comment_created_at": "2025-01-18T00:44:48+00:00",
        "comment_author": "benkoshy",
        "comment_body": "applied",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1909434261",
    "pr_number": 54066,
    "pr_file": "guides/source/debugging_rails_applications.md",
    "created_at": "2025-01-09T21:07:49+00:00",
    "commented_code": "### What is the Logger?\n\nRails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may also be substituted.\n\nYou can specify an alternative logger in `config/application.rb` or any other environment file, for example:\nRails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may be substituted:\n\n```ruby\n# config/application.rb\nconfig.logger = Logger.new(STDOUT)\nconfig.logger = Log4r::Logger.new(\"Application Log\")\n```\n\nOr in the `Initializer` section, add _any_ of the following\nOr in the `Initializer` section, add _any_ of the following:",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1909434261",
        "repo_full_name": "rails/rails",
        "pr_number": 54066,
        "pr_file": "guides/source/debugging_rails_applications.md",
        "discussion_id": "1909434261",
        "commented_code": "@@ -107,16 +107,15 @@ It can also be useful to save information to log files at runtime. Rails maintai\n \n ### What is the Logger?\n \n-Rails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may also be substituted.\n-\n-You can specify an alternative logger in `config/application.rb` or any other environment file, for example:\n+Rails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may be substituted:\n \n ```ruby\n+# config/application.rb\n config.logger = Logger.new(STDOUT)\n config.logger = Log4r::Logger.new(\"Application Log\")\n ```\n \n-Or in the `Initializer` section, add _any_ of the following\n+Or in the `Initializer` section, add _any_ of the following:",
        "comment_created_at": "2025-01-09T21:07:49+00:00",
        "comment_author": "p8",
        "comment_body": "I'd probably remove this line and the following example.\r\nI don't think we should be advising configuring logger this way as the environment config seems the most common location.",
        "pr_file_module": null
      },
      {
        "comment_id": "1920909201",
        "repo_full_name": "rails/rails",
        "pr_number": 54066,
        "pr_file": "guides/source/debugging_rails_applications.md",
        "discussion_id": "1909434261",
        "commented_code": "@@ -107,16 +107,15 @@ It can also be useful to save information to log files at runtime. Rails maintai\n \n ### What is the Logger?\n \n-Rails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may also be substituted.\n-\n-You can specify an alternative logger in `config/application.rb` or any other environment file, for example:\n+Rails makes use of the `ActiveSupport::Logger` class to write log information. Other loggers, such as `Log4r`, may be substituted:\n \n ```ruby\n+# config/application.rb\n config.logger = Logger.new(STDOUT)\n config.logger = Log4r::Logger.new(\"Application Log\")\n ```\n \n-Or in the `Initializer` section, add _any_ of the following\n+Or in the `Initializer` section, add _any_ of the following:",
        "comment_created_at": "2025-01-18T00:45:42+00:00",
        "comment_author": "benkoshy",
        "comment_body": "removed as suggested.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1909436249",
    "pr_number": 54066,
    "pr_file": "guides/source/debugging_rails_applications.md",
    "created_at": "2025-01-09T21:09:58+00:00",
    "commented_code": "The available log levels are: `:debug`, `:info`, `:warn`, `:error`, `:fatal`,\nand `:unknown`, corresponding to the log level numbers from 0 up to 5,\nrespectively. To change the default log level, use\nrespectively. To change the default log level:\n\n```ruby\nconfig.log_level = :warn # In any environment initializer, or\nRails.logger.level = 0 # at any time\n# config/application.rb",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1909436249",
        "repo_full_name": "rails/rails",
        "pr_number": 54066,
        "pr_file": "guides/source/debugging_rails_applications.md",
        "discussion_id": "1909436249",
        "commented_code": "@@ -134,11 +133,11 @@ method.\n \n The available log levels are: `:debug`, `:info`, `:warn`, `:error`, `:fatal`,\n and `:unknown`, corresponding to the log level numbers from 0 up to 5,\n-respectively. To change the default log level, use\n+respectively. To change the default log level:\n \n ```ruby\n-config.log_level = :warn # In any environment initializer, or\n-Rails.logger.level = 0 # at any time\n+# config/application.rb",
        "comment_created_at": "2025-01-09T21:09:58+00:00",
        "comment_author": "p8",
        "comment_body": "Similarly, I think this should mention the environment file as that [is where](https://github.com/rails/rails/blob/86312f5dc05b96d9c1c71ef03d257c155622f00e/railties/lib/rails/generators/rails/app/templates/config/environments/production.rb.tt#L45) this is located in a new Rails app.\r\n```suggestion\r\n# config/environments/production.rb\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1920916219",
        "repo_full_name": "rails/rails",
        "pr_number": 54066,
        "pr_file": "guides/source/debugging_rails_applications.md",
        "discussion_id": "1909436249",
        "commented_code": "@@ -134,11 +133,11 @@ method.\n \n The available log levels are: `:debug`, `:info`, `:warn`, `:error`, `:fatal`,\n and `:unknown`, corresponding to the log level numbers from 0 up to 5,\n-respectively. To change the default log level, use\n+respectively. To change the default log level:\n \n ```ruby\n-config.log_level = :warn # In any environment initializer, or\n-Rails.logger.level = 0 # at any time\n+# config/application.rb",
        "comment_created_at": "2025-01-18T01:07:52+00:00",
        "comment_author": "benkoshy",
        "comment_body": "applied.",
        "pr_file_module": null
      },
      {
        "comment_id": "1920916553",
        "repo_full_name": "rails/rails",
        "pr_number": 54066,
        "pr_file": "guides/source/debugging_rails_applications.md",
        "discussion_id": "1909436249",
        "commented_code": "@@ -134,11 +133,11 @@ method.\n \n The available log levels are: `:debug`, `:info`, `:warn`, `:error`, `:fatal`,\n and `:unknown`, corresponding to the log level numbers from 0 up to 5,\n-respectively. To change the default log level, use\n+respectively. To change the default log level:\n \n ```ruby\n-config.log_level = :warn # In any environment initializer, or\n-Rails.logger.level = 0 # at any time\n+# config/application.rb",
        "comment_created_at": "2025-01-18T01:09:05+00:00",
        "comment_author": "benkoshy",
        "comment_body": "applied.",
        "pr_file_module": null
      }
    ]
  }
]
