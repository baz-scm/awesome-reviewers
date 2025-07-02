---
title: Document APIs clearly
description: When designing and documenting APIs, prioritize clarity and completeness
  through concrete examples and accurate parameter descriptions. Your documentation
  should help developers understand both the basic usage and edge cases of your API.
repository: rails/rails
label: API
language: Markdown
comments_count: 6
repository_stars: 57027
---

When designing and documenting APIs, prioritize clarity and completeness through concrete examples and accurate parameter descriptions. Your documentation should help developers understand both the basic usage and edge cases of your API.

For parameter documentation:
- Explain what each parameter does and its default value
- Clearly indicate parameter limitations (like when they apply)
- Use proper formatting for parameter names (e.g., `api_timestamp_field:`)

Always include practical examples:
```ruby
# Good - shows parameter usage with examples
# acts_as_api_resource api_timestamp_field: :last_api_access
#
# Example:
class Product < ApplicationRecord
  acts_as_api_resource api_timestamp_field: :last_accessed_at
end
```

When designing callback-style APIs, follow Rails conventions where possible:
```ruby
# Option 1: Named options with method references or lambdas
has_one_attached :image, after_attached: :process_image

# Option 2: Configuration within blocks
has_one_attached :image do |attachable|
  attachable.after_attached do |blob|
    process_image(blob)
  end
end
```

Keep documentation consistent across all locations (guides and API reference), with simpler cases in guides and more complex edge cases in API reference documentation. This approach ensures developers can find the right information at the right time as they progress from basic to advanced usage.


[
  {
    "discussion_id": "2154568767",
    "pr_number": 55203,
    "pr_file": "guides/source/plugins.md",
    "created_at": "2025-06-18T13:12:04+00:00",
    "commented_code": "This section will explain how to add a method to String that will be available anywhere in your Rails application.\n\nIn this example you will add a method to String named `to_squawk`. To begin, create a new test file with a few assertions:\nWARNING: Before proceeding, it's important to understand that extending core\nclasses (like String, Array, Hash, etc.) should be used sparingly, if at all.\nCore class extensions can be brittle, dangerous, and are often\nunnecessary.<br></br> They can:</br>\n- Cause naming conflicts when multiple gems extend the same class with the same\n  method name</br>\n- Break unexpectedly when Ruby or Rails updates change core class behavior</br>\n- Make debugging difficult because it's not obvious where methods come from</br>\n- Create coupling issues between your plugin and other code<br></br> Better\nalternatives to consider:</br>\n- Create utility modules or helper classes instead</br>\n- Use composition over monkey patching</br>\n- Implement functionality as instance methods on your own classes<br></br> For\nmore details on why core class extensions can be problematic, see [The Case\nAgainst Monkey\nPatching](https://shopify.engineering/the-case-against-monkey-patching).\n<br></br> That said, understanding how core class extensions work is valuable.\nThe example below demonstrates the technique, but they should be used sparingly\n- consider whether it's the right approach for your specific use case.\n\nIn this example you will add a method to Integer named `requests_per_hour`.\n\nIn `lib/api_boost.rb`, add `require \"api_boost/core_ext\"`:\n\n```ruby\n# yaffle/test/core_ext_test.rb\n\nrequire \"test_helper\"\n\nclass CoreExtTest < ActiveSupport::TestCase\n  def test_to_squawk_prepends_the_word_squawk\n    assert_equal \"squawk! Hello World\", \"Hello World\".to_squawk\n  end\nend\n```\n\nRun `bin/test` to run the test. This test should fail because we haven't implemented the `to_squawk` method:\n\n```bash\n$ bin/test\nE\n\nError:\nCoreExtTest#test_to_squawk_prepends_the_word_squawk:\nNoMethodError: undefined method `to_squawk' for \"Hello World\":String\n\n# api_boost/lib/api_boost.rb\n\nbin/test /path/to/yaffle/test/core_ext_test.rb:4\nrequire \"api_boost/version\"\nrequire \"api_boost/railtie\"\nrequire \"api_boost/core_ext\"\n\n.\n\nFinished in 0.003358s, 595.6483 runs/s, 297.8242 assertions/s.\n2 runs, 1 assertions, 0 failures, 1 errors, 0 skips\n```\n\nGreat - now you are ready to start development.\n\nIn `lib/yaffle.rb`, add `require \"yaffle/core_ext\"`:\n\n```ruby\n# yaffle/lib/yaffle.rb\n\nrequire \"yaffle/version\"\nrequire \"yaffle/railtie\"\nrequire \"yaffle/core_ext\"\n\nmodule Yaffle\nmodule ApiBoost\n  # Your code goes here...\nend\n```\n\nFinally, create the `core_ext.rb` file and add the `to_squawk` method:\nCreate the `core_ext.rb` file and add a method to Integer to define a RateLimit that could define `10.requests_per_hour`, similar to `10.hours` that returns a Time.\n\n```ruby\n# yaffle/lib/yaffle/core_ext.rb\n# api_boost/lib/api_boost/core_ext.rb\n\nclass String\n  def to_squawk\n    \"squawk! #{self}\".strip\nApiBoost::RateLimit = Data.define(:requests, :per)\n\nclass Integer\n  def requests_per_hour\n    ApiBoost::RateLimit.new(self, :hour)\n  end\nend\n```\n\nTo test that your method does what it says it does, run the unit tests with `bin/test` from your plugin directory.\nTo see this in action, change to the `test/dummy` directory, start `bin/rails console`, and test the API response formatting:\n\n```bash\n$ bin/test\n...\n2 runs, 2 assertions, 0 failures, 0 errors, 0 skips\n$ cd test/dummy\n$ bin/rails console\n```\n\nTo see this in action, change to the `test/dummy` directory, start `bin/rails console`, and commence squawking:\n\n```irb\nirb> \"Hello World\".to_squawk\n=> \"squawk! Hello World\"\nirb> 10.requests_per_hour\n=> #<struct ApiBoost::RateLimit requests=10, per=:hour>\n```\n\nThe dummy application automatically loads your plugin, so any extensions you add are immediately available for testing.\n\nAdd an \"acts_as\" Method to Active Record\n----------------------------------------\n\nA common pattern in plugins is to add a method called `acts_as_something` to models. In this case, you\nwant to write a method called `acts_as_yaffle` that adds a `squawk` method to your Active Record models.\nwant to write a method called `acts_as_api_resource` that adds API-specific functionality to your Active Record models.\n\nTo begin, set up your files so that you have:\nLet\u2019s say you\u2019re building an API and you want to keep track of the last time a resource (like a `Product`) was accessed via that API. You might want to use that timestamp to:\n\n```ruby\n# yaffle/test/acts_as_yaffle_test.rb\n* throttle requests\n* show \u201clast active\u201d times in your admin panel\n* prioritize stale records for syncing\n\nrequire \"test_helper\"\nInstead of writing this logic in every model, you can use a shared plugin. The `acts_as_api_resource` method adds this functionality to any model, letting you track API activity by updating a timestamp field.\n\nclass ActsAsYaffleTest < ActiveSupport::TestCase\nend\n```\nTo begin, set up your files so that you have:\n\n```ruby\n# yaffle/lib/yaffle.rb\n# api_boost/lib/api_boost.rb\n\nrequire \"yaffle/version\"\nrequire \"yaffle/railtie\"\nrequire \"yaffle/core_ext\"\nrequire \"yaffle/acts_as_yaffle\"\nrequire \"api_boost/version\"\nrequire \"api_boost/railtie\"\nrequire \"api_boost/core_ext\"\nrequire \"api_boost/acts_as_api_resource\"\n\nmodule Yaffle\nmodule ApiBoost\n  # Your code goes here...\nend\n```\n\n```ruby\n# yaffle/lib/yaffle/acts_as_yaffle.rb\n# api_boost/lib/api_boost/acts_as_api_resource.rb\n\nmodule ApiBoost\n  module ActsAsApiResource\n    extend ActiveSupport::Concern\n\nmodule Yaffle\n  module ActsAsYaffle\n    class_methods do\n      def acts_as_api_resource(api_timestamp_field: :last_request_at)\n        # Create a class-level setting that stores which field to use for the API timestamp.\n        cattr_accessor :api_timestamp_field, default: api_timestamp_field.to_s\n      end\n    end\n  end\nend\n```\n\nThe code above uses `ActiveSupport::Concern` to simplify including modules with both class and instance methods. Methods in the `class_methods` block become class methods when the module is included. For more details, see the [ActiveSupport::Concern API documentation](https://api.rubyonrails.org/classes/ActiveSupport/Concern.html).\n\n### Add a Class Method\n\nThis plugin will expect that you've added a method to your model named `last_squawk`. However, the\nplugin users might have already defined a method on their model named `last_squawk` that they use\nfor something else. This plugin will allow the name to be changed by adding a class method called `yaffle_text_field`.\nBy default, this plugin expects your model to have a column named `last_request_at`. However, since that column name might already be used for something else, the plugin lets you customize it. You can override the default by passing a different column name with the `api_timestamp_field: option`. Internally, this value is stored in a class-level setting called `api_timestamp_field`, which the plugin uses when updating the timestamp.",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2154568767",
        "repo_full_name": "rails/rails",
        "pr_number": 55203,
        "pr_file": "guides/source/plugins.md",
        "discussion_id": "2154568767",
        "commented_code": "@@ -92,388 +190,465 @@ Extending Core Classes\n \n This section will explain how to add a method to String that will be available anywhere in your Rails application.\n \n-In this example you will add a method to String named `to_squawk`. To begin, create a new test file with a few assertions:\n+WARNING: Before proceeding, it's important to understand that extending core\n+classes (like String, Array, Hash, etc.) should be used sparingly, if at all.\n+Core class extensions can be brittle, dangerous, and are often\n+unnecessary.<br></br> They can:</br>\n+- Cause naming conflicts when multiple gems extend the same class with the same\n+  method name</br>\n+- Break unexpectedly when Ruby or Rails updates change core class behavior</br>\n+- Make debugging difficult because it's not obvious where methods come from</br>\n+- Create coupling issues between your plugin and other code<br></br> Better\n+alternatives to consider:</br>\n+- Create utility modules or helper classes instead</br>\n+- Use composition over monkey patching</br>\n+- Implement functionality as instance methods on your own classes<br></br> For\n+more details on why core class extensions can be problematic, see [The Case\n+Against Monkey\n+Patching](https://shopify.engineering/the-case-against-monkey-patching).\n+<br></br> That said, understanding how core class extensions work is valuable.\n+The example below demonstrates the technique, but they should be used sparingly\n+- consider whether it's the right approach for your specific use case.\n+\n+In this example you will add a method to Integer named `requests_per_hour`.\n+\n+In `lib/api_boost.rb`, add `require \"api_boost/core_ext\"`:\n \n ```ruby\n-# yaffle/test/core_ext_test.rb\n-\n-require \"test_helper\"\n-\n-class CoreExtTest < ActiveSupport::TestCase\n-  def test_to_squawk_prepends_the_word_squawk\n-    assert_equal \"squawk! Hello World\", \"Hello World\".to_squawk\n-  end\n-end\n-```\n-\n-Run `bin/test` to run the test. This test should fail because we haven't implemented the `to_squawk` method:\n-\n-```bash\n-$ bin/test\n-E\n-\n-Error:\n-CoreExtTest#test_to_squawk_prepends_the_word_squawk:\n-NoMethodError: undefined method `to_squawk' for \"Hello World\":String\n-\n+# api_boost/lib/api_boost.rb\n \n-bin/test /path/to/yaffle/test/core_ext_test.rb:4\n+require \"api_boost/version\"\n+require \"api_boost/railtie\"\n+require \"api_boost/core_ext\"\n \n-.\n-\n-Finished in 0.003358s, 595.6483 runs/s, 297.8242 assertions/s.\n-2 runs, 1 assertions, 0 failures, 1 errors, 0 skips\n-```\n-\n-Great - now you are ready to start development.\n-\n-In `lib/yaffle.rb`, add `require \"yaffle/core_ext\"`:\n-\n-```ruby\n-# yaffle/lib/yaffle.rb\n-\n-require \"yaffle/version\"\n-require \"yaffle/railtie\"\n-require \"yaffle/core_ext\"\n-\n-module Yaffle\n+module ApiBoost\n   # Your code goes here...\n end\n ```\n \n-Finally, create the `core_ext.rb` file and add the `to_squawk` method:\n+Create the `core_ext.rb` file and add a method to Integer to define a RateLimit that could define `10.requests_per_hour`, similar to `10.hours` that returns a Time.\n \n ```ruby\n-# yaffle/lib/yaffle/core_ext.rb\n+# api_boost/lib/api_boost/core_ext.rb\n \n-class String\n-  def to_squawk\n-    \"squawk! #{self}\".strip\n+ApiBoost::RateLimit = Data.define(:requests, :per)\n+\n+class Integer\n+  def requests_per_hour\n+    ApiBoost::RateLimit.new(self, :hour)\n   end\n end\n ```\n \n-To test that your method does what it says it does, run the unit tests with `bin/test` from your plugin directory.\n+To see this in action, change to the `test/dummy` directory, start `bin/rails console`, and test the API response formatting:\n \n ```bash\n-$ bin/test\n-...\n-2 runs, 2 assertions, 0 failures, 0 errors, 0 skips\n+$ cd test/dummy\n+$ bin/rails console\n ```\n \n-To see this in action, change to the `test/dummy` directory, start `bin/rails console`, and commence squawking:\n-\n ```irb\n-irb> \"Hello World\".to_squawk\n-=> \"squawk! Hello World\"\n+irb> 10.requests_per_hour\n+=> #<struct ApiBoost::RateLimit requests=10, per=:hour>\n ```\n \n+The dummy application automatically loads your plugin, so any extensions you add are immediately available for testing.\n+\n Add an \"acts_as\" Method to Active Record\n ----------------------------------------\n \n A common pattern in plugins is to add a method called `acts_as_something` to models. In this case, you\n-want to write a method called `acts_as_yaffle` that adds a `squawk` method to your Active Record models.\n+want to write a method called `acts_as_api_resource` that adds API-specific functionality to your Active Record models.\n \n-To begin, set up your files so that you have:\n+Let\u2019s say you\u2019re building an API and you want to keep track of the last time a resource (like a `Product`) was accessed via that API. You might want to use that timestamp to:\n \n-```ruby\n-# yaffle/test/acts_as_yaffle_test.rb\n+* throttle requests\n+* show \u201clast active\u201d times in your admin panel\n+* prioritize stale records for syncing\n \n-require \"test_helper\"\n+Instead of writing this logic in every model, you can use a shared plugin. The `acts_as_api_resource` method adds this functionality to any model, letting you track API activity by updating a timestamp field.\n \n-class ActsAsYaffleTest < ActiveSupport::TestCase\n-end\n-```\n+To begin, set up your files so that you have:\n \n ```ruby\n-# yaffle/lib/yaffle.rb\n+# api_boost/lib/api_boost.rb\n \n-require \"yaffle/version\"\n-require \"yaffle/railtie\"\n-require \"yaffle/core_ext\"\n-require \"yaffle/acts_as_yaffle\"\n+require \"api_boost/version\"\n+require \"api_boost/railtie\"\n+require \"api_boost/core_ext\"\n+require \"api_boost/acts_as_api_resource\"\n \n-module Yaffle\n+module ApiBoost\n   # Your code goes here...\n end\n ```\n \n ```ruby\n-# yaffle/lib/yaffle/acts_as_yaffle.rb\n+# api_boost/lib/api_boost/acts_as_api_resource.rb\n+\n+module ApiBoost\n+  module ActsAsApiResource\n+    extend ActiveSupport::Concern\n \n-module Yaffle\n-  module ActsAsYaffle\n+    class_methods do\n+      def acts_as_api_resource(api_timestamp_field: :last_request_at)\n+        # Create a class-level setting that stores which field to use for the API timestamp.\n+        cattr_accessor :api_timestamp_field, default: api_timestamp_field.to_s\n+      end\n+    end\n   end\n end\n ```\n \n+The code above uses `ActiveSupport::Concern` to simplify including modules with both class and instance methods. Methods in the `class_methods` block become class methods when the module is included. For more details, see the [ActiveSupport::Concern API documentation](https://api.rubyonrails.org/classes/ActiveSupport/Concern.html).\n+\n ### Add a Class Method\n \n-This plugin will expect that you've added a method to your model named `last_squawk`. However, the\n-plugin users might have already defined a method on their model named `last_squawk` that they use\n-for something else. This plugin will allow the name to be changed by adding a class method called `yaffle_text_field`.\n+By default, this plugin expects your model to have a column named `last_request_at`. However, since that column name might already be used for something else, the plugin lets you customize it. You can override the default by passing a different column name with the `api_timestamp_field: option`. Internally, this value is stored in a class-level setting called `api_timestamp_field`, which the plugin uses when updating the timestamp.",
        "comment_created_at": "2025-06-18T13:12:04+00:00",
        "comment_author": "alexcameron89",
        "comment_body": "```suggestion\nBy default, this plugin expects your model to have a column named `last_request_at`. However, since that column name might already be used for something else, the plugin lets you customize it. You can override the default by passing a different column name with the `api_timestamp_field:` option. Internally, this value is stored in a class-level setting called `api_timestamp_field`, which the plugin uses when updating the timestamp.\n```\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1602152720",
    "pr_number": 51814,
    "pr_file": "guides/source/active_storage_overview.md",
    "created_at": "2024-05-15T19:34:20+00:00",
    "commented_code": "NOTE: Since Active Storage relies on polymorphic associations, and [polymorphic associations](./association_basics.html#polymorphic-associations) rely on storing class names in the database, that data must remain synchronized with the class name used by the Ruby code. When renaming classes that use `has_many_attached`, make sure to also update the class names in the `active_storage_attachments.record_type` polymorphic type column of the corresponding rows.\n\n### Callbacks\n\nActive Storage provides callbacks for when attachments are successfully uploaded to the configured service.\n**Before** and **After** callbacks are available on both `has_one_attached` and `has_many_attached` associations.\nThe method name will include the attachment name and the callback type.\n_For variants, the suffix `_variant_attached` will be used._\n\n```ruby\nclass Message < ApplicationRecord\n  has_one_attached :image do |attachable|\n    attachable.variant :thumb, resize_to_limit: [100, 100]\n  end\n\n  has_many_attached :images do |attachable|\n    attachable.variant :thumb, resize_to_limit: [100, 100]\n  end\n\n  def before_image_attached(image_blob)",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1602152720",
        "repo_full_name": "rails/rails",
        "pr_number": 51814,
        "pr_file": "guides/source/active_storage_overview.md",
        "discussion_id": "1602152720",
        "commented_code": "@@ -553,6 +553,41 @@ end\n \n NOTE: Since Active Storage relies on polymorphic associations, and [polymorphic associations](./association_basics.html#polymorphic-associations) rely on storing class names in the database, that data must remain synchronized with the class name used by the Ruby code. When renaming classes that use `has_many_attached`, make sure to also update the class names in the `active_storage_attachments.record_type` polymorphic type column of the corresponding rows.\n \n+### Callbacks\n+\n+Active Storage provides callbacks for when attachments are successfully uploaded to the configured service.\n+**Before** and **After** callbacks are available on both `has_one_attached` and `has_many_attached` associations.\n+The method name will include the attachment name and the callback type.\n+_For variants, the suffix `_variant_attached` will be used._\n+\n+```ruby\n+class Message < ApplicationRecord\n+  has_one_attached :image do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  has_many_attached :images do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  def before_image_attached(image_blob)",
        "comment_created_at": "2024-05-15T19:34:20+00:00",
        "comment_author": "MatheusRich",
        "comment_body": "IMHO this feels different from normal AR callbacks. Usually we'd have something like\r\n\r\n```rb\r\nclass Message < ApplicationRecord\r\n  has_one_attached :image do |attachable|\r\n    attachable.variant :thumb, resize_to_limit: [100, 100]\r\n  end\r\n\r\n  before_image_attached do |image_blob|\r\n    # do stuff\r\n  end\r\nend\r\n```\r\n\r\nMinor change, but it feels more similar to what we already have with Active Record callbacks. Thoughts?",
        "pr_file_module": null
      },
      {
        "comment_id": "1602201440",
        "repo_full_name": "rails/rails",
        "pr_number": 51814,
        "pr_file": "guides/source/active_storage_overview.md",
        "discussion_id": "1602152720",
        "commented_code": "@@ -553,6 +553,41 @@ end\n \n NOTE: Since Active Storage relies on polymorphic associations, and [polymorphic associations](./association_basics.html#polymorphic-associations) rely on storing class names in the database, that data must remain synchronized with the class name used by the Ruby code. When renaming classes that use `has_many_attached`, make sure to also update the class names in the `active_storage_attachments.record_type` polymorphic type column of the corresponding rows.\n \n+### Callbacks\n+\n+Active Storage provides callbacks for when attachments are successfully uploaded to the configured service.\n+**Before** and **After** callbacks are available on both `has_one_attached` and `has_many_attached` associations.\n+The method name will include the attachment name and the callback type.\n+_For variants, the suffix `_variant_attached` will be used._\n+\n+```ruby\n+class Message < ApplicationRecord\n+  has_one_attached :image do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  has_many_attached :images do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  def before_image_attached(image_blob)",
        "comment_created_at": "2024-05-15T20:23:12+00:00",
        "comment_author": "rapito",
        "comment_body": "> IMHO this feels different from normal AR callbacks. Usually we'd have something like\r\n> \r\n> ```ruby\r\n> class Message < ApplicationRecord\r\n>   has_one_attached :image do |attachable|\r\n>     attachable.variant :thumb, resize_to_limit: [100, 100]\r\n>   end\r\n> \r\n>   before_image_attached do |image_blob|\r\n>     # do stuff\r\n>   end\r\n> end\r\n> ```\r\n> \r\n> Minor change, but it feels more similar to what we already have with Active Record callbacks. Thoughts?\r\n\r\nThanks @MatheusRich, for sure! I completely agree with you. And this was the original intent. \r\nActually that was the first iteration, the problem however was that ar callbacks would not allow us to yield parameters back to it. \r\n\r\nWe would have to add that ability to ar callbacks from the ground up and in the end we decided against it and follow this simpler approach.",
        "pr_file_module": null
      },
      {
        "comment_id": "1605710987",
        "repo_full_name": "rails/rails",
        "pr_number": 51814,
        "pr_file": "guides/source/active_storage_overview.md",
        "discussion_id": "1602152720",
        "commented_code": "@@ -553,6 +553,41 @@ end\n \n NOTE: Since Active Storage relies on polymorphic associations, and [polymorphic associations](./association_basics.html#polymorphic-associations) rely on storing class names in the database, that data must remain synchronized with the class name used by the Ruby code. When renaming classes that use `has_many_attached`, make sure to also update the class names in the `active_storage_attachments.record_type` polymorphic type column of the corresponding rows.\n \n+### Callbacks\n+\n+Active Storage provides callbacks for when attachments are successfully uploaded to the configured service.\n+**Before** and **After** callbacks are available on both `has_one_attached` and `has_many_attached` associations.\n+The method name will include the attachment name and the callback type.\n+_For variants, the suffix `_variant_attached` will be used._\n+\n+```ruby\n+class Message < ApplicationRecord\n+  has_one_attached :image do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  has_many_attached :images do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  def before_image_attached(image_blob)",
        "comment_created_at": "2024-05-18T08:41:23+00:00",
        "comment_author": "zzak",
        "comment_body": "This isn't a fully baked thought, but what about something like:\r\n\r\n```\r\nbefore_image_attached :do_stuff\r\n\r\ndef do_stuff(blob)\r\n  # do stuff with blob\r\nend\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1605793003",
        "repo_full_name": "rails/rails",
        "pr_number": 51814,
        "pr_file": "guides/source/active_storage_overview.md",
        "discussion_id": "1602152720",
        "commented_code": "@@ -553,6 +553,41 @@ end\n \n NOTE: Since Active Storage relies on polymorphic associations, and [polymorphic associations](./association_basics.html#polymorphic-associations) rely on storing class names in the database, that data must remain synchronized with the class name used by the Ruby code. When renaming classes that use `has_many_attached`, make sure to also update the class names in the `active_storage_attachments.record_type` polymorphic type column of the corresponding rows.\n \n+### Callbacks\n+\n+Active Storage provides callbacks for when attachments are successfully uploaded to the configured service.\n+**Before** and **After** callbacks are available on both `has_one_attached` and `has_many_attached` associations.\n+The method name will include the attachment name and the callback type.\n+_For variants, the suffix `_variant_attached` will be used._\n+\n+```ruby\n+class Message < ApplicationRecord\n+  has_one_attached :image do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  has_many_attached :images do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  def before_image_attached(image_blob)",
        "comment_created_at": "2024-05-18T13:48:30+00:00",
        "comment_author": "rapito",
        "comment_body": "> This isn't a fully baked thought, but what about something like:\r\n> \r\n> ```\r\n> before_image_attached :do_stuff\r\n> \r\n> def do_stuff(blob)\r\n>   # do stuff with blob\r\n> end\r\n> ```\r\n\r\nHi! That is the same proposition on the first comment, please read my [answer to it above](https://github.com/rails/rails/pull/51814#discussion_r1602201440).",
        "pr_file_module": null
      },
      {
        "comment_id": "1606076609",
        "repo_full_name": "rails/rails",
        "pr_number": 51814,
        "pr_file": "guides/source/active_storage_overview.md",
        "discussion_id": "1602152720",
        "commented_code": "@@ -553,6 +553,41 @@ end\n \n NOTE: Since Active Storage relies on polymorphic associations, and [polymorphic associations](./association_basics.html#polymorphic-associations) rely on storing class names in the database, that data must remain synchronized with the class name used by the Ruby code. When renaming classes that use `has_many_attached`, make sure to also update the class names in the `active_storage_attachments.record_type` polymorphic type column of the corresponding rows.\n \n+### Callbacks\n+\n+Active Storage provides callbacks for when attachments are successfully uploaded to the configured service.\n+**Before** and **After** callbacks are available on both `has_one_attached` and `has_many_attached` associations.\n+The method name will include the attachment name and the callback type.\n+_For variants, the suffix `_variant_attached` will be used._\n+\n+```ruby\n+class Message < ApplicationRecord\n+  has_one_attached :image do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  has_many_attached :images do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  def before_image_attached(image_blob)",
        "comment_created_at": "2024-05-19T17:55:29+00:00",
        "comment_author": "mattboldt",
        "comment_body": "Great work here! Echoing Robert's earlier message: normal AM callbacks don't allow us to pass an argument. My assumption is that AM callbacks expect to be idempotent, and that all information is available on `self`. However, if you `has_many_attached`, and you want to do some processing on the specific image that was just attached, that info is harder to get on `self` alone. You could query the most recently added attachment, but that could cause race conditions.\r\n\r\nI wonder if it would help prevent confusion by differentiating it from the usual ActiveModel Callback pattern. Something like...\r\n\r\n```rb\r\nclass Message < ApplicationRecord\r\n  # with a lambda\r\n  has_one_attached :image, after_attached: ->(blob) { puts \"image attached\" } do |attachable|\r\n    attachable.variant :thumb, resize_to_limit: [100, 100]\r\n  end\r\n\r\n  # OR, with a method name\r\n  has_one_attached :image, after_attached: :example_after_attached do |attachable|\r\n    attachable.variant :thumb, resize_to_limit: [100, 100]\r\n  end\r\n\r\n  def example_after_attached(blob)\r\n  end\r\nend\r\n```\r\n\r\nNow it's more like a part of `has_one_attached`'s API rather than trying to mimic the ActiveModel Callback API. You could still send an argument to it like you have here so you get all the same functionality, and the user gets to customize the method name (or use a lambda).\r\n\r\n_However_, if folks aren't concerned about this, I think your solution looks good as-is. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1607222342",
        "repo_full_name": "rails/rails",
        "pr_number": 51814,
        "pr_file": "guides/source/active_storage_overview.md",
        "discussion_id": "1602152720",
        "commented_code": "@@ -553,6 +553,41 @@ end\n \n NOTE: Since Active Storage relies on polymorphic associations, and [polymorphic associations](./association_basics.html#polymorphic-associations) rely on storing class names in the database, that data must remain synchronized with the class name used by the Ruby code. When renaming classes that use `has_many_attached`, make sure to also update the class names in the `active_storage_attachments.record_type` polymorphic type column of the corresponding rows.\n \n+### Callbacks\n+\n+Active Storage provides callbacks for when attachments are successfully uploaded to the configured service.\n+**Before** and **After** callbacks are available on both `has_one_attached` and `has_many_attached` associations.\n+The method name will include the attachment name and the callback type.\n+_For variants, the suffix `_variant_attached` will be used._\n+\n+```ruby\n+class Message < ApplicationRecord\n+  has_one_attached :image do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  has_many_attached :images do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  def before_image_attached(image_blob)",
        "comment_created_at": "2024-05-20T20:09:04+00:00",
        "comment_author": "rapito",
        "comment_body": "I actually love your suggestion Matt, it makes a lot of sense to me and feels more explicit (and makes the behavior more readable and deterministic). \r\n\r\nI don't have a strong opinion about leaving it as-is or using the new approach. I'm fine with whichever. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1612660732",
        "repo_full_name": "rails/rails",
        "pr_number": 51814,
        "pr_file": "guides/source/active_storage_overview.md",
        "discussion_id": "1602152720",
        "commented_code": "@@ -553,6 +553,41 @@ end\n \n NOTE: Since Active Storage relies on polymorphic associations, and [polymorphic associations](./association_basics.html#polymorphic-associations) rely on storing class names in the database, that data must remain synchronized with the class name used by the Ruby code. When renaming classes that use `has_many_attached`, make sure to also update the class names in the `active_storage_attachments.record_type` polymorphic type column of the corresponding rows.\n \n+### Callbacks\n+\n+Active Storage provides callbacks for when attachments are successfully uploaded to the configured service.\n+**Before** and **After** callbacks are available on both `has_one_attached` and `has_many_attached` associations.\n+The method name will include the attachment name and the callback type.\n+_For variants, the suffix `_variant_attached` will be used._\n+\n+```ruby\n+class Message < ApplicationRecord\n+  has_one_attached :image do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  has_many_attached :images do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  def before_image_attached(image_blob)",
        "comment_created_at": "2024-05-24T03:21:12+00:00",
        "comment_author": "natematykiewicz",
        "comment_body": "That last suggestion feels a lot more like normal ActiveRecord. I like the flexibility of it compared to a magically named method that you have to constantly do `respond_to?` checks for.\r\n\r\nOne suggestion I was thinking that might be a little more ergonomic than a hash argument in a method that also expects a block, is to add 2 methods to [ActiveStorage::Reflection::HasAttachedReflection](https://github.com/rails/rails/blob/21bbf5aeef607298fbc0f6bc88ef862c452d62d7/activestorage/lib/active_storage/reflection.rb).\r\n\r\n```ruby\r\nclass Message < ApplicationRecord\r\n  # with a lambda\r\n  has_one_attached :image do |attachable|\r\n    attachable.variant :thumb, resize_to_limit: [100, 100]\r\n\r\n    attachable.after_attached do |blob|\r\n      puts \"image attached\"\r\n    end\r\n  end\r\n\r\n  # OR, with a method name\r\n  has_one_attached :image do |attachable|\r\n    attachable.variant :thumb, resize_to_limit: [100, 100]\r\n\r\n    attachable.before_attached :example_before_attached\r\n  end\r\n\r\n  def example_before_attached(blob)\r\n  end\r\nend\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1612662138",
        "repo_full_name": "rails/rails",
        "pr_number": 51814,
        "pr_file": "guides/source/active_storage_overview.md",
        "discussion_id": "1602152720",
        "commented_code": "@@ -553,6 +553,41 @@ end\n \n NOTE: Since Active Storage relies on polymorphic associations, and [polymorphic associations](./association_basics.html#polymorphic-associations) rely on storing class names in the database, that data must remain synchronized with the class name used by the Ruby code. When renaming classes that use `has_many_attached`, make sure to also update the class names in the `active_storage_attachments.record_type` polymorphic type column of the corresponding rows.\n \n+### Callbacks\n+\n+Active Storage provides callbacks for when attachments are successfully uploaded to the configured service.\n+**Before** and **After** callbacks are available on both `has_one_attached` and `has_many_attached` associations.\n+The method name will include the attachment name and the callback type.\n+_For variants, the suffix `_variant_attached` will be used._\n+\n+```ruby\n+class Message < ApplicationRecord\n+  has_one_attached :image do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  has_many_attached :images do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  def before_image_attached(image_blob)",
        "comment_created_at": "2024-05-24T03:24:29+00:00",
        "comment_author": "natematykiewicz",
        "comment_body": "It'd also be more performant to have to actually specify at the time of defining the `has_one_attached` that there are callbacks, than to always attempt to run callbacks only to find that none are defined.",
        "pr_file_module": null
      },
      {
        "comment_id": "1744781703",
        "repo_full_name": "rails/rails",
        "pr_number": 51814,
        "pr_file": "guides/source/active_storage_overview.md",
        "discussion_id": "1602152720",
        "commented_code": "@@ -553,6 +553,41 @@ end\n \n NOTE: Since Active Storage relies on polymorphic associations, and [polymorphic associations](./association_basics.html#polymorphic-associations) rely on storing class names in the database, that data must remain synchronized with the class name used by the Ruby code. When renaming classes that use `has_many_attached`, make sure to also update the class names in the `active_storage_attachments.record_type` polymorphic type column of the corresponding rows.\n \n+### Callbacks\n+\n+Active Storage provides callbacks for when attachments are successfully uploaded to the configured service.\n+**Before** and **After** callbacks are available on both `has_one_attached` and `has_many_attached` associations.\n+The method name will include the attachment name and the callback type.\n+_For variants, the suffix `_variant_attached` will be used._\n+\n+```ruby\n+class Message < ApplicationRecord\n+  has_one_attached :image do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  has_many_attached :images do |attachable|\n+    attachable.variant :thumb, resize_to_limit: [100, 100]\n+  end\n+\n+  def before_image_attached(image_blob)",
        "comment_created_at": "2024-09-05T04:23:14+00:00",
        "comment_author": "rapito",
        "comment_body": "I went ahead with @mattboldt 's suggestion and made it as named options that support both lambdas and symbols. \r\nNow it actually looks more _rails-y_  and is more performant. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2119731986",
    "pr_number": 55137,
    "pr_file": "guides/source/plugins.md",
    "created_at": "2025-06-01T23:44:34+00:00",
    "commented_code": "This section will explain how to add a method to String that will be available anywhere in your Rails application.\n\nIn this example you will add a method to String named `to_squawk`. To begin, create a new test file with a few assertions:\nWARNING: Before proceeding, it's important to understand that extending core\nclasses (like String, Array, Hash, etc.) should be used sparingly, if at all.\nCore class extensions can be brittle, dangerous, and are often\nunnecessary.<br></br> They can:</br>\n- Cause naming conflicts when multiple gems extend the same class with the same\n  method name</br>\n- Break unexpectedly when Ruby or Rails updates change core class behavior</br>\n- Make debugging difficult because it's not obvious where methods come from</br>\n- Create coupling issues between your plugin and other code<br></br> Better\nalternatives to consider:</br>\n- Create utility modules or helper classes instead</br>\n- Use composition over monkey patching</br>\n- Implement functionality as instance methods on your own classes<br></br> For\nmore details on why core class extensions can be problematic, see [The Case\nAgainst Monkey\nPatching](https://shopify.engineering/the-case-against-monkey-patching).\n<br></br> That said, understanding how core class extensions work is valuable.\nThe example below demonstrates the technique, but they should be used sparingly\n- consider whether it's the right approach for your specific use case.\n\n\nIn this example you will add a method to String named `to_throttled_response`.\n\nIn `lib/api_boost.rb`, add `require \"api_boost/core_ext\"`:\n\n```ruby\n# yaffle/test/core_ext_test.rb\n# api_boost/lib/api_boost.rb\n\nrequire \"test_helper\"\nrequire \"api_boost/version\"\nrequire \"api_boost/railtie\"\nrequire \"api_boost/core_ext\"\n\nclass CoreExtTest < ActiveSupport::TestCase\n  def test_to_squawk_prepends_the_word_squawk\n    assert_equal \"squawk! Hello World\", \"Hello World\".to_squawk\n  end\nmodule ApiBoost\n  # Your code goes here...\nend\n```\n\nRun `bin/test` to run the test. This test should fail because we haven't implemented the `to_squawk` method:\nCreate the `core_ext.rb` file and add the `to_throttled_response` method:\n\n```bash\n$ bin/test\nE\n```ruby\n# api_boost/lib/api_boost/core_ext.rb\n\nError:\nCoreExtTest#test_to_squawk_prepends_the_word_squawk:\nNoMethodError: undefined method `to_squawk' for \"Hello World\":String\nclass String\n  def to_throttled_response(limit = \"60 requests per hour\")\n    {\n      data: self,\n      rate_limit: limit\n    }\n  end\nend\n```\n\nTo see this in action, change to the `test/dummy` directory, start `bin/rails console`, and test the API response formatting:\n\nbin/test /path/to/yaffle/test/core_ext_test.rb:4\n```irb\n$ cd test/dummy\n$ bin/rails console\n\n.\nirb> \"Hello API\".to_throttled_response\n=> {:data=>\"Hello API\", :rate_limit=>\"60 requests per hour\"}\n\nFinished in 0.003358s, 595.6483 runs/s, 297.8242 assertions/s.\n2 runs, 1 assertions, 0 failures, 1 errors, 0 skips\nirb> \"User data\".to_throttled_response(\"100 requests per hour\")\n=> {:data=>\"User data\", :rate_limit=>\"100 requests per hour\"}\n```\n\nGreat - now you are ready to start development.\nThe dummy application automatically loads your plugin, so any extensions you add are immediately available for testing.\n\nAdd an \"acts_as\" Method to Active Record\n----------------------------------------\n\nIn `lib/yaffle.rb`, add `require \"yaffle/core_ext\"`:\nA common pattern in plugins is to add a method called `acts_as_something` to models. In this case, you\nwant to write a method called `acts_as_api_resource` that adds API-specific functionality to your Active Record models.\n\nTo begin, set up your files so that you have:\n\n```ruby\n# yaffle/lib/yaffle.rb\n# api_boost/lib/api_boost.rb\n\nrequire \"yaffle/version\"\nrequire \"yaffle/railtie\"\nrequire \"yaffle/core_ext\"\nrequire \"api_boost/version\"\nrequire \"api_boost/railtie\"\nrequire \"api_boost/core_ext\"\nrequire \"api_boost/acts_as_api_resource\"\n\nmodule Yaffle\nmodule ApiBoost\n  # Your code goes here...\nend\n```\n\nFinally, create the `core_ext.rb` file and add the `to_squawk` method:\n\n```ruby\n# yaffle/lib/yaffle/core_ext.rb\n# api_boost/lib/api_boost/acts_as_api_resource.rb\n\nclass String\n  def to_squawk\n    \"squawk! #{self}\".strip\nmodule ApiBoost\n  module ActsAsApiResource\n    extend ActiveSupport::Concern\n\n    class_methods do\n      def acts_as_api_resource(options = {})\n        cattr_accessor :api_timestamp_field, default: (options[:api_timestamp_field] || :last_request_at).to_s\n      end\n    end\n  end\nend\n```\n\nTo test that your method does what it says it does, run the unit tests with `bin/test` from your plugin directory.\nThe code above uses `ActiveSupport::Concern` to simplify including modules with both class and instance methods. Methods in the `class_methods` block become class methods when the module is included. For more details, see the [ActiveSupport::Concern API documentation](https://api.rubyonrails.org/classes/ActiveSupport/Concern.html).\n\n```bash\n$ bin/test\n...\n2 runs, 2 assertions, 0 failures, 0 errors, 0 skips\n```\n### Add a Class Method\n\nTo see this in action, change to the `test/dummy` directory, start `bin/rails console`, and commence squawking:\nThis plugin will expect that you've added a method to your model named `last_request_at`. However, the\nplugin users might have already defined a method on their model named `last_request_at` that they use\nfor something else. This plugin will allow the name to be changed by adding a class method called `api_timestamp_field`.",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2119731986",
        "repo_full_name": "rails/rails",
        "pr_number": 55137,
        "pr_file": "guides/source/plugins.md",
        "discussion_id": "2119731986",
        "commented_code": "@@ -92,388 +179,477 @@ Extending Core Classes\n \n This section will explain how to add a method to String that will be available anywhere in your Rails application.\n \n-In this example you will add a method to String named `to_squawk`. To begin, create a new test file with a few assertions:\n+WARNING: Before proceeding, it's important to understand that extending core\n+classes (like String, Array, Hash, etc.) should be used sparingly, if at all.\n+Core class extensions can be brittle, dangerous, and are often\n+unnecessary.<br></br> They can:</br>\n+- Cause naming conflicts when multiple gems extend the same class with the same\n+  method name</br>\n+- Break unexpectedly when Ruby or Rails updates change core class behavior</br>\n+- Make debugging difficult because it's not obvious where methods come from</br>\n+- Create coupling issues between your plugin and other code<br></br> Better\n+alternatives to consider:</br>\n+- Create utility modules or helper classes instead</br>\n+- Use composition over monkey patching</br>\n+- Implement functionality as instance methods on your own classes<br></br> For\n+more details on why core class extensions can be problematic, see [The Case\n+Against Monkey\n+Patching](https://shopify.engineering/the-case-against-monkey-patching).\n+<br></br> That said, understanding how core class extensions work is valuable.\n+The example below demonstrates the technique, but they should be used sparingly\n+- consider whether it's the right approach for your specific use case.\n+\n+\n+In this example you will add a method to String named `to_throttled_response`.\n+\n+In `lib/api_boost.rb`, add `require \"api_boost/core_ext\"`:\n \n ```ruby\n-# yaffle/test/core_ext_test.rb\n+# api_boost/lib/api_boost.rb\n \n-require \"test_helper\"\n+require \"api_boost/version\"\n+require \"api_boost/railtie\"\n+require \"api_boost/core_ext\"\n \n-class CoreExtTest < ActiveSupport::TestCase\n-  def test_to_squawk_prepends_the_word_squawk\n-    assert_equal \"squawk! Hello World\", \"Hello World\".to_squawk\n-  end\n+module ApiBoost\n+  # Your code goes here...\n end\n ```\n \n-Run `bin/test` to run the test. This test should fail because we haven't implemented the `to_squawk` method:\n+Create the `core_ext.rb` file and add the `to_throttled_response` method:\n \n-```bash\n-$ bin/test\n-E\n+```ruby\n+# api_boost/lib/api_boost/core_ext.rb\n \n-Error:\n-CoreExtTest#test_to_squawk_prepends_the_word_squawk:\n-NoMethodError: undefined method `to_squawk' for \"Hello World\":String\n+class String\n+  def to_throttled_response(limit = \"60 requests per hour\")\n+    {\n+      data: self,\n+      rate_limit: limit\n+    }\n+  end\n+end\n+```\n \n+To see this in action, change to the `test/dummy` directory, start `bin/rails console`, and test the API response formatting:\n \n-bin/test /path/to/yaffle/test/core_ext_test.rb:4\n+```irb\n+$ cd test/dummy\n+$ bin/rails console\n \n-.\n+irb> \"Hello API\".to_throttled_response\n+=> {:data=>\"Hello API\", :rate_limit=>\"60 requests per hour\"}\n \n-Finished in 0.003358s, 595.6483 runs/s, 297.8242 assertions/s.\n-2 runs, 1 assertions, 0 failures, 1 errors, 0 skips\n+irb> \"User data\".to_throttled_response(\"100 requests per hour\")\n+=> {:data=>\"User data\", :rate_limit=>\"100 requests per hour\"}\n ```\n \n-Great - now you are ready to start development.\n+The dummy application automatically loads your plugin, so any extensions you add are immediately available for testing.\n+\n+Add an \"acts_as\" Method to Active Record\n+----------------------------------------\n \n-In `lib/yaffle.rb`, add `require \"yaffle/core_ext\"`:\n+A common pattern in plugins is to add a method called `acts_as_something` to models. In this case, you\n+want to write a method called `acts_as_api_resource` that adds API-specific functionality to your Active Record models.\n+\n+To begin, set up your files so that you have:\n \n ```ruby\n-# yaffle/lib/yaffle.rb\n+# api_boost/lib/api_boost.rb\n \n-require \"yaffle/version\"\n-require \"yaffle/railtie\"\n-require \"yaffle/core_ext\"\n+require \"api_boost/version\"\n+require \"api_boost/railtie\"\n+require \"api_boost/core_ext\"\n+require \"api_boost/acts_as_api_resource\"\n \n-module Yaffle\n+module ApiBoost\n   # Your code goes here...\n end\n ```\n \n-Finally, create the `core_ext.rb` file and add the `to_squawk` method:\n-\n ```ruby\n-# yaffle/lib/yaffle/core_ext.rb\n+# api_boost/lib/api_boost/acts_as_api_resource.rb\n \n-class String\n-  def to_squawk\n-    \"squawk! #{self}\".strip\n+module ApiBoost\n+  module ActsAsApiResource\n+    extend ActiveSupport::Concern\n+\n+    class_methods do\n+      def acts_as_api_resource(options = {})\n+        cattr_accessor :api_timestamp_field, default: (options[:api_timestamp_field] || :last_request_at).to_s\n+      end\n+    end\n   end\n end\n ```\n \n-To test that your method does what it says it does, run the unit tests with `bin/test` from your plugin directory.\n+The code above uses `ActiveSupport::Concern` to simplify including modules with both class and instance methods. Methods in the `class_methods` block become class methods when the module is included. For more details, see the [ActiveSupport::Concern API documentation](https://api.rubyonrails.org/classes/ActiveSupport/Concern.html).\n \n-```bash\n-$ bin/test\n-...\n-2 runs, 2 assertions, 0 failures, 0 errors, 0 skips\n-```\n+### Add a Class Method\n \n-To see this in action, change to the `test/dummy` directory, start `bin/rails console`, and commence squawking:\n+This plugin will expect that you've added a method to your model named `last_request_at`. However, the\n+plugin users might have already defined a method on their model named `last_request_at` that they use\n+for something else. This plugin will allow the name to be changed by adding a class method called `api_timestamp_field`.",
        "comment_created_at": "2025-06-01T23:44:34+00:00",
        "comment_author": "irishbryan",
        "comment_body": "> This plugin will allow the name to be changed by adding a class method called `api_timestamp_field`\r\n\r\nMight be nice to include example of this.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2098857540",
    "pr_number": 55090,
    "pr_file": "guides/source/active_record_querying.md",
    "created_at": "2025-05-20T20:53:14+00:00",
    "commented_code": "irb> assoc.unscope(:includes).pluck(:id)\n```\n\nNOTE: Be aware that `pluck` ignores any previous `select` clauses:\n\n```irb\nirb> Customer.select(:email).pluck(:id)\nSELECT \"customers\".\"id\" FROM customers\n```\n\nIf you need to use raw SQL, this is how you can do it:\n\n```irb\nirb> Customer.pluck(Aler.sql(\"DISTINCT id\"))\nSELECT DISTINCT id FROM customers\n```",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2098857540",
        "repo_full_name": "rails/rails",
        "pr_number": 55090,
        "pr_file": "guides/source/active_record_querying.md",
        "discussion_id": "2098857540",
        "commented_code": "@@ -2408,6 +2408,20 @@ One way to avoid this is to `unscope` the includes:\n irb> assoc.unscope(:includes).pluck(:id)\n ```\n \n+NOTE: Be aware that `pluck` ignores any previous `select` clauses:\n+\n+```irb\n+irb> Customer.select(:email).pluck(:id)\n+SELECT \"customers\".\"id\" FROM customers\n+```\n+\n+If you need to use raw SQL, this is how you can do it:\n+\n+```irb\n+irb> Customer.pluck(Aler.sql(\"DISTINCT id\"))\n+SELECT DISTINCT id FROM customers\n+```\n+",
        "comment_created_at": "2025-05-20T20:53:14+00:00",
        "comment_author": "skipkayhil",
        "comment_body": "One of the examples in the [API docs for pluck](https://api.rubyonrails.org/classes/ActiveRecord/Calculations.html#method-i-pluck) already demonstrates using `Arel.sql`. Sinces the guides are more of an entrypoint than the API docs, I'm thinking we may want to only document simpler cases in the guide and leave more complex cases in the API docs.",
        "pr_file_module": null
      },
      {
        "comment_id": "2098867591",
        "repo_full_name": "rails/rails",
        "pr_number": 55090,
        "pr_file": "guides/source/active_record_querying.md",
        "discussion_id": "2098857540",
        "commented_code": "@@ -2408,6 +2408,20 @@ One way to avoid this is to `unscope` the includes:\n irb> assoc.unscope(:includes).pluck(:id)\n ```\n \n+NOTE: Be aware that `pluck` ignores any previous `select` clauses:\n+\n+```irb\n+irb> Customer.select(:email).pluck(:id)\n+SELECT \"customers\".\"id\" FROM customers\n+```\n+\n+If you need to use raw SQL, this is how you can do it:\n+\n+```irb\n+irb> Customer.pluck(Aler.sql(\"DISTINCT id\"))\n+SELECT DISTINCT id FROM customers\n+```\n+",
        "comment_created_at": "2025-05-20T20:59:52+00:00",
        "comment_author": "daffo",
        "comment_body": "gotcha\r\n\r\ndo you think is worth having the note/warning directly in the API docs rather than here in the guide?\r\njust above the Arel.sql example perhaps? or below, under all the examples section?",
        "pr_file_module": null
      },
      {
        "comment_id": "2098880331",
        "repo_full_name": "rails/rails",
        "pr_number": 55090,
        "pr_file": "guides/source/active_record_querying.md",
        "discussion_id": "2098857540",
        "commented_code": "@@ -2408,6 +2408,20 @@ One way to avoid this is to `unscope` the includes:\n irb> assoc.unscope(:includes).pluck(:id)\n ```\n \n+NOTE: Be aware that `pluck` ignores any previous `select` clauses:\n+\n+```irb\n+irb> Customer.select(:email).pluck(:id)\n+SELECT \"customers\".\"id\" FROM customers\n+```\n+\n+If you need to use raw SQL, this is how you can do it:\n+\n+```irb\n+irb> Customer.pluck(Aler.sql(\"DISTINCT id\"))\n+SELECT DISTINCT id FROM customers\n+```\n+",
        "comment_created_at": "2025-05-20T21:09:31+00:00",
        "comment_author": "skipkayhil",
        "comment_body": "I think my opinion would be yes, even the `select(:column).pluck(:another)` edge case probably is more suited for API docs",
        "pr_file_module": null
      },
      {
        "comment_id": "2098904952",
        "repo_full_name": "rails/rails",
        "pr_number": 55090,
        "pr_file": "guides/source/active_record_querying.md",
        "discussion_id": "2098857540",
        "commented_code": "@@ -2408,6 +2408,20 @@ One way to avoid this is to `unscope` the includes:\n irb> assoc.unscope(:includes).pluck(:id)\n ```\n \n+NOTE: Be aware that `pluck` ignores any previous `select` clauses:\n+\n+```irb\n+irb> Customer.select(:email).pluck(:id)\n+SELECT \"customers\".\"id\" FROM customers\n+```\n+\n+If you need to use raw SQL, this is how you can do it:\n+\n+```irb\n+irb> Customer.pluck(Aler.sql(\"DISTINCT id\"))\n+SELECT DISTINCT id FROM customers\n+```\n+",
        "comment_created_at": "2025-05-20T21:27:33+00:00",
        "comment_author": "daffo",
        "comment_body": "https://github.com/rails/rails/pull/55090/commits/c9a2a70b4e14ebc73355dd45a2e65fb43246d092",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1915597213",
    "pr_number": 54198,
    "pr_file": "guides/source/getting_started.md",
    "created_at": "2025-01-14T21:04:58+00:00",
    "commented_code": "A subscriber may want to unsubscribe at some point, so let's build that next.\n\nFirst, we need a route for unsubscribing that will be the URL we include in\nemails.\nemails, explicitly setting the identifying param to `token` (instead of the\nstandard `id`).\n\n```ruby\n  resource :unsubscribe, only: [ :show ]\n  resource :unsubscribe, param: :token, only: [ :show ]",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1915597213",
        "repo_full_name": "rails/rails",
        "pr_number": 54198,
        "pr_file": "guides/source/getting_started.md",
        "discussion_id": "1915597213",
        "commented_code": "@@ -2353,10 +2353,11 @@ module could be used in multiple models to provide the same functionality.\n A subscriber may want to unsubscribe at some point, so let's build that next.\n \n First, we need a route for unsubscribing that will be the URL we include in\n-emails.\n+emails, explicitly setting the identifying param to `token` (instead of the\n+standard `id`).\n \n ```ruby\n-  resource :unsubscribe, only: [ :show ]\n+  resource :unsubscribe, param: :token, only: [ :show ]",
        "comment_created_at": "2025-01-14T21:04:58+00:00",
        "comment_author": "Edouard-chin",
        "comment_body": "The `param` argument has no effect here as it's a singular resource. It only works for resource**s** (plural).\r\n\r\nAre you sure that calling `unsubscribe_url(token: \"blabla\")` doesn't work? It should add the token as a query string parameter (`https://example.com/unsubscribe?token=blabla`) regardless of what's in the route definition.",
        "pr_file_module": null
      },
      {
        "comment_id": "1915945672",
        "repo_full_name": "rails/rails",
        "pr_number": 54198,
        "pr_file": "guides/source/getting_started.md",
        "discussion_id": "1915597213",
        "commented_code": "@@ -2353,10 +2353,11 @@ module could be used in multiple models to provide the same functionality.\n A subscriber may want to unsubscribe at some point, so let's build that next.\n \n First, we need a route for unsubscribing that will be the URL we include in\n-emails.\n+emails, explicitly setting the identifying param to `token` (instead of the\n+standard `id`).\n \n ```ruby\n-  resource :unsubscribe, only: [ :show ]\n+  resource :unsubscribe, param: :token, only: [ :show ]",
        "comment_created_at": "2025-01-15T05:03:19+00:00",
        "comment_author": "jainil",
        "comment_body": "You're right. This is a miss at my end as I used the `resources` declaration in my follow along project. I'll close this as it's a non-issue. Thanks for the review!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1098148056",
    "pr_number": 47229,
    "pr_file": "guides/source/action_cable_overview.md",
    "created_at": "2023-02-07T03:53:29+00:00",
    "commented_code": "# Called when the consumer has successfully\n  # become a subscriber to this channel.\n  def subscribed\n    # stream_from \"some_channel\"\n  end\n\n  # Called once a consumer has cut its cable connection.\n  def unsubscribed\n    # Any cleanup needed when channel is unsubscribed\n  end\nend\n```\n\n#### Actions\n\nAlmost any public method declared on a channel is automatically exposed as a\ncallable action to the client. These methods can take an optional `data`\nargument containing an optional Hash sent by the client.\n\nThe `#subscribed` and `#unsubscribed` methods , and any public method\ndefined on `ActionCable::Channel::Base`, can not be called by the client.\n\nExample:\n\n```ruby\nclass AppearanceChannel < ApplicationCable::Channel\n  def subscribed\n    @connection_token = generate_connection_token\n  end\n\n  def unsubscribed\n    current_user.disappear @connection_token\n  end\n\n  def appear(data)\n    current_user.appear @connection_token, on: data['appearing_on']\n  end\n\n  def away\n    current_user.away @connection_token\n  end\n\n  private\n    def generate_connection_token\n      SecureRandom.hex(36)\n    end\nend\n```\n\nIn this example `#appear` and `#away` are callable by the client, whereas\n`#subscribed` and `#unsubscribed` are not. `#generate_connection_token` is also\nnot callable, since it's a private method. You'll see that `#appear` accepts a\n`data` parameter, which it then uses as part of its model call. `#away` does\nnot, since it's simply a trigger action.",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1098148056",
        "repo_full_name": "rails/rails",
        "pr_number": 47229,
        "pr_file": "guides/source/action_cable_overview.md",
        "discussion_id": "1098148056",
        "commented_code": "@@ -235,10 +235,58 @@ class ChatChannel < ApplicationCable::Channel\n   # Called when the consumer has successfully\n   # become a subscriber to this channel.\n   def subscribed\n+    # stream_from \"some_channel\"\n+  end\n+\n+  # Called once a consumer has cut its cable connection.\n+  def unsubscribed\n+    # Any cleanup needed when channel is unsubscribed\n   end\n end\n ```\n \n+#### Actions\n+\n+Almost any public method declared on a channel is automatically exposed as a\n+callable action to the client. These methods can take an optional `data`\n+argument containing an optional Hash sent by the client.\n+\n+The `#subscribed` and `#unsubscribed` methods , and any public method\n+defined on `ActionCable::Channel::Base`, can not be called by the client.\n+\n+Example:\n+\n+```ruby\n+class AppearanceChannel < ApplicationCable::Channel\n+  def subscribed\n+    @connection_token = generate_connection_token\n+  end\n+\n+  def unsubscribed\n+    current_user.disappear @connection_token\n+  end\n+\n+  def appear(data)\n+    current_user.appear @connection_token, on: data['appearing_on']\n+  end\n+\n+  def away\n+    current_user.away @connection_token\n+  end\n+\n+  private\n+    def generate_connection_token\n+      SecureRandom.hex(36)\n+    end\n+end\n+```\n+\n+In this example `#appear` and `#away` are callable by the client, whereas\n+`#subscribed` and `#unsubscribed` are not. `#generate_connection_token` is also\n+not callable, since it's a private method. You'll see that `#appear` accepts a\n+`data` parameter, which it then uses as part of its model call. `#away` does\n+not, since it's simply a trigger action.",
        "comment_created_at": "2023-02-07T03:53:29+00:00",
        "comment_author": "zzak",
        "comment_body": "I think this example comes from here:\r\nhttps://edgeapi.rubyonrails.org/classes/ActionCable/Channel/Base.html\r\n\r\nWhich is fine, but I think if we're going to update the description let's do it in both places.\r\n\r\ne.g. (without code formatting, from copy/paste)\r\n\r\n> In this example, the subscribed and unsubscribed methods are not callable methods, as they were already declared in [ActionCable::Channel::Base](https://edgeapi.rubyonrails.org/classes/ActionCable/Channel/Base.html), but #appear and #away are. #generate_connection_token is also not callable, since it\u2019s a private method. You\u2019ll see that appear accepts a data parameter, which it then uses as part of its model call. #away does not, since it\u2019s simply a trigger action.\r\n> \r\n> Also note that in this example, current_user is available because it was marked as an identifying attribute on the connection. All such identifiers will automatically create a delegation method of the same name on the channel instance.",
        "pr_file_module": null
      }
    ]
  }
]
