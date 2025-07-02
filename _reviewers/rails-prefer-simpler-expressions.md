---
title: Prefer simpler expressions
description: "Always choose the simplest, most readable way to express your code logic.\
  \ Unnecessary complexity makes code harder to understand and maintain. \n\nWhen\
  \ writing conditionals, method calls, or data transformations, ask yourself: \"\
  Is there a clearer way to express this?\""
repository: rails/rails
label: Code Style
language: Ruby
comments_count: 6
repository_stars: 57027
---

Always choose the simplest, most readable way to express your code logic. Unnecessary complexity makes code harder to understand and maintain. 

When writing conditionals, method calls, or data transformations, ask yourself: "Is there a clearer way to express this?"

Examples of simplifying expressions:

1. Remove redundant conditionals when context makes them obvious:
```ruby
# Instead of this
if reflection.belongs_to? && model.ignored_columns.include?(reflection.foreign_key.to_s)

# Use this (when already in a belongs_to context)
if model.ignored_columns.include?(reflection.foreign_key.to_s)
```

2. Format array display consistently:
```ruby
# Instead of this verbose approach
filter_names = @filters.length == 1 ? @filters.first.inspect : "[#{@filters.map(&:inspect).join(", ")}]"

# Use the built-in inspect method
filter_names = @filters.length == 1 ? @filters.first.inspect : @filters.inspect
```

3. Use direct array methods instead of custom iterations:
```ruby
# Instead of searching with any?
unless ActiveStorage.supported_image_processing_methods.any? { |method| method_name == method }

# Use the more direct include?
unless ActiveStorage.supported_image_processing_methods.include?(method_name)
```

4. Optimize iterations when appropriate:
```ruby
# Instead of filtering then iterating
enums_to_create = columns.select { |c| c.type == :enum && c.options[:values] }
enums_to_create.each do |c|
  # process enum
end

# Check inside the loop to avoid an extra iteration
columns.each do |c|
  next unless c.type == :enum && c.options[:values]
  # process enum
end
```

5. Use modern language features when they improve readability:
```ruby
# Instead of ignoring block arguments
def add_binds(binds, proc_for_binds = nil, &_)

# Use anonymous block syntax (Ruby 2.7+)
def add_binds(binds, proc_for_binds = nil, &)
```

Remember that code is read far more often than it's written. Optimizing for readability pays dividends throughout the lifecycle of your application.


[
  {
    "discussion_id": "1770560982",
    "pr_number": 53007,
    "pr_file": "activerecord/lib/active_record/associations/builder/belongs_to.rb",
    "created_at": "2024-09-22T13:55:59+00:00",
    "commented_code": "[:destroy, :delete, :destroy_async]\n    end\n\n    def self.validate_reflection!(model, reflection)\n      if reflection.belongs_to? && model.ignored_columns.include?(reflection.foreign_key.to_s)",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1770560982",
        "repo_full_name": "rails/rails",
        "pr_number": 53007,
        "pr_file": "activerecord/lib/active_record/associations/builder/belongs_to.rb",
        "discussion_id": "1770560982",
        "commented_code": "@@ -17,6 +17,12 @@ def self.valid_dependent_options\n       [:destroy, :delete, :destroy_async]\n     end\n \n+    def self.validate_reflection!(model, reflection)\n+      if reflection.belongs_to? && model.ignored_columns.include?(reflection.foreign_key.to_s)",
        "comment_created_at": "2024-09-22T13:55:59+00:00",
        "comment_author": "nvasilevski",
        "comment_body": "Could `reflection.belongs_to?` be omitted? We are in a `belongs_to` reflection builder so `reflection` being `belongs_to` should be implied. Unless there is a corner case I'm missing \r\n\r\n```suggestion\r\n      if model.ignored_columns.include?(reflection.foreign_key.to_s)\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1770577535",
        "repo_full_name": "rails/rails",
        "pr_number": 53007,
        "pr_file": "activerecord/lib/active_record/associations/builder/belongs_to.rb",
        "discussion_id": "1770560982",
        "commented_code": "@@ -17,6 +17,12 @@ def self.valid_dependent_options\n       [:destroy, :delete, :destroy_async]\n     end\n \n+    def self.validate_reflection!(model, reflection)\n+      if reflection.belongs_to? && model.ignored_columns.include?(reflection.foreign_key.to_s)",
        "comment_created_at": "2024-09-22T15:21:12+00:00",
        "comment_author": "rubyrider",
        "comment_body": "You are right I actually forgot after moving this logic from association to belongs_to builder. I will push tonight and update you. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1770606464",
        "repo_full_name": "rails/rails",
        "pr_number": 53007,
        "pr_file": "activerecord/lib/active_record/associations/builder/belongs_to.rb",
        "discussion_id": "1770560982",
        "commented_code": "@@ -17,6 +17,12 @@ def self.valid_dependent_options\n       [:destroy, :delete, :destroy_async]\n     end\n \n+    def self.validate_reflection!(model, reflection)\n+      if reflection.belongs_to? && model.ignored_columns.include?(reflection.foreign_key.to_s)",
        "comment_created_at": "2024-09-22T18:11:11+00:00",
        "comment_author": "rubyrider",
        "comment_body": "@nvasilevski  thank you so much for pointing out the redundant belongs_to? check. I just pushed the refactoring. Let me know if that is okey.\r\n\r\nRegarding when foreign key does not exists: I think we can consider a new pull request. what do you think? I think we can keep this pull request only for the given context. Let me know your feedback . \r\n\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "734468437",
    "pr_number": 43487,
    "pr_file": "actionpack/lib/abstract_controller/callbacks.rb",
    "created_at": "2021-10-22T11:45:00+00:00",
    "commented_code": "define_callbacks :process_action,\n                       terminator: ->(controller, result_lambda) { result_lambda.call; controller.performed? },\n                       skip_after_callbacks_if_terminated: true\n      mattr_accessor :raise_on_missing_callback_actions, default: false\n    end\n\n    class ActionFilter # :nodoc:\n      def initialize(actions)\n      def initialize(filters, conditional_key, actions)\n        @filters = filters.to_a\n        @conditional_key = conditional_key\n        @actions = Array(actions).map(&:to_s).to_set\n      end\n\n      def match?(controller)\n        if controller.raise_on_missing_callback_actions\n          missing_action = @actions.find { |action| !controller.available_action?(action) }\n          if missing_action\n            filter_names = @filters.length == 1 ? @filters.first.inspect : \"[#{@filters.map(&:inspect).join(\", \")}]\"",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "734468437",
        "repo_full_name": "rails/rails",
        "pr_number": 43487,
        "pr_file": "actionpack/lib/abstract_controller/callbacks.rb",
        "discussion_id": "734468437",
        "commented_code": "@@ -33,14 +33,26 @@ module Callbacks\n       define_callbacks :process_action,\n                        terminator: ->(controller, result_lambda) { result_lambda.call; controller.performed? },\n                        skip_after_callbacks_if_terminated: true\n+      mattr_accessor :raise_on_missing_callback_actions, default: false\n     end\n \n     class ActionFilter # :nodoc:\n-      def initialize(actions)\n+      def initialize(filters, conditional_key, actions)\n+        @filters = filters.to_a\n+        @conditional_key = conditional_key\n         @actions = Array(actions).map(&:to_s).to_set\n       end\n \n       def match?(controller)\n+        if controller.raise_on_missing_callback_actions\n+          missing_action = @actions.find { |action| !controller.available_action?(action) }\n+          if missing_action\n+            filter_names = @filters.length == 1 ? @filters.first.inspect : \"[#{@filters.map(&:inspect).join(\", \")}]\"",
        "comment_created_at": "2021-10-22T11:45:00+00:00",
        "comment_author": "DNNX",
        "comment_body": "This is equivalent, but way easier to read (and most likely faster):\r\n\r\n```suggestion\r\n            filter_names = @filters.length == 1 ? @filters.first.inspect : @filters.inspect\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1947023442",
    "pr_number": 54332,
    "pr_file": "activerecord/lib/active_record/connection_adapters/mysql/schema_creation.rb",
    "created_at": "2025-02-07T19:00:48+00:00",
    "commented_code": "sql << \"USING #{o.using}\" if o.using\n            sql << \"ON #{quote_table_name(o.table)}\" if create\n            sql << \"(#{quoted_columns(o)})\"\n            sql << \"INVISIBLE\" if o.disabled? && !mariadb?\n            sql << \"IGNORED\" if o.disabled? && mariadb?",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1947023442",
        "repo_full_name": "rails/rails",
        "pr_number": 54332,
        "pr_file": "activerecord/lib/active_record/connection_adapters/mysql/schema_creation.rb",
        "discussion_id": "1947023442",
        "commented_code": "@@ -49,6 +49,8 @@ def visit_IndexDefinition(o, create = false)\n             sql << \"USING #{o.using}\" if o.using\n             sql << \"ON #{quote_table_name(o.table)}\" if create\n             sql << \"(#{quoted_columns(o)})\"\n+            sql << \"INVISIBLE\" if o.disabled? && !mariadb?\n+            sql << \"IGNORED\" if o.disabled? && mariadb?",
        "comment_created_at": "2025-02-07T19:00:48+00:00",
        "comment_author": "adrianna-chang-shopify",
        "comment_body": "```suggestion\r\n            if o.disabled?\r\n              sql << \"#{mariadb? ? \"IGNORED\" : \"INVISIBLE\"}\"\r\n            end\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1954571154",
        "repo_full_name": "rails/rails",
        "pr_number": 54332,
        "pr_file": "activerecord/lib/active_record/connection_adapters/mysql/schema_creation.rb",
        "discussion_id": "1947023442",
        "commented_code": "@@ -49,6 +49,8 @@ def visit_IndexDefinition(o, create = false)\n             sql << \"USING #{o.using}\" if o.using\n             sql << \"ON #{quote_table_name(o.table)}\" if create\n             sql << \"(#{quoted_columns(o)})\"\n+            sql << \"INVISIBLE\" if o.disabled? && !mariadb?\n+            sql << \"IGNORED\" if o.disabled? && mariadb?",
        "comment_created_at": "2025-02-13T14:10:10+00:00",
        "comment_author": "mtaner",
        "comment_body": "I decided to keep it the original way as I think it is easier to read ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1934246531",
    "pr_number": 54397,
    "pr_file": "activerecord/lib/active_record/connection_adapters/postgresql/schema_creation.rb",
    "created_at": "2025-01-29T16:50:07+00:00",
    "commented_code": "module PostgreSQL\n      class SchemaCreation < SchemaCreation # :nodoc:\n        private\n          delegate :quoted_include_columns_for_index, to: :@conn\n          delegate :quoted_include_columns_for_index, :create_enum, to: :@conn\n\n          def visit_TableDefinition(o)\n            create_enums(o.columns)\n            super\n          end\n\n          def visit_AlterTable(o)\n            create_enums(o.adds.map(&:column))\n            sql = super\n            sql << o.constraint_validations.map { |fk| visit_ValidateConstraint fk }.join(\" \")\n            sql << o.exclusion_constraint_adds.map { |con| visit_AddExclusionConstraint con }.join(\" \")\n            sql << o.unique_constraint_adds.map { |con| visit_AddUniqueConstraint con }.join(\" \")\n          end\n\n          def create_enums(columns)\n            enums_to_create = columns.select { |c| c.type == :enum && c.options[:values] }\n\n            enums_to_create.each do |c|\n              enum_type = c.options[:enum_type] || c.name",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1934246531",
        "repo_full_name": "rails/rails",
        "pr_number": 54397,
        "pr_file": "activerecord/lib/active_record/connection_adapters/postgresql/schema_creation.rb",
        "discussion_id": "1934246531",
        "commented_code": "@@ -5,15 +5,30 @@ module ConnectionAdapters\n     module PostgreSQL\n       class SchemaCreation < SchemaCreation # :nodoc:\n         private\n-          delegate :quoted_include_columns_for_index, to: :@conn\n+          delegate :quoted_include_columns_for_index, :create_enum, to: :@conn\n+\n+          def visit_TableDefinition(o)\n+            create_enums(o.columns)\n+            super\n+          end\n \n           def visit_AlterTable(o)\n+            create_enums(o.adds.map(&:column))\n             sql = super\n             sql << o.constraint_validations.map { |fk| visit_ValidateConstraint fk }.join(\" \")\n             sql << o.exclusion_constraint_adds.map { |con| visit_AddExclusionConstraint con }.join(\" \")\n             sql << o.unique_constraint_adds.map { |con| visit_AddUniqueConstraint con }.join(\" \")\n           end\n \n+          def create_enums(columns)\n+            enums_to_create = columns.select { |c| c.type == :enum && c.options[:values] }\n+\n+            enums_to_create.each do |c|\n+              enum_type = c.options[:enum_type] || c.name",
        "comment_created_at": "2025-01-29T16:50:07+00:00",
        "comment_author": "nvasilevski",
        "comment_body": "We could save one iteration by moving the check inside the loop. But this code is not on a hot path so I think we should optimize for readability. And building `enums_to_create` on a separate line may be a better option from readability perspective. So totally up to you! \r\n\r\n```suggestion\r\n            columns.each do |c|\r\n             \u00a0next unless c.type == :enum && c.options[:values]\r\n             \u00a0 \r\n              enum_type = c.options[:enum_type] || c.name\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1934285017",
        "repo_full_name": "rails/rails",
        "pr_number": 54397,
        "pr_file": "activerecord/lib/active_record/connection_adapters/postgresql/schema_creation.rb",
        "discussion_id": "1934246531",
        "commented_code": "@@ -5,15 +5,30 @@ module ConnectionAdapters\n     module PostgreSQL\n       class SchemaCreation < SchemaCreation # :nodoc:\n         private\n-          delegate :quoted_include_columns_for_index, to: :@conn\n+          delegate :quoted_include_columns_for_index, :create_enum, to: :@conn\n+\n+          def visit_TableDefinition(o)\n+            create_enums(o.columns)\n+            super\n+          end\n \n           def visit_AlterTable(o)\n+            create_enums(o.adds.map(&:column))\n             sql = super\n             sql << o.constraint_validations.map { |fk| visit_ValidateConstraint fk }.join(\" \")\n             sql << o.exclusion_constraint_adds.map { |con| visit_AddExclusionConstraint con }.join(\" \")\n             sql << o.unique_constraint_adds.map { |con| visit_AddUniqueConstraint con }.join(\" \")\n           end\n \n+          def create_enums(columns)\n+            enums_to_create = columns.select { |c| c.type == :enum && c.options[:values] }\n+\n+            enums_to_create.each do |c|\n+              enum_type = c.options[:enum_type] || c.name",
        "comment_created_at": "2025-01-29T17:15:18+00:00",
        "comment_author": "jenshenny",
        "comment_body": "I originally separated on another line for readability as you mentioned, but your suggestion is still plenty readable. Done!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "873169576",
    "pr_number": 45100,
    "pr_file": "activestorage/lib/active_storage/transformers/image_magick.rb",
    "created_at": "2022-05-15T13:25:56+00:00",
    "commented_code": "# frozen_string_literal: true\n\nmodule ActiveStorage\n  module Transformers\n    class ImageMagick < ImageProcessingTransformer\n      private\n        def processor\n          ImageProcessing::MiniMagick\n        end\n\n        def validate_transformation(name, argument)\n          method_name = name.to_s.tr(\"-\", \"_\")\n\n          unless ActiveStorage.supported_image_processing_methods.any? { |method| method_name == method }",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "873169576",
        "repo_full_name": "rails/rails",
        "pr_number": 45100,
        "pr_file": "activestorage/lib/active_storage/transformers/image_magick.rb",
        "discussion_id": "873169576",
        "commented_code": "@@ -0,0 +1,72 @@\n+# frozen_string_literal: true\n+\n+module ActiveStorage\n+  module Transformers\n+    class ImageMagick < ImageProcessingTransformer\n+      private\n+        def processor\n+          ImageProcessing::MiniMagick\n+        end\n+\n+        def validate_transformation(name, argument)\n+          method_name = name.to_s.tr(\"-\", \"_\")\n+\n+          unless ActiveStorage.supported_image_processing_methods.any? { |method| method_name == method }",
        "comment_created_at": "2022-05-15T13:25:56+00:00",
        "comment_author": "byroot",
        "comment_body": "I know you just moved it over, but I wonder why this isn't just:\r\n\r\n```suggestion\r\n          unless ActiveStorage.supported_image_processing_methods.include?(method_name)\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1930213694",
    "pr_number": 54361,
    "pr_file": "activerecord/lib/active_record/statement_cache.rb",
    "created_at": "2025-01-27T09:29:03+00:00",
    "commented_code": "self\n      end\n\n      def add_bind(obj)\n      def add_bind(obj, &_)\n        @binds << obj\n        @parts << Substitute.new\n        self\n      end\n\n      def add_binds(binds, proc_for_binds = nil)\n      def add_binds(binds, proc_for_binds = nil, &_)",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1930213694",
        "repo_full_name": "rails/rails",
        "pr_number": 54361,
        "pr_file": "activerecord/lib/active_record/statement_cache.rb",
        "discussion_id": "1930213694",
        "commented_code": "@@ -74,13 +74,13 @@ def <<(str)\n         self\n       end\n \n-      def add_bind(obj)\n+      def add_bind(obj, &_)\n         @binds << obj\n         @parts << Substitute.new\n         self\n       end\n \n-      def add_binds(binds, proc_for_binds = nil)\n+      def add_binds(binds, proc_for_binds = nil, &_)",
        "comment_created_at": "2025-01-27T09:29:03+00:00",
        "comment_author": "byroot",
        "comment_body": "We require 3.2 now, so you can use an anonymous block\r\n\r\n```suggestion\r\n      def add_binds(binds, proc_for_binds = nil, &)\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
