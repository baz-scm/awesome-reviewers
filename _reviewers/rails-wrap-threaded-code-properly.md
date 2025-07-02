---
title: Wrap threaded code properly
description: When working with threads in Rails applications, always wrap application
  code with `Rails.application.executor.wrap` to ensure thread safety and proper state
  management. Code running outside these wrappers can cause race conditions, memory
  leaks, and inconsistent application state.
repository: rails/rails
label: Concurrency
language: Markdown
comments_count: 3
repository_stars: 57027
---

When working with threads in Rails applications, always wrap application code with `Rails.application.executor.wrap` to ensure thread safety and proper state management. Code running outside these wrappers can cause race conditions, memory leaks, and inconsistent application state.

```ruby
# INCORRECT - application code outside wrapper
Thread.new do
  user = User.find(params[:id])  # Unsafe!
  Rails.application.executor.wrap do
    # Some wrapped code
  end
end

# CORRECT - all application code inside wrapper
Thread.new do
  # No application code here
  Rails.application.executor.wrap do
    user = User.find(params[:id])
    # All application code goes here
  end
end
```

This applies to all scenarios where you manually create threads, including when using thread pools from libraries like Concurrent Ruby. The Rails executor ensures that your thread has proper access to autoloading, manages database connections correctly, and handles thread-local data appropriately.

For long-running operations that may be interrupted (like during deployments), also consider implementing checkpoints to preserve progress:

```ruby
Rails.application.executor.wrap do
  records.find_each do |record|
    record.process
    # Create checkpoints regularly for interruptible work
    checkpoint! if should_checkpoint?
  end
end
```


[
  {
    "discussion_id": "2154594443",
    "pr_number": 55179,
    "pr_file": "guides/source/threading_and_code_execution.md",
    "created_at": "2025-06-18T13:20:42+00:00",
    "commented_code": "```\n\nTIP: If you repeatedly invoke application code from a long-running process, you\nmay want to wrap using the [Reloader](#reloader) instead.\nmay want to wrap using the [Reloader](#the-reloader) instead.\n\nEach thread should be wrapped before it runs application code, so if your\napplication manually delegates work to other threads, such as via `Thread.new`\nor Concurrent Ruby features that use thread pools, you should immediately wrap\nthe block:\nIf your application manually delegates work to other threads, such as via\n`Thread.new`, or uses features from the [Concurrent\nRuby](https://github.com/ruby-concurrency/concurrent-ruby) gem that use thread\npools, you should immediately wrap the block, before any application code is\nrun:\n\n```ruby\nThread.new do",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2154594443",
        "repo_full_name": "rails/rails",
        "pr_number": 55179,
        "pr_file": "guides/source/threading_and_code_execution.md",
        "discussion_id": "2154594443",
        "commented_code": "@@ -72,12 +150,13 @@ end\n ```\n \n TIP: If you repeatedly invoke application code from a long-running process, you\n-may want to wrap using the [Reloader](#reloader) instead.\n+may want to wrap using the [Reloader](#the-reloader) instead.\n \n-Each thread should be wrapped before it runs application code, so if your\n-application manually delegates work to other threads, such as via `Thread.new`\n-or Concurrent Ruby features that use thread pools, you should immediately wrap\n-the block:\n+If your application manually delegates work to other threads, such as via\n+`Thread.new`, or uses features from the [Concurrent\n+Ruby](https://github.com/ruby-concurrency/concurrent-ruby) gem that use thread\n+pools, you should immediately wrap the block, before any application code is\n+run:\n \n ```ruby\n Thread.new do",
        "comment_created_at": "2025-06-18T13:20:42+00:00",
        "comment_author": "p8",
        "comment_body": "Maybe we should make it more explicit that no code should be defined outside `Rails.application.executor.wrap`?\r\n```suggestion\r\nThread.new do\r\n  # no code here\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2167152581",
    "pr_number": 55179,
    "pr_file": "guides/source/threading_and_code_execution.md",
    "created_at": "2025-06-25T16:35:54+00:00",
    "commented_code": "end\n```\n\n### Concurrency\nNOTE: The Rails Executor is safely re-entrant; it can be called again if it is\nalready running. In this case, the `wrap` method has no effect.\n\n#### Running Mode\n\nWhen called, the Rails Executor will put the current thread into `running` mode\nin the [Load Interlock](#load-interlock).\n\nThe Executor will put the current thread into `running` mode in the [Load\nInterlock](#load-interlock). This operation will block temporarily if another\nthread is currently either autoloading a constant or unloading/reloading\nthe application.\nThis operation will block temporarily if another thread is currently either\nautoloading a constant or unloading/reloading the application.\n\nReloader\n--------\n#### Examples of Wrapped Application Code\n\nLike the Executor, the Reloader also wraps application code. If the Executor is\nnot already active on the current thread, the Reloader will invoke it for you,\nso you only need to call one. This also guarantees that everything the Reloader\ndoes, including all its callback invocations, occurs wrapped inside the\nExecutor.\nAny time your library or component needs to invoke code that will run in the\napplication, the code should be wrapped to ensure thread safety and a consistent\nand clean runtime state.\n\nFor example, you may be setting a `Current` user (using\n[`ActiveSupport::CurrentAttributes`](https://api.rubyonrails.org/classes/ActiveSupport/CurrentAttributes.html)).\n\n```ruby\ndef log_with_user_context(message)\n  Rails.application.executor.wrap do\n    Current.user = User.find_by(id: 1)\n  end\nend\n```\n\nYou may be triggering an Active Record callback or lifecycle hook in an\napplication:\n\n```ruby\ndef perform_task_with_record(record)\n  Rails.application.executor.wrap do\n    record.save! # Executes before_save, after_save, etc.\n  end\nend\n```\n\nOr enqueuing or performing a background job within the application:\n\n```ruby\ndef enqueue_background_job(job_class, *args)\n  Rails.application.executor.wrap do\n    job_class.perform_later(*args)\n  end\nend\n```\n\nThese are just a few of many possible use cases, including rendering views or\ntemplates, broadcasting via [`Action Cable`](action_cable_overview.html) or\nusing [`Rails.cache`](caching_with_rails.html).\n\n### The Reloader\n\nLike the Executor, the\n[Reloader](https://api.rubyonrails.org/classes/ActiveSupport/Reloader.html) also\nwraps application code. The Reloader is only suitable where a long-running\nframework-level process repeatedly calls into application code, such as for a\nweb server or job queue.\n\nNOTE: Rails automatically wraps web requests and Active Job workers, so you'll\nrarely need to invoke the Reloader for yourself. Always consider whether the\nExecutor is a better fit for your use case.\n\nIf the Executor is not already active on the current thread, the Reloader will\ninvoke it for you, so you only need to call one. This also guarantees that\neverything the Reloader does, including all its callback executions, occurs\nwrapped inside the Executor.\n\n```ruby\nRails.application.reloader.wrap do\n  # call application code here\nend\n```\n\nThe Reloader is only suitable where a long-running framework-level process\nrepeatedly calls into application code, such as for a web server or job queue.\nRails automatically wraps web requests and Active Job workers, so you'll rarely\nneed to invoke the Reloader for yourself. Always consider whether the Executor\nis a better fit for your use case.\n\n### Callbacks\n#### Callbacks\n\nBefore entering the wrapped block, the Reloader will check whether the running\napplication needs to be reloaded -- for example, because a model's source file has\nbeen modified. If it determines a reload is required, it will wait until it's\nsafe, and then do so, before continuing. When the application is configured to\nalways reload regardless of whether any changes are detected, the reload is\ninstead performed at the end of the block.\napplication needs to be reloaded (because a model's source file has been\nmodified, for example). If it determines a reload is required, it will wait\nuntil it's safe, and then do so, before continuing. When the application is\nconfigured to always reload regardless of whether any changes are detected, the\nreload is instead performed at the end of the block.\n\nThe Reloader also provides `to_run` and `to_complete` callbacks; they are\ninvoked at the same points as those of the Executor, but only when the current\nexecution has initiated an application reload. When no reload is deemed\nnecessary, the Reloader will invoke the wrapped block with no other callbacks.",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2167152581",
        "repo_full_name": "rails/rails",
        "pr_number": 55179,
        "pr_file": "guides/source/threading_and_code_execution.md",
        "discussion_id": "2167152581",
        "commented_code": "@@ -106,60 +183,113 @@ ensure\n end\n ```\n \n-### Concurrency\n+NOTE: The Rails Executor is safely re-entrant; it can be called again if it is\n+already running. In this case, the `wrap` method has no effect.\n+\n+#### Running Mode\n+\n+When called, the Rails Executor will put the current thread into `running` mode\n+in the [Load Interlock](#load-interlock).\n \n-The Executor will put the current thread into `running` mode in the [Load\n-Interlock](#load-interlock). This operation will block temporarily if another\n-thread is currently either autoloading a constant or unloading/reloading\n-the application.\n+This operation will block temporarily if another thread is currently either\n+autoloading a constant or unloading/reloading the application.\n \n-Reloader\n---------\n+#### Examples of Wrapped Application Code\n \n-Like the Executor, the Reloader also wraps application code. If the Executor is\n-not already active on the current thread, the Reloader will invoke it for you,\n-so you only need to call one. This also guarantees that everything the Reloader\n-does, including all its callback invocations, occurs wrapped inside the\n-Executor.\n+Any time your library or component needs to invoke code that will run in the\n+application, the code should be wrapped to ensure thread safety and a consistent\n+and clean runtime state.\n+\n+For example, you may be setting a `Current` user (using\n+[`ActiveSupport::CurrentAttributes`](https://api.rubyonrails.org/classes/ActiveSupport/CurrentAttributes.html)).\n+\n+```ruby\n+def log_with_user_context(message)\n+  Rails.application.executor.wrap do\n+    Current.user = User.find_by(id: 1)\n+  end\n+end\n+```\n+\n+You may be triggering an Active Record callback or lifecycle hook in an\n+application:\n+\n+```ruby\n+def perform_task_with_record(record)\n+  Rails.application.executor.wrap do\n+    record.save! # Executes before_save, after_save, etc.\n+  end\n+end\n+```\n+\n+Or enqueuing or performing a background job within the application:\n+\n+```ruby\n+def enqueue_background_job(job_class, *args)\n+  Rails.application.executor.wrap do\n+    job_class.perform_later(*args)\n+  end\n+end\n+```\n+\n+These are just a few of many possible use cases, including rendering views or\n+templates, broadcasting via [`Action Cable`](action_cable_overview.html) or\n+using [`Rails.cache`](caching_with_rails.html).\n+\n+### The Reloader\n+\n+Like the Executor, the\n+[Reloader](https://api.rubyonrails.org/classes/ActiveSupport/Reloader.html) also\n+wraps application code. The Reloader is only suitable where a long-running\n+framework-level process repeatedly calls into application code, such as for a\n+web server or job queue.\n+\n+NOTE: Rails automatically wraps web requests and Active Job workers, so you'll\n+rarely need to invoke the Reloader for yourself. Always consider whether the\n+Executor is a better fit for your use case.\n+\n+If the Executor is not already active on the current thread, the Reloader will\n+invoke it for you, so you only need to call one. This also guarantees that\n+everything the Reloader does, including all its callback executions, occurs\n+wrapped inside the Executor.\n \n ```ruby\n Rails.application.reloader.wrap do\n   # call application code here\n end\n ```\n \n-The Reloader is only suitable where a long-running framework-level process\n-repeatedly calls into application code, such as for a web server or job queue.\n-Rails automatically wraps web requests and Active Job workers, so you'll rarely\n-need to invoke the Reloader for yourself. Always consider whether the Executor\n-is a better fit for your use case.\n-\n-### Callbacks\n+#### Callbacks\n \n Before entering the wrapped block, the Reloader will check whether the running\n-application needs to be reloaded -- for example, because a model's source file has\n-been modified. If it determines a reload is required, it will wait until it's\n-safe, and then do so, before continuing. When the application is configured to\n-always reload regardless of whether any changes are detected, the reload is\n-instead performed at the end of the block.\n+application needs to be reloaded (because a model's source file has been\n+modified, for example). If it determines a reload is required, it will wait\n+until it's safe, and then do so, before continuing. When the application is\n+configured to always reload regardless of whether any changes are detected, the\n+reload is instead performed at the end of the block.\n \n The Reloader also provides `to_run` and `to_complete` callbacks; they are\n invoked at the same points as those of the Executor, but only when the current\n execution has initiated an application reload. When no reload is deemed\n necessary, the Reloader will invoke the wrapped block with no other callbacks.\n ",
        "comment_created_at": "2025-06-25T16:35:54+00:00",
        "comment_author": "p8",
        "comment_body": "It would be nice to show an code example here as well:\r\n````suggestion\r\n\r\n```ruby\r\nRails.application.reloader.to_run do\r\n  # call reloading code here\r\nend\r\n```\r\n\r\n````",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2150283629",
    "pr_number": 55193,
    "pr_file": "guides/source/active_job_basics.md",
    "created_at": "2025-06-16T15:21:51+00:00",
    "commented_code": "[`queue_with_priority`]:\n    https://api.rubyonrails.org/classes/ActiveJob/QueuePriority/ClassMethods.html#method-i-queue_with_priority\n\nJob Continuations\n-----------------\n\nJobs can be split into resumable steps using continuations. This is useful when\na job may be interrupted - for example, during queue shutdown. When using\ncontinuations, the job can resume from the last completed step, avoiding the\nneed to restart from the beginning.\n\nTo use continuations, include the `ActiveJob::Continuable` module. You can then\ndefine each step using the `step` method inside the `perform` method. Each step can\nbe declared with a block or by referencing a method name.\n\n```ruby\nclass ProcessImportJob < ApplicationJob\n  include ActiveJob::Continuable\n\n  def perform(import_id)\n    # Always runs on job start, even when resuming from an interrupted step.\n    @import = Import.find(import_id)\n\n    # Step defined using a block\n    step :initialize do\n      @import.initialize\n    end\n\n    # Step with a cursor \u2014 progress is saved and resumed if the job is interrupted\n    step :process do |step|\n      @import.records.find_each(start: step.cursor) do |record|\n        record.process\n        step.advance! from: record.id\n      end\n    end\n\n    # Step defined by referencing a method\n    step :finalize\n  end\n\n  private\n    def finalize\n      @import.finalize",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2150283629",
        "repo_full_name": "rails/rails",
        "pr_number": 55193,
        "pr_file": "guides/source/active_job_basics.md",
        "discussion_id": "2150283629",
        "commented_code": "@@ -671,6 +671,56 @@ number as more important.\n [`queue_with_priority`]:\n     https://api.rubyonrails.org/classes/ActiveJob/QueuePriority/ClassMethods.html#method-i-queue_with_priority\n \n+Job Continuations\n+-----------------\n+\n+Jobs can be split into resumable steps using continuations. This is useful when\n+a job may be interrupted - for example, during queue shutdown. When using\n+continuations, the job can resume from the last completed step, avoiding the\n+need to restart from the beginning.\n+\n+To use continuations, include the `ActiveJob::Continuable` module. You can then\n+define each step using the `step` method inside the `perform` method. Each step can\n+be declared with a block or by referencing a method name.\n+\n+```ruby\n+class ProcessImportJob < ApplicationJob\n+  include ActiveJob::Continuable\n+\n+  def perform(import_id)\n+    # Always runs on job start, even when resuming from an interrupted step.\n+    @import = Import.find(import_id)\n+\n+    # Step defined using a block\n+    step :initialize do\n+      @import.initialize\n+    end\n+\n+    # Step with a cursor \u2014 progress is saved and resumed if the job is interrupted\n+    step :process do |step|\n+      @import.records.find_each(start: step.cursor) do |record|\n+        record.process\n+        step.advance! from: record.id\n+      end\n+    end\n+\n+    # Step defined by referencing a method\n+    step :finalize\n+  end\n+\n+  private\n+    def finalize\n+      @import.finalize",
        "comment_created_at": "2025-06-16T15:21:51+00:00",
        "comment_author": "MiroslavCsonka",
        "comment_body": "I'm not sure I understand this completely, or if our setup (SolidQueue) is incorrect, but what would happen if the finalize method takes 10 minutes and a deployment interrupts it? Like a long SQL query or a huge file download. Would the scheduler just kill the job, not record any continuations, and it would just start from scratch?\r\n\r\nIt's my understanding that it's `step`, `.checkpoint!`, `.advance!`, and `.set!` that are responsible for checking whether or not we are in the process of shutting down, and if we are, they attach metadata to the job and reschedule it.\r\n\r\nThis means that if your SolidQueue shutdown_timeout config is 5 seconds (the default), the above methods have to be called at least every 5 seconds; otherwise, the whole progress is potentially lost, right?",
        "pr_file_module": null
      },
      {
        "comment_id": "2152568358",
        "repo_full_name": "rails/rails",
        "pr_number": 55193,
        "pr_file": "guides/source/active_job_basics.md",
        "discussion_id": "2150283629",
        "commented_code": "@@ -671,6 +671,56 @@ number as more important.\n [`queue_with_priority`]:\n     https://api.rubyonrails.org/classes/ActiveJob/QueuePriority/ClassMethods.html#method-i-queue_with_priority\n \n+Job Continuations\n+-----------------\n+\n+Jobs can be split into resumable steps using continuations. This is useful when\n+a job may be interrupted - for example, during queue shutdown. When using\n+continuations, the job can resume from the last completed step, avoiding the\n+need to restart from the beginning.\n+\n+To use continuations, include the `ActiveJob::Continuable` module. You can then\n+define each step using the `step` method inside the `perform` method. Each step can\n+be declared with a block or by referencing a method name.\n+\n+```ruby\n+class ProcessImportJob < ApplicationJob\n+  include ActiveJob::Continuable\n+\n+  def perform(import_id)\n+    # Always runs on job start, even when resuming from an interrupted step.\n+    @import = Import.find(import_id)\n+\n+    # Step defined using a block\n+    step :initialize do\n+      @import.initialize\n+    end\n+\n+    # Step with a cursor \u2014 progress is saved and resumed if the job is interrupted\n+    step :process do |step|\n+      @import.records.find_each(start: step.cursor) do |record|\n+        record.process\n+        step.advance! from: record.id\n+      end\n+    end\n+\n+    # Step defined by referencing a method\n+    step :finalize\n+  end\n+\n+  private\n+    def finalize\n+      @import.finalize",
        "comment_created_at": "2025-06-17T15:27:38+00:00",
        "comment_author": "satyakampandya",
        "comment_body": "As far as I understand, yes - if the `finalize` method takes 10 minutes and gets interrupted by a deployment, and no continuation methods like `step`, `.checkpoint!`, `.advance!`, or `.set!` are called during that time, then the job might just get stopped without saving any progress. That would mean it could start over from the beginning, depending on how retries are set up.\r\n\r\nSo yeah, you're right, for long-running tasks, it seems important to call one of those methods regularly to make sure progress isn\u2019t lost if the job shuts down mid-way.\r\n\r\nThis feature was added recently by @djmb in [PR #55127](https://github.com/rails/rails/pull/55127), so tagging him in case he\u2019d like to chime in and clarify any edge cases or gotchas I might have missed. \ud83d\ude4f",
        "pr_file_module": null
      },
      {
        "comment_id": "2154563691",
        "repo_full_name": "rails/rails",
        "pr_number": 55193,
        "pr_file": "guides/source/active_job_basics.md",
        "discussion_id": "2150283629",
        "commented_code": "@@ -671,6 +671,56 @@ number as more important.\n [`queue_with_priority`]:\n     https://api.rubyonrails.org/classes/ActiveJob/QueuePriority/ClassMethods.html#method-i-queue_with_priority\n \n+Job Continuations\n+-----------------\n+\n+Jobs can be split into resumable steps using continuations. This is useful when\n+a job may be interrupted - for example, during queue shutdown. When using\n+continuations, the job can resume from the last completed step, avoiding the\n+need to restart from the beginning.\n+\n+To use continuations, include the `ActiveJob::Continuable` module. You can then\n+define each step using the `step` method inside the `perform` method. Each step can\n+be declared with a block or by referencing a method name.\n+\n+```ruby\n+class ProcessImportJob < ApplicationJob\n+  include ActiveJob::Continuable\n+\n+  def perform(import_id)\n+    # Always runs on job start, even when resuming from an interrupted step.\n+    @import = Import.find(import_id)\n+\n+    # Step defined using a block\n+    step :initialize do\n+      @import.initialize\n+    end\n+\n+    # Step with a cursor \u2014 progress is saved and resumed if the job is interrupted\n+    step :process do |step|\n+      @import.records.find_each(start: step.cursor) do |record|\n+        record.process\n+        step.advance! from: record.id\n+      end\n+    end\n+\n+    # Step defined by referencing a method\n+    step :finalize\n+  end\n+\n+  private\n+    def finalize\n+      @import.finalize",
        "comment_created_at": "2025-06-18T13:09:55+00:00",
        "comment_author": "djmb",
        "comment_body": "Yes that's right - checkpoints need to be created by the job, so if you don't create them often enough then the progress could be lost.\r\n\r\nReally I guess the answer is not to have single actions that take that long. It's a good constraint to work with. SQL can be optimized and downloads can maybe by split by using range requests so there's often a way. Long running things that can't be split up (say shelling out to ffmpeg or gzip or something like that) could be run in a separate thread.\r\n\r\nBut I'm sure there will be cases where that's not possible or desirable. Maybe we need a mechanism to deliberately interrupt the job to save progress before doing something slow. I'll have a think about that.",
        "pr_file_module": null
      },
      {
        "comment_id": "2154637907",
        "repo_full_name": "rails/rails",
        "pr_number": 55193,
        "pr_file": "guides/source/active_job_basics.md",
        "discussion_id": "2150283629",
        "commented_code": "@@ -671,6 +671,56 @@ number as more important.\n [`queue_with_priority`]:\n     https://api.rubyonrails.org/classes/ActiveJob/QueuePriority/ClassMethods.html#method-i-queue_with_priority\n \n+Job Continuations\n+-----------------\n+\n+Jobs can be split into resumable steps using continuations. This is useful when\n+a job may be interrupted - for example, during queue shutdown. When using\n+continuations, the job can resume from the last completed step, avoiding the\n+need to restart from the beginning.\n+\n+To use continuations, include the `ActiveJob::Continuable` module. You can then\n+define each step using the `step` method inside the `perform` method. Each step can\n+be declared with a block or by referencing a method name.\n+\n+```ruby\n+class ProcessImportJob < ApplicationJob\n+  include ActiveJob::Continuable\n+\n+  def perform(import_id)\n+    # Always runs on job start, even when resuming from an interrupted step.\n+    @import = Import.find(import_id)\n+\n+    # Step defined using a block\n+    step :initialize do\n+      @import.initialize\n+    end\n+\n+    # Step with a cursor \u2014 progress is saved and resumed if the job is interrupted\n+    step :process do |step|\n+      @import.records.find_each(start: step.cursor) do |record|\n+        record.process\n+        step.advance! from: record.id\n+      end\n+    end\n+\n+    # Step defined by referencing a method\n+    step :finalize\n+  end\n+\n+  private\n+    def finalize\n+      @import.finalize",
        "comment_created_at": "2025-06-18T13:37:50+00:00",
        "comment_author": "MiroslavCsonka",
        "comment_body": "Thanks, gentlemen, for the clarification. That's the behaviour I've been seeing in our production job.\r\n\r\nIt takes 6 hours, but basically, it downloads tens of GB of zip files from S3, unwraps them, imports them into the database, and then recomputes some statistics on top of it. Everything, except the last stage, could be done in 5-second chunks, but the last bit is a problem since if that gets interrupted, it has to start from scratch (redownload, unzip, parse CSV, etc.). The recomputation is the problem since it's a single materialised view, which takes 90 minutes at the moment, so it's hard to say if we can do it within 5 seconds. We would need to improve the performance at least 1000 times \ud83d\ude05\r\n\r\nI liked the idea of steps, so I came up with [this gist](https://gist.github.com/MiroslavCsonka/c13674099ce1366d2e774bc05dcd1fe1). It does a \"step\" (I called it stage so it doesn't clash with Rails), but the idea is to schedule another job to do the next stage.",
        "pr_file_module": null
      },
      {
        "comment_id": "2157018355",
        "repo_full_name": "rails/rails",
        "pr_number": 55193,
        "pr_file": "guides/source/active_job_basics.md",
        "discussion_id": "2150283629",
        "commented_code": "@@ -671,6 +671,56 @@ number as more important.\n [`queue_with_priority`]:\n     https://api.rubyonrails.org/classes/ActiveJob/QueuePriority/ClassMethods.html#method-i-queue_with_priority\n \n+Job Continuations\n+-----------------\n+\n+Jobs can be split into resumable steps using continuations. This is useful when\n+a job may be interrupted - for example, during queue shutdown. When using\n+continuations, the job can resume from the last completed step, avoiding the\n+need to restart from the beginning.\n+\n+To use continuations, include the `ActiveJob::Continuable` module. You can then\n+define each step using the `step` method inside the `perform` method. Each step can\n+be declared with a block or by referencing a method name.\n+\n+```ruby\n+class ProcessImportJob < ApplicationJob\n+  include ActiveJob::Continuable\n+\n+  def perform(import_id)\n+    # Always runs on job start, even when resuming from an interrupted step.\n+    @import = Import.find(import_id)\n+\n+    # Step defined using a block\n+    step :initialize do\n+      @import.initialize\n+    end\n+\n+    # Step with a cursor \u2014 progress is saved and resumed if the job is interrupted\n+    step :process do |step|\n+      @import.records.find_each(start: step.cursor) do |record|\n+        record.process\n+        step.advance! from: record.id\n+      end\n+    end\n+\n+    # Step defined by referencing a method\n+    step :finalize\n+  end\n+\n+  private\n+    def finalize\n+      @import.finalize",
        "comment_created_at": "2025-06-19T13:26:01+00:00",
        "comment_author": "djmb",
        "comment_body": "Thanks for that pointer - @MiroslavCsonka. I think this is going to be a common problem, so inspired by your gist I've added a [PR for isolated steps](https://github.com/rails/rails/pull/55212).",
        "pr_file_module": null
      },
      {
        "comment_id": "2157230243",
        "repo_full_name": "rails/rails",
        "pr_number": 55193,
        "pr_file": "guides/source/active_job_basics.md",
        "discussion_id": "2150283629",
        "commented_code": "@@ -671,6 +671,56 @@ number as more important.\n [`queue_with_priority`]:\n     https://api.rubyonrails.org/classes/ActiveJob/QueuePriority/ClassMethods.html#method-i-queue_with_priority\n \n+Job Continuations\n+-----------------\n+\n+Jobs can be split into resumable steps using continuations. This is useful when\n+a job may be interrupted - for example, during queue shutdown. When using\n+continuations, the job can resume from the last completed step, avoiding the\n+need to restart from the beginning.\n+\n+To use continuations, include the `ActiveJob::Continuable` module. You can then\n+define each step using the `step` method inside the `perform` method. Each step can\n+be declared with a block or by referencing a method name.\n+\n+```ruby\n+class ProcessImportJob < ApplicationJob\n+  include ActiveJob::Continuable\n+\n+  def perform(import_id)\n+    # Always runs on job start, even when resuming from an interrupted step.\n+    @import = Import.find(import_id)\n+\n+    # Step defined using a block\n+    step :initialize do\n+      @import.initialize\n+    end\n+\n+    # Step with a cursor \u2014 progress is saved and resumed if the job is interrupted\n+    step :process do |step|\n+      @import.records.find_each(start: step.cursor) do |record|\n+        record.process\n+        step.advance! from: record.id\n+      end\n+    end\n+\n+    # Step defined by referencing a method\n+    step :finalize\n+  end\n+\n+  private\n+    def finalize\n+      @import.finalize",
        "comment_created_at": "2025-06-19T14:58:56+00:00",
        "comment_author": "MiroslavCsonka",
        "comment_body": "Oh nice! Once the CI build is green, happy to upgrade our prod and test it out",
        "pr_file_module": null
      }
    ]
  }
]
