---
title: Example documentation standards
description: Organize API documentation examples for maximum clarity and usefulness.
  Place hand-written examples before generated examples since they're typically more
  valuable to users. When using @example tags, include only the descriptive title
  without redundant 'Example:' prefixes.
repository: aws/aws-sdk-js
label: Documentation
language: Ruby
comments_count: 2
repository_stars: 7628
---

Organize API documentation examples for maximum clarity and usefulness. Place hand-written examples before generated examples since they're typically more valuable to users. When using @example tags, include only the descriptive title without redundant 'Example:' prefixes.

For instance:
```ruby
# Good
@example Custom implementation
  # Hand-written example here
@example Calling the operation
  # Generated example here

# Avoid
@example Example: Custom implementation
  # Example here
```

This approach improves readability and maintains consistent documentation style.


[
  {
    "discussion_id": "35271327",
    "pr_number": 667,
    "pr_file": "doc-src/templates/api-versions/model_documentor.rb",
    "created_at": "2015-07-22T22:20:41+00:00",
    "commented_code": "@lines += shapes(api, operation['input']).map {|line| \"  \" + line }\n\n    ## @example tag\n\n    @lines << \"@example Calling the #{method_name(operation_name)} operation\"",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "35271327",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 667,
        "pr_file": "doc-src/templates/api-versions/model_documentor.rb",
        "discussion_id": "35271327",
        "commented_code": "@@ -93,11 +93,19 @@ def initialize(operation_name, operation, api, klass)\n     @lines += shapes(api, operation['input']).map {|line| \"  \" + line }\n \n     ## @example tag\n-\n     @lines << \"@example Calling the #{method_name(operation_name)} operation\"",
        "comment_created_at": "2015-07-22T22:20:41+00:00",
        "comment_author": "lsegal",
        "comment_body": "I would suggest moving any hand-written examples above the generated example, since they are likely to be more correct / useful.\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "35271330",
    "pr_number": 667,
    "pr_file": "doc-src/templates/api-versions/model_documentor.rb",
    "created_at": "2015-07-22T22:20:42+00:00",
    "commented_code": "@lines += shapes(api, operation['input']).map {|line| \"  \" + line }\n\n    ## @example tag\n\n    @lines << \"@example Calling the #{method_name(operation_name)} operation\"\n    @lines << generate_example(api, klass, method_name(operation_name),\n                operation['input']).split(\"\\n\").map {|line| \"  \" + line }\n    @lines << \"\"\n    if examples\n      examples.each do |example|\n        @lines << \"@example Example: #{example['title']}\"",
    "repo_full_name": "aws/aws-sdk-js",
    "discussion_comments": [
      {
        "comment_id": "35271330",
        "repo_full_name": "aws/aws-sdk-js",
        "pr_number": 667,
        "pr_file": "doc-src/templates/api-versions/model_documentor.rb",
        "discussion_id": "35271330",
        "commented_code": "@@ -93,11 +93,19 @@ def initialize(operation_name, operation, api, klass)\n     @lines += shapes(api, operation['input']).map {|line| \"  \" + line }\n \n     ## @example tag\n-\n     @lines << \"@example Calling the #{method_name(operation_name)} operation\"\n     @lines << generate_example(api, klass, method_name(operation_name),\n                 operation['input']).split(\"\\n\").map {|line| \"  \" + line }\n-    @lines << \"\"\n+    if examples\n+      examples.each do |example|\n+        @lines << \"@example Example: #{example['title']}\"",
        "comment_created_at": "2015-07-22T22:20:42+00:00",
        "comment_author": "lsegal",
        "comment_body": "Example tags should not be prefixed with \"Example:\" text, let's just list the title.\n",
        "pr_file_module": null
      }
    ]
  }
]
