---
title: Initialize nil-prone variables
description: 'Always initialize variables that might be nil to appropriate default
  values to prevent unexpected behavior. For boolean flags, explicitly initialize
  to false in constructors or initialization methods:'
repository: rails/rails
label: Null Handling
language: Ruby
comments_count: 5
repository_stars: 57027
---

Always initialize variables that might be nil to appropriate default values to prevent unexpected behavior. For boolean flags, explicitly initialize to false in constructors or initialization methods:

```ruby
def initialize
  @unsubscribed = false  # Clear and explicit boolean state
end
```

For collections, initialize to empty arrays or hashes rather than nil. When setting defaults, use `||=` or `Hash#reverse_merge!` to assign values only when current value is nil:

```ruby
@options[:autocomplete] ||= "off"  # Only assigns if nil
# or
@options.reverse_merge!(autocomplete: "off")
```

When implementing predicate methods, use explicit `== true` comparison to ensure they return true or false, never nil:

```ruby
def define_predicate_method(name)
  define_method("#{name}?") { public_send(name) == true }
end
```

For complex types like JSON, provide sensible defaults:

```ruby
# When handling JSON type
when :json then {}  # Or use a more descriptive example structure
```

This proactive approach prevents nil-related errors and ensures consistent behavior throughout your application lifecycle.


[
  {
    "discussion_id": "2153628612",
    "pr_number": 55201,
    "pr_file": "actioncable/lib/action_cable/channel/base.rb",
    "created_at": "2025-06-18T04:47:26+00:00",
    "commented_code": "# cleanup with callbacks. This method is not intended to be called directly by\n      # the user. Instead, override the #unsubscribed callback.\n      def unsubscribe_from_channel # :nodoc:\n        @unsubscribed = true",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2153628612",
        "repo_full_name": "rails/rails",
        "pr_number": 55201,
        "pr_file": "actioncable/lib/action_cable/channel/base.rb",
        "discussion_id": "2153628612",
        "commented_code": "@@ -200,11 +200,16 @@ def subscribe_to_channel\n       # cleanup with callbacks. This method is not intended to be called directly by\n       # the user. Instead, override the #unsubscribed callback.\n       def unsubscribe_from_channel # :nodoc:\n+        @unsubscribed = true",
        "comment_created_at": "2025-06-18T04:47:26+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider initializing the @unsubscribed instance variable to false (e.g., in the channel's constructor or subscribe_to_channel method) to ensure a clear and explicit boolean state throughout the channel lifecycle.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1447646417",
    "pr_number": 46376,
    "pr_file": "activemodel/lib/active_model/attribute_registration.rb",
    "created_at": "2024-01-10T16:42:46+00:00",
    "commented_code": "def resolve_type_name(name, **options)\n          Type.lookup(name, **options)\n        end\n\n        def define_predicate_method(name)\n          define_method(\"#{name}?\") { public_send(name) == true }",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1447646417",
        "repo_full_name": "rails/rails",
        "pr_number": 46376,
        "pr_file": "activemodel/lib/active_model/attribute_registration.rb",
        "discussion_id": "1447646417",
        "commented_code": "@@ -72,6 +73,10 @@ def resolve_attribute_name(name)\n         def resolve_type_name(name, **options)\n           Type.lookup(name, **options)\n         end\n+\n+        def define_predicate_method(name)\n+          define_method(\"#{name}?\") { public_send(name) == true }",
        "comment_created_at": "2024-01-10T16:42:46+00:00",
        "comment_author": "nvasilevski",
        "comment_body": "Just to clarify, `== true` part was added intentionally to make the method strictly return a boolean? (Never `nil`)\r\n\r\nI think this is a reasonable design even though technically we have an option to drop this comparison as most of the values will be coerced to `true` or `false` and `nil` is falsey so it wouldn't be wrong. \r\n\r\nBut personally I'm leaning towards keeping the comparison to avoid situations like:\r\n`Person.new.loves_ruby? # => nil` which from falseness perspective is \"No\" but in reality could mean \"the person is not sure yet\"",
        "pr_file_module": null
      },
      {
        "comment_id": "1451649229",
        "repo_full_name": "rails/rails",
        "pr_number": 46376,
        "pr_file": "activemodel/lib/active_model/attribute_registration.rb",
        "discussion_id": "1447646417",
        "commented_code": "@@ -72,6 +73,10 @@ def resolve_attribute_name(name)\n         def resolve_type_name(name, **options)\n           Type.lookup(name, **options)\n         end\n+\n+        def define_predicate_method(name)\n+          define_method(\"#{name}?\") { public_send(name) == true }",
        "comment_created_at": "2024-01-14T03:48:41+00:00",
        "comment_author": "zzak",
        "comment_body": "@nvasilevski Can you think of a situation where we make this distinction? I was under the assumption that we care more about the [semantics](https://edgeguides.rubyonrails.org/api_documentation_guidelines.html#booleans) than the specific values \ud83e\udd14 ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1825409899",
    "pr_number": 53512,
    "pr_file": "actionview/lib/action_view/helpers/tags/hidden_field.rb",
    "created_at": "2024-11-01T04:16:16+00:00",
    "commented_code": "module Tags # :nodoc:\n      class HiddenField < TextField # :nodoc:\n        def render\n          @options[:autocomplete] = \"off\"\n          @options[:autocomplete] ||= \"off\"",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1825409899",
        "repo_full_name": "rails/rails",
        "pr_number": 53512,
        "pr_file": "actionview/lib/action_view/helpers/tags/hidden_field.rb",
        "discussion_id": "1825409899",
        "commented_code": "@@ -5,7 +5,7 @@ module Helpers\n     module Tags # :nodoc:\n       class HiddenField < TextField # :nodoc:\n         def render\n-          @options[:autocomplete] = \"off\"\n+          @options[:autocomplete] ||= \"off\"",
        "comment_created_at": "2024-11-01T04:16:16+00:00",
        "comment_author": "seanpdoyle",
        "comment_body": "Would this assign `\"off\"` if the tag were rendered with `autocomplete: false`?\r\n\r\nIf `\"off\"` should only ever supersede `nil`, would [Hash#reverse_merge!](https://edgeapi.rubyonrails.org/classes/Hash.html#method-i-reverse_merge-21) (or its `Hash#with_defaults!` alias) work here?",
        "pr_file_module": null
      },
      {
        "comment_id": "1825626671",
        "repo_full_name": "rails/rails",
        "pr_number": 53512,
        "pr_file": "actionview/lib/action_view/helpers/tags/hidden_field.rb",
        "discussion_id": "1825409899",
        "commented_code": "@@ -5,7 +5,7 @@ module Helpers\n     module Tags # :nodoc:\n       class HiddenField < TextField # :nodoc:\n         def render\n-          @options[:autocomplete] = \"off\"\n+          @options[:autocomplete] ||= \"off\"",
        "comment_created_at": "2024-11-01T09:27:04+00:00",
        "comment_author": "brendon",
        "comment_body": "`autocomplete: false` seems to generate `autocomplete=\"false\"` rather than remove the attribute. I guess it should be `autocomplete: nil` to remove the default?",
        "pr_file_module": null
      },
      {
        "comment_id": "1826511949",
        "repo_full_name": "rails/rails",
        "pr_number": 53512,
        "pr_file": "actionview/lib/action_view/helpers/tags/hidden_field.rb",
        "discussion_id": "1825409899",
        "commented_code": "@@ -5,7 +5,7 @@ module Helpers\n     module Tags # :nodoc:\n       class HiddenField < TextField # :nodoc:\n         def render\n-          @options[:autocomplete] = \"off\"\n+          @options[:autocomplete] ||= \"off\"",
        "comment_created_at": "2024-11-02T06:40:29+00:00",
        "comment_author": "brendon",
        "comment_body": "I've used `reverse_merge!` here since `with_defaults!` makes less sense.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2033056367",
    "pr_number": 54886,
    "pr_file": "railties/lib/rails/generators/generated_attribute.rb",
    "created_at": "2025-04-08T12:12:07+00:00",
    "commented_code": "when :references, :belongs_to,\n                          :attachment, :attachments,\n                          :rich_text                   then nil\n                     when :json                        then {}",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2033056367",
        "repo_full_name": "rails/rails",
        "pr_number": 54886,
        "pr_file": "railties/lib/rails/generators/generated_attribute.rb",
        "discussion_id": "2033056367",
        "commented_code": "@@ -148,6 +148,7 @@ def default\n                      when :references, :belongs_to,\n                           :attachment, :attachments,\n                           :rich_text                   then nil\n+                     when :json                        then {}",
        "comment_created_at": "2025-04-08T12:12:07+00:00",
        "comment_author": "stevepolitodesign",
        "comment_body": "This might require more thought. We really need to return a String, not a Hash.\r\n\r\n```suggestion\r\n                     when :json                        then '{\"key\":  \"value\"}'\r\n```\r\n\r\nBut that's pretty cumbersome. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2033061960",
        "repo_full_name": "rails/rails",
        "pr_number": 54886,
        "pr_file": "railties/lib/rails/generators/generated_attribute.rb",
        "discussion_id": "2033056367",
        "commented_code": "@@ -148,6 +148,7 @@ def default\n                      when :references, :belongs_to,\n                           :attachment, :attachments,\n                           :rich_text                   then nil\n+                     when :json                        then {}",
        "comment_created_at": "2025-04-08T12:15:21+00:00",
        "comment_author": "stevepolitodesign",
        "comment_body": "I _think_ we can also use YAML to describe JSON too, which might be the better solution, and would warrant keeping this value as `nil`.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1934234172",
    "pr_number": 54397,
    "pr_file": "activerecord/lib/active_record/connection_adapters/postgresql/schema_creation.rb",
    "created_at": "2025-01-29T16:41:58+00:00",
    "commented_code": "module PostgreSQL\n      class SchemaCreation < SchemaCreation # :nodoc:\n        private\n          delegate :quoted_include_columns_for_index, to: :@conn\n          delegate :quoted_include_columns_for_index, :create_enum, to: :@conn\n\n          def visit_TableDefinition(o)\n            create_enums(o.columns)\n            super\n          end\n\n          def visit_AlterTable(o)\n            create_enums(o.adds.map(&:column))\n            sql = super\n            sql << o.constraint_validations.map { |fk| visit_ValidateConstraint fk }.join(\" \")\n            sql << o.exclusion_constraint_adds.map { |con| visit_AddExclusionConstraint con }.join(\" \")\n            sql << o.unique_constraint_adds.map { |con| visit_AddUniqueConstraint con }.join(\" \")\n          end\n\n          def create_enums(columns)\n            return unless enums_to_create = columns.select { |c| c.type == :enum && c.options[:values] }",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1934234172",
        "repo_full_name": "rails/rails",
        "pr_number": 54397,
        "pr_file": "activerecord/lib/active_record/connection_adapters/postgresql/schema_creation.rb",
        "discussion_id": "1934234172",
        "commented_code": "@@ -5,15 +5,30 @@ module ConnectionAdapters\n     module PostgreSQL\n       class SchemaCreation < SchemaCreation # :nodoc:\n         private\n-          delegate :quoted_include_columns_for_index, to: :@conn\n+          delegate :quoted_include_columns_for_index, :create_enum, to: :@conn\n+\n+          def visit_TableDefinition(o)\n+            create_enums(o.columns)\n+            super\n+          end\n \n           def visit_AlterTable(o)\n+            create_enums(o.adds.map(&:column))\n             sql = super\n             sql << o.constraint_validations.map { |fk| visit_ValidateConstraint fk }.join(\" \")\n             sql << o.exclusion_constraint_adds.map { |con| visit_AddExclusionConstraint con }.join(\" \")\n             sql << o.unique_constraint_adds.map { |con| visit_AddUniqueConstraint con }.join(\" \")\n           end\n \n+          def create_enums(columns)\n+            return unless enums_to_create = columns.select { |c| c.type == :enum && c.options[:values] }",
        "comment_created_at": "2025-01-29T16:41:58+00:00",
        "comment_author": "nvasilevski",
        "comment_body": "`select` always returns an `Array` which will be a truthy value so we never return. Let's explicitly check for an `empty?` result \r\n\r\n```suggestion\r\n            enums_to_create = columns.select { |c| c.type == :enum && c.options[:values] }\r\n            return if  enums_to_create.empty?\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1934235047",
        "repo_full_name": "rails/rails",
        "pr_number": 54397,
        "pr_file": "activerecord/lib/active_record/connection_adapters/postgresql/schema_creation.rb",
        "discussion_id": "1934234172",
        "commented_code": "@@ -5,15 +5,30 @@ module ConnectionAdapters\n     module PostgreSQL\n       class SchemaCreation < SchemaCreation # :nodoc:\n         private\n-          delegate :quoted_include_columns_for_index, to: :@conn\n+          delegate :quoted_include_columns_for_index, :create_enum, to: :@conn\n+\n+          def visit_TableDefinition(o)\n+            create_enums(o.columns)\n+            super\n+          end\n \n           def visit_AlterTable(o)\n+            create_enums(o.adds.map(&:column))\n             sql = super\n             sql << o.constraint_validations.map { |fk| visit_ValidateConstraint fk }.join(\" \")\n             sql << o.exclusion_constraint_adds.map { |con| visit_AddExclusionConstraint con }.join(\" \")\n             sql << o.unique_constraint_adds.map { |con| visit_AddUniqueConstraint con }.join(\" \")\n           end\n \n+          def create_enums(columns)\n+            return unless enums_to_create = columns.select { |c| c.type == :enum && c.options[:values] }",
        "comment_created_at": "2025-01-29T16:42:28+00:00",
        "comment_author": "nvasilevski",
        "comment_body": "Actually, I think the whole `return` can be omitted. If `enums_to_create` is empty - `enums_to_create.each` will do nothing which is equal to returning ",
        "pr_file_module": null
      },
      {
        "comment_id": "1934239553",
        "repo_full_name": "rails/rails",
        "pr_number": 54397,
        "pr_file": "activerecord/lib/active_record/connection_adapters/postgresql/schema_creation.rb",
        "discussion_id": "1934234172",
        "commented_code": "@@ -5,15 +5,30 @@ module ConnectionAdapters\n     module PostgreSQL\n       class SchemaCreation < SchemaCreation # :nodoc:\n         private\n-          delegate :quoted_include_columns_for_index, to: :@conn\n+          delegate :quoted_include_columns_for_index, :create_enum, to: :@conn\n+\n+          def visit_TableDefinition(o)\n+            create_enums(o.columns)\n+            super\n+          end\n \n           def visit_AlterTable(o)\n+            create_enums(o.adds.map(&:column))\n             sql = super\n             sql << o.constraint_validations.map { |fk| visit_ValidateConstraint fk }.join(\" \")\n             sql << o.exclusion_constraint_adds.map { |con| visit_AddExclusionConstraint con }.join(\" \")\n             sql << o.unique_constraint_adds.map { |con| visit_AddUniqueConstraint con }.join(\" \")\n           end\n \n+          def create_enums(columns)\n+            return unless enums_to_create = columns.select { |c| c.type == :enum && c.options[:values] }",
        "comment_created_at": "2025-01-29T16:45:34+00:00",
        "comment_author": "jenshenny",
        "comment_body": "> select always returns an Array which will be a truthy value so we never return\r\n\r\n\ud83e\udd26\u200d\u2640\ufe0f right, yeah I think we can omit the return then",
        "pr_file_module": null
      }
    ]
  }
]
