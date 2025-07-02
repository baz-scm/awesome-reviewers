---
title: Contextual error messages
description: Error messages should provide sufficient context to understand and debug
  the problem efficiently. Include both the expected and actual values in error messages,
  along with specific information about what failed. This makes troubleshooting much
  more straightforward and reduces debugging time.
repository: rails/rails
label: Error Handling
language: Ruby
comments_count: 4
repository_stars: 57027
---

Error messages should provide sufficient context to understand and debug the problem efficiently. Include both the expected and actual values in error messages, along with specific information about what failed. This makes troubleshooting much more straightforward and reduces debugging time.

**Good practice:**
```ruby
# Clear about what was expected and what was received
unless value == true || value == false
  raise ArgumentError, "distinct expects a boolean value, got: #{value.inspect}"
end

# Shows both expected and actual values
actual_checksum = service.compute_checksum(file) 
unless actual_checksum == checksum
  raise ActiveStorage::IntegrityError, "Checksum verification failed expecting #{checksum}, but downloaded file having #{actual_checksum}"
end

# Specific about which value caused the problem
unless ActiveStorage.supported_image_processing_methods.any? { |method| method_name == method }
  raise UnsupportedImageProcessingMethod, "Method '#{method_name}' is not supported. Supported methods: #{ActiveStorage.supported_image_processing_methods.join(', ')}"
end
```

**Bad practice:**
```ruby
# Vague error message with no context
unless value == true || value == false
  raise ArgumentError, "Invalid value"
end

# Missing the actual values causing the failure
unless actual_checksum == checksum
  raise ActiveStorage::IntegrityError, "Checksum verification failed"
end
```

Contextual error messages make your API more user-friendly and significantly reduce troubleshooting time when problems occur. They also serve as implicit documentation about parameter constraints and expected behaviors.


[
  {
    "discussion_id": "1485398106",
    "pr_number": 51045,
    "pr_file": "activerecord/lib/active_record/relation/query_methods.rb",
    "created_at": "2024-02-11T01:01:17+00:00",
    "commented_code": "# Like #distinct, but modifies relation in place.\n    def distinct!(value = true) # :nodoc:\n      unless [true, false].include?(value)\n        raise ArgumentError, \"Expected TrueClass or FalseClass, got #{value.class}\"\n      end",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1485398106",
        "repo_full_name": "rails/rails",
        "pr_number": 51045,
        "pr_file": "activerecord/lib/active_record/relation/query_methods.rb",
        "discussion_id": "1485398106",
        "commented_code": "@@ -1312,6 +1312,10 @@ def distinct(value = true)\n \n     # Like #distinct, but modifies relation in place.\n     def distinct!(value = true) # :nodoc:\n+      unless [true, false].include?(value)\n+        raise ArgumentError, \"Expected TrueClass or FalseClass, got #{value.class}\"\n+      end",
        "comment_created_at": "2024-02-11T01:01:17+00:00",
        "comment_author": "fatkodima",
        "comment_body": "```suggestion\r\n      unless value == true || value == false\r\n        raise ArgumentError, \"distinct expects a boolean value, got: #{value.inspect}\"\r\n      end\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1485398323",
        "repo_full_name": "rails/rails",
        "pr_number": 51045,
        "pr_file": "activerecord/lib/active_record/relation/query_methods.rb",
        "discussion_id": "1485398106",
        "commented_code": "@@ -1312,6 +1312,10 @@ def distinct(value = true)\n \n     # Like #distinct, but modifies relation in place.\n     def distinct!(value = true) # :nodoc:\n+      unless [true, false].include?(value)\n+        raise ArgumentError, \"Expected TrueClass or FalseClass, got #{value.class}\"\n+      end",
        "comment_created_at": "2024-02-11T01:01:47+00:00",
        "comment_author": "fatkodima",
        "comment_body": "This logic should be placed in `distinct` method, not `distinct!`.",
        "pr_file_module": null
      },
      {
        "comment_id": "1485400123",
        "repo_full_name": "rails/rails",
        "pr_number": 51045,
        "pr_file": "activerecord/lib/active_record/relation/query_methods.rb",
        "discussion_id": "1485398106",
        "commented_code": "@@ -1312,6 +1312,10 @@ def distinct(value = true)\n \n     # Like #distinct, but modifies relation in place.\n     def distinct!(value = true) # :nodoc:\n+      unless [true, false].include?(value)\n+        raise ArgumentError, \"Expected TrueClass or FalseClass, got #{value.class}\"\n+      end",
        "comment_created_at": "2024-02-11T01:06:34+00:00",
        "comment_author": "joshuay03",
        "comment_body": "> This logic should be placed in `distinct` method, not `distinct!`.\r\n\r\nShould we not keep it consistent acrross both even if the latter is undocumented?",
        "pr_file_module": null
      },
      {
        "comment_id": "1485564042",
        "repo_full_name": "rails/rails",
        "pr_number": 51045,
        "pr_file": "activerecord/lib/active_record/relation/query_methods.rb",
        "discussion_id": "1485398106",
        "commented_code": "@@ -1312,6 +1312,10 @@ def distinct(value = true)\n \n     # Like #distinct, but modifies relation in place.\n     def distinct!(value = true) # :nodoc:\n+      unless [true, false].include?(value)\n+        raise ArgumentError, \"Expected TrueClass or FalseClass, got #{value.class}\"\n+      end",
        "comment_created_at": "2024-02-11T10:11:44+00:00",
        "comment_author": "fatkodima",
        "comment_body": "Ok, I was sure that ActiveRecord prefers the suggested style inside that file, but I see examples of both error checking in user-facing and internal `!` methods.\r\nSo using it inside `distinct!` seems ok.",
        "pr_file_module": null
      },
      {
        "comment_id": "1485567824",
        "repo_full_name": "rails/rails",
        "pr_number": 51045,
        "pr_file": "activerecord/lib/active_record/relation/query_methods.rb",
        "discussion_id": "1485398106",
        "commented_code": "@@ -1312,6 +1312,10 @@ def distinct(value = true)\n \n     # Like #distinct, but modifies relation in place.\n     def distinct!(value = true) # :nodoc:\n+      unless [true, false].include?(value)\n+        raise ArgumentError, \"Expected TrueClass or FalseClass, got #{value.class}\"\n+      end",
        "comment_created_at": "2024-02-11T10:38:12+00:00",
        "comment_author": "joshuay03",
        "comment_body": "I have committed your suggestion but kept the validation in both `#distinct` and `distinct!`.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2095207282",
    "pr_number": 54468,
    "pr_file": "activestorage/lib/active_storage/downloader.rb",
    "created_at": "2025-05-19T08:54:15+00:00",
    "commented_code": "end\n\n      def verify_integrity_of(file, checksum:)\n        unless ActiveStorage.checksum_implementation.file(file).base64digest == checksum\n        unless service.compute_checksum(file) == checksum\n          raise ActiveStorage::IntegrityError",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2095207282",
        "repo_full_name": "rails/rails",
        "pr_number": 54468,
        "pr_file": "activestorage/lib/active_storage/downloader.rb",
        "discussion_id": "2095207282",
        "commented_code": "@@ -35,7 +35,7 @@ def download(key, file)\n       end\n \n       def verify_integrity_of(file, checksum:)\n-        unless ActiveStorage.checksum_implementation.file(file).base64digest == checksum\n+        unless service.compute_checksum(file) == checksum\n           raise ActiveStorage::IntegrityError",
        "comment_created_at": "2025-05-19T08:54:15+00:00",
        "comment_author": "bogdan",
        "comment_body": "Needs to be a little more clear when raising exception:\r\n\r\n```suggestion\r\n        actual_checksum = service.compute_checksum(file) \r\n        unless actual_checksum == checksum\r\n          raise ActiveStorage::IntegrityError, \"Checksum verification failed expecting #{checksum}, but downloaded file having #{actual_checksum}\"\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1938548965",
    "pr_number": 54341,
    "pr_file": "activesupport/lib/active_support/core_ext/range/sole.rb",
    "created_at": "2025-02-02T18:21:27+00:00",
    "commented_code": "# frozen_string_literal: true\n\nclass Range\n  # Returns the sole item in the range. If there are no items, or more\n  # than one item, raises Enumerable::SoleItemExpectedError.\n  #\n  #   (1..1).sole   # => 1\n  #   (2..1).sole   # => Enumerable::SoleItemExpectedError: no item found\n  #   (..1).sole    # => Enumerable::SoleItemExpectedError: multiple items found\n  def sole\n    if self.begin.nil? || self.end.nil?\n      raise ActiveSupport::EnumerableCoreExt::SoleItemExpectedError, \"multiple items found\"",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1938548965",
        "repo_full_name": "rails/rails",
        "pr_number": 54341,
        "pr_file": "activesupport/lib/active_support/core_ext/range/sole.rb",
        "discussion_id": "1938548965",
        "commented_code": "@@ -0,0 +1,17 @@\n+# frozen_string_literal: true\n+\n+class Range\n+  # Returns the sole item in the range. If there are no items, or more\n+  # than one item, raises Enumerable::SoleItemExpectedError.\n+  #\n+  #   (1..1).sole   # => 1\n+  #   (2..1).sole   # => Enumerable::SoleItemExpectedError: no item found\n+  #   (..1).sole    # => Enumerable::SoleItemExpectedError: multiple items found\n+  def sole\n+    if self.begin.nil? || self.end.nil?\n+      raise ActiveSupport::EnumerableCoreExt::SoleItemExpectedError, \"multiple items found\"",
        "comment_created_at": "2025-02-02T18:21:27+00:00",
        "comment_author": "nvasilevski",
        "comment_body": "Not sure if it's worth it but wanted to mention that we have an opportunity to be more specific in the message and tell that the instance is an endless array which by definition can not represent a sole item",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "873169750",
    "pr_number": 45100,
    "pr_file": "activestorage/lib/active_storage/transformers/image_magick.rb",
    "created_at": "2022-05-15T13:27:08+00:00",
    "commented_code": "# frozen_string_literal: true\n\nmodule ActiveStorage\n  module Transformers\n    class ImageMagick < ImageProcessingTransformer\n      private\n        def processor\n          ImageProcessing::MiniMagick\n        end\n\n        def validate_transformation(name, argument)\n          method_name = name.to_s.tr(\"-\", \"_\")\n\n          unless ActiveStorage.supported_image_processing_methods.any? { |method| method_name == method }\n            raise UnsupportedImageProcessingMethod, <<~ERROR.squish\n              One or more of the provided transformation methods is not supported.",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "873169750",
        "repo_full_name": "rails/rails",
        "pr_number": 45100,
        "pr_file": "activestorage/lib/active_storage/transformers/image_magick.rb",
        "discussion_id": "873169750",
        "commented_code": "@@ -0,0 +1,72 @@\n+# frozen_string_literal: true\n+\n+module ActiveStorage\n+  module Transformers\n+    class ImageMagick < ImageProcessingTransformer\n+      private\n+        def processor\n+          ImageProcessing::MiniMagick\n+        end\n+\n+        def validate_transformation(name, argument)\n+          method_name = name.to_s.tr(\"-\", \"_\")\n+\n+          unless ActiveStorage.supported_image_processing_methods.any? { |method| method_name == method }\n+            raise UnsupportedImageProcessingMethod, <<~ERROR.squish\n+              One or more of the provided transformation methods is not supported.",
        "comment_created_at": "2022-05-15T13:27:08+00:00",
        "comment_author": "byroot",
        "comment_body": "When writing error message, it's best to include the faulty value.",
        "pr_file_module": null
      }
    ]
  }
]
