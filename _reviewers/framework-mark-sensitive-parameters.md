---
title: Mark sensitive parameters
description: Always use the `#[\SensitiveParameter]` attribute for parameters containing
  sensitive information such as passwords, tokens, API keys, and personal identifiable
  information. This prevents accidental exposure of sensitive data in logs, stack
  traces, and debugging information, which could otherwise lead to security breaches.
repository: laravel/framework
label: Security
language: PHP
comments_count: 2
repository_stars: 33763
---

Always use the `#[\SensitiveParameter]` attribute for parameters containing sensitive information such as passwords, tokens, API keys, and personal identifiable information. This prevents accidental exposure of sensitive data in logs, stack traces, and debugging information, which could otherwise lead to security breaches.

```php
// Before - security risk
public function __construct(
    public ?string $username = null,
    public ?string $pass = null,
) {}

// After - secure
public function __construct(
    public ?string $username = null,
    #[\SensitiveParameter]
    public ?string $pass = null,
) {}

// Also use in method parameters
public function validateCredentials(
    $username, 
    #[\SensitiveParameter] $password
) {
    // Password won't appear in logs or stack traces
}
```

For legacy PHP versions without attribute support, consider using alternative patterns such as:
1. Accepting sensitive data through non-logged channels
2. Sanitizing log output manually before writing
3. Using specialized secure input handlers

Additionally, ensure proper error handling for security-critical functions. Avoid using error suppression operators (@) in favor of try-catch blocks that capture errors without exposing implementation details.


[
  {
    "discussion_id": "1878116494",
    "pr_number": 53821,
    "pr_file": "src/Illuminate/Hashing/ArgonHasher.php",
    "created_at": "2024-12-10T13:40:39+00:00",
    "commented_code": "*/\n    public function make(#[\\SensitiveParameter] $value, array $options = [])\n    {\n        $hash = @password_hash($value, $this->algorithm(), [\n            'memory_cost' => $this->memory($options),\n            'time_cost' => $this->time($options),\n            'threads' => $this->threads($options),\n        ]);\n\n        if (! is_string($hash)) {\n        try {\n            $hash = password_hash($value, $this->algorithm(), [\n                'memory_cost' => $this->memory($options),\n                'time_cost' => $this->time($options),\n                'threads' => $this->threads($options),\n            ]);\n        } catch (Error) {",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1878116494",
        "repo_full_name": "laravel/framework",
        "pr_number": 53821,
        "pr_file": "src/Illuminate/Hashing/ArgonHasher.php",
        "discussion_id": "1878116494",
        "commented_code": "@@ -60,13 +61,13 @@ public function __construct(array $options = [])\n      */\n     public function make(#[\\SensitiveParameter] $value, array $options = [])\n     {\n-        $hash = @password_hash($value, $this->algorithm(), [\n-            'memory_cost' => $this->memory($options),\n-            'time_cost' => $this->time($options),\n-            'threads' => $this->threads($options),\n-        ]);\n-\n-        if (! is_string($hash)) {\n+        try {\n+            $hash = password_hash($value, $this->algorithm(), [\n+                'memory_cost' => $this->memory($options),\n+                'time_cost' => $this->time($options),\n+                'threads' => $this->threads($options),\n+            ]);\n+        } catch (Error) {",
        "comment_created_at": "2024-12-10T13:40:39+00:00",
        "comment_author": "cosmastech",
        "comment_body": "Might it be helpful to add this caught Error as the `previous` parameter of the RuntimeException?",
        "pr_file_module": null
      },
      {
        "comment_id": "1878332094",
        "repo_full_name": "laravel/framework",
        "pr_number": 53821,
        "pr_file": "src/Illuminate/Hashing/ArgonHasher.php",
        "discussion_id": "1878116494",
        "commented_code": "@@ -60,13 +61,13 @@ public function __construct(array $options = [])\n      */\n     public function make(#[\\SensitiveParameter] $value, array $options = [])\n     {\n-        $hash = @password_hash($value, $this->algorithm(), [\n-            'memory_cost' => $this->memory($options),\n-            'time_cost' => $this->time($options),\n-            'threads' => $this->threads($options),\n-        ]);\n-\n-        if (! is_string($hash)) {\n+        try {\n+            $hash = password_hash($value, $this->algorithm(), [\n+                'memory_cost' => $this->memory($options),\n+                'time_cost' => $this->time($options),\n+                'threads' => $this->threads($options),\n+            ]);\n+        } catch (Error) {",
        "comment_created_at": "2024-12-10T15:38:01+00:00",
        "comment_author": "browner12",
        "comment_body": "yah, I was considering that. is there any security implication though, because it could expose info like which algo is being used?",
        "pr_file_module": null
      },
      {
        "comment_id": "1878386477",
        "repo_full_name": "laravel/framework",
        "pr_number": 53821,
        "pr_file": "src/Illuminate/Hashing/ArgonHasher.php",
        "discussion_id": "1878116494",
        "commented_code": "@@ -60,13 +61,13 @@ public function __construct(array $options = [])\n      */\n     public function make(#[\\SensitiveParameter] $value, array $options = [])\n     {\n-        $hash = @password_hash($value, $this->algorithm(), [\n-            'memory_cost' => $this->memory($options),\n-            'time_cost' => $this->time($options),\n-            'threads' => $this->threads($options),\n-        ]);\n-\n-        if (! is_string($hash)) {\n+        try {\n+            $hash = password_hash($value, $this->algorithm(), [\n+                'memory_cost' => $this->memory($options),\n+                'time_cost' => $this->time($options),\n+                'threads' => $this->threads($options),\n+            ]);\n+        } catch (Error) {",
        "comment_created_at": "2024-12-10T16:09:01+00:00",
        "comment_author": "cosmastech",
        "comment_body": "Isn't it already showing the hashing algo in the exception message?\n\nIn theory, these exceptions should not be passed along to the end-user when the app is set to production mode.\n\n(I don't have a strong opinion on it either way, just a thought as I have fallen into the practice of forwarding exceptions when throwing a new one)",
        "pr_file_module": null
      },
      {
        "comment_id": "1878387944",
        "repo_full_name": "laravel/framework",
        "pr_number": 53821,
        "pr_file": "src/Illuminate/Hashing/ArgonHasher.php",
        "discussion_id": "1878116494",
        "commented_code": "@@ -60,13 +61,13 @@ public function __construct(array $options = [])\n      */\n     public function make(#[\\SensitiveParameter] $value, array $options = [])\n     {\n-        $hash = @password_hash($value, $this->algorithm(), [\n-            'memory_cost' => $this->memory($options),\n-            'time_cost' => $this->time($options),\n-            'threads' => $this->threads($options),\n-        ]);\n-\n-        if (! is_string($hash)) {\n+        try {\n+            $hash = password_hash($value, $this->algorithm(), [\n+                'memory_cost' => $this->memory($options),\n+                'time_cost' => $this->time($options),\n+                'threads' => $this->threads($options),\n+            ]);\n+        } catch (Error) {",
        "comment_created_at": "2024-12-10T16:09:58+00:00",
        "comment_author": "cosmastech",
        "comment_body": "It also catches a generic Error object, which could be caused by any number of things. At least this way you can see what specifically happened.",
        "pr_file_module": null
      },
      {
        "comment_id": "1878417875",
        "repo_full_name": "laravel/framework",
        "pr_number": 53821,
        "pr_file": "src/Illuminate/Hashing/ArgonHasher.php",
        "discussion_id": "1878116494",
        "commented_code": "@@ -60,13 +61,13 @@ public function __construct(array $options = [])\n      */\n     public function make(#[\\SensitiveParameter] $value, array $options = [])\n     {\n-        $hash = @password_hash($value, $this->algorithm(), [\n-            'memory_cost' => $this->memory($options),\n-            'time_cost' => $this->time($options),\n-            'threads' => $this->threads($options),\n-        ]);\n-\n-        if (! is_string($hash)) {\n+        try {\n+            $hash = password_hash($value, $this->algorithm(), [\n+                'memory_cost' => $this->memory($options),\n+                'time_cost' => $this->time($options),\n+                'threads' => $this->threads($options),\n+            ]);\n+        } catch (Error) {",
        "comment_created_at": "2024-12-10T16:24:50+00:00",
        "comment_author": "browner12",
        "comment_body": "it could also expose other info, like cost factor, etc. \r\n\r\nyou're right, it should never show to users in production.\r\n\r\nI'd say give a PR a shot, and see what other people think.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1837330959",
    "pr_number": 53370,
    "pr_file": "src/Illuminate/Support/Url.php",
    "created_at": "2024-11-12T00:21:55+00:00",
    "commented_code": "<?php\n\nnamespace Illuminate\\Support;\n\nuse Illuminate\\Contracts\\Support\\Arrayable;\nuse Stringable;\n\nclass Url implements Arrayable, Stringable\n{\n    /**\n     * Constructor.\n     */\n    public function __construct(\n        public ?string $scheme = null,\n        public ?string $host = null,\n        public ?int $port = null,\n        public ?string $user = null,\n        public ?string $pass = null,",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1837330959",
        "repo_full_name": "laravel/framework",
        "pr_number": 53370,
        "pr_file": "src/Illuminate/Support/Url.php",
        "discussion_id": "1837330959",
        "commented_code": "@@ -0,0 +1,113 @@\n+<?php\n+\n+namespace Illuminate\\Support;\n+\n+use Illuminate\\Contracts\\Support\\Arrayable;\n+use Stringable;\n+\n+class Url implements Arrayable, Stringable\n+{\n+    /**\n+     * Constructor.\n+     */\n+    public function __construct(\n+        public ?string $scheme = null,\n+        public ?string $host = null,\n+        public ?int $port = null,\n+        public ?string $user = null,\n+        public ?string $pass = null,",
        "comment_created_at": "2024-11-12T00:21:55+00:00",
        "comment_author": "timacdonald",
        "comment_body": "Should we mark this as sensitive so it does not end up in logs / stacktraces?\r\n\r\n```suggestion\r\n        #[\\SensitiveParameter]\r\n        public ?string $pass = null,\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1837332870",
        "repo_full_name": "laravel/framework",
        "pr_number": 53370,
        "pr_file": "src/Illuminate/Support/Url.php",
        "discussion_id": "1837330959",
        "commented_code": "@@ -0,0 +1,113 @@\n+<?php\n+\n+namespace Illuminate\\Support;\n+\n+use Illuminate\\Contracts\\Support\\Arrayable;\n+use Stringable;\n+\n+class Url implements Arrayable, Stringable\n+{\n+    /**\n+     * Constructor.\n+     */\n+    public function __construct(\n+        public ?string $scheme = null,\n+        public ?string $host = null,\n+        public ?int $port = null,\n+        public ?string $user = null,\n+        public ?string $pass = null,",
        "comment_created_at": "2024-11-12T00:25:35+00:00",
        "comment_author": "stevebauman",
        "comment_body": "Yup I agree!",
        "pr_file_module": null
      }
    ]
  }
]
