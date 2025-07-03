---
title: Optimize loop operations
description: 'When writing loops, optimize for both readability and performance by
  following these key principles:


  1. **Exit early** when a decision can be made:

  ```php'
repository: laravel/framework
label: Algorithms
language: PHP
comments_count: 4
repository_stars: 33763
---

When writing loops, optimize for both readability and performance by following these key principles:

1. **Exit early** when a decision can be made:
```php
// Instead of this:
foreach ($keys as $key) {
    if (! static::has($array, $key)) {
        $result = false;
    }
}
return $result;

// Do this:
foreach ($keys as $key) {
    if (! static::has($array, $key)) {
        return false;
    }
}
return true;
```

2. **Move invariant operations outside loops**:
```php
// Instead of this:
foreach ($array as $key => $item) {
    $groupKey = is_callable($groupBy) ? $groupBy($item, $key) : static::get($item, $groupBy);
    // ...
}

// Do this:
$groupBy = is_callable($groupBy) ? $groupBy : fn ($item) => static::get($item, $groupBy);
foreach ($array as $key => $item) {
    $groupKey = $groupBy($item, $key);
    // ...
}
```

3. **Use O(1) operations** where possible instead of O(n):
```php
// Instead of this:
if (in_array(InteractsWithQueue::class, $uses) && in_array(Queueable::class, $uses)) {
    // ...
}

// Do this:
if (isset($uses[InteractsWithQueue::class], $uses[Queueable::class])) {
    // ...
}
```

4. **Add early termination conditions** for algorithms that can complete before processing all elements:
```php
// Add early exit:
foreach ($map as $roman => $value) {
    while ($number >= $value) {
        $result .= $roman;
        $number -= $value;
    }
    
    if ($number === 0) {
        return $result;
    }
}
```

These optimizations help reduce computational complexity and unnecessary operations, resulting in more efficient and maintainable code.


[
  {
    "discussion_id": "2101429227",
    "pr_number": 55815,
    "pr_file": "src/Illuminate/Collections/Arr.php",
    "created_at": "2025-05-22T01:05:00+00:00",
    "commented_code": "return true;\n    }\n\n    /**\n     * Determine if all keys exist in an array using \"dot\" notation.\n     *\n     * @param  \\ArrayAccess|array  $array\n     * @param  string|array  $keys\n     * @return bool\n     */\n    public static function hasAll($array, $keys)\n    {\n        $keys = (array) $keys;\n\n        if (! $array || $keys === []) {\n            return false;\n        }\n\n        $result = true;\n\n        foreach ($keys as $key) {\n            if (! static::has($array, $key)) {\n                $result = false;\n            }\n        }\n\n        return $result;",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2101429227",
        "repo_full_name": "laravel/framework",
        "pr_number": 55815,
        "pr_file": "src/Illuminate/Collections/Arr.php",
        "discussion_id": "2101429227",
        "commented_code": "@@ -495,6 +495,32 @@ public static function has($array, $keys)\n         return true;\n     }\n \n+    /**\n+     * Determine if all keys exist in an array using \"dot\" notation.\n+     *\n+     * @param  \\ArrayAccess|array  $array\n+     * @param  string|array  $keys\n+     * @return bool\n+     */\n+    public static function hasAll($array, $keys)\n+    {\n+        $keys = (array) $keys;\n+\n+        if (! $array || $keys === []) {\n+            return false;\n+        }\n+\n+        $result = true;\n+\n+        foreach ($keys as $key) {\n+            if (! static::has($array, $key)) {\n+                $result = false;\n+            }\n+        }\n+\n+        return $result;",
        "comment_created_at": "2025-05-22T01:05:00+00:00",
        "comment_author": "Rizky92",
        "comment_body": "Might be better to bail on first failure.\r\n```suggestion\r\n        foreach ($keys as $key) {\r\n            if (! static::has($array, $key)) {\r\n                return false;\r\n            }\r\n        }\r\n\r\n        return true;\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2101461078",
        "repo_full_name": "laravel/framework",
        "pr_number": 55815,
        "pr_file": "src/Illuminate/Collections/Arr.php",
        "discussion_id": "2101429227",
        "commented_code": "@@ -495,6 +495,32 @@ public static function has($array, $keys)\n         return true;\n     }\n \n+    /**\n+     * Determine if all keys exist in an array using \"dot\" notation.\n+     *\n+     * @param  \\ArrayAccess|array  $array\n+     * @param  string|array  $keys\n+     * @return bool\n+     */\n+    public static function hasAll($array, $keys)\n+    {\n+        $keys = (array) $keys;\n+\n+        if (! $array || $keys === []) {\n+            return false;\n+        }\n+\n+        $result = true;\n+\n+        foreach ($keys as $key) {\n+            if (! static::has($array, $key)) {\n+                $result = false;\n+            }\n+        }\n+\n+        return $result;",
        "comment_created_at": "2025-05-22T01:42:28+00:00",
        "comment_author": "devajmeireles",
        "comment_body": "Thanks!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2051354482",
    "pr_number": 55472,
    "pr_file": "src/Illuminate/Collections/Arr.php",
    "created_at": "2025-04-19T02:42:19+00:00",
    "commented_code": "return is_array($value) ? $value : [$value];\n    }\n\n    /**\n     * Group an associative array by a key or callback.\n     *\n     * @param  array  $array\n     * @param  string|int|callable  $groupBy\n     * @param  bool  $preserveKeys\n     * @return array\n     */\n    public static function groupBy($array, $groupBy, $preserveKeys = false)\n    {\n        $result = [];\n\n        foreach ($array as $key => $item) {\n            $groupKey = is_callable($groupBy) ? $groupBy($item, $key) : static::get($item, $groupBy);",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2051354482",
        "repo_full_name": "laravel/framework",
        "pr_number": 55472,
        "pr_file": "src/Illuminate/Collections/Arr.php",
        "discussion_id": "2051354482",
        "commented_code": "@@ -1021,4 +1021,29 @@ public static function wrap($value)\n \n         return is_array($value) ? $value : [$value];\n     }\n+\n+    /**\n+     * Group an associative array by a key or callback.\n+     *\n+     * @param  array  $array\n+     * @param  string|int|callable  $groupBy\n+     * @param  bool  $preserveKeys\n+     * @return array\n+     */\n+    public static function groupBy($array, $groupBy, $preserveKeys = false)\n+    {\n+        $result = [];\n+\n+        foreach ($array as $key => $item) {\n+            $groupKey = is_callable($groupBy) ? $groupBy($item, $key) : static::get($item, $groupBy);",
        "comment_created_at": "2025-04-19T02:42:19+00:00",
        "comment_author": "rodrigopedra",
        "comment_body": "I would ensure `$groupBy` is a callback out the loop, so we don't need to check if it is a callback on every item.\r\n\r\nSomething like this:\r\n\r\n```php\r\n$groupBy = is_callable($groupBy) ? $groupBy : fn ($item) => static::get($item, $groupBy);\r\n\r\nforeach ($array as $key => $item) {\r\n    $groupKey = $groupBy($item, $key);\r\n\r\n    // ...\r\n}\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2051403566",
        "repo_full_name": "laravel/framework",
        "pr_number": 55472,
        "pr_file": "src/Illuminate/Collections/Arr.php",
        "discussion_id": "2051354482",
        "commented_code": "@@ -1021,4 +1021,29 @@ public static function wrap($value)\n \n         return is_array($value) ? $value : [$value];\n     }\n+\n+    /**\n+     * Group an associative array by a key or callback.\n+     *\n+     * @param  array  $array\n+     * @param  string|int|callable  $groupBy\n+     * @param  bool  $preserveKeys\n+     * @return array\n+     */\n+    public static function groupBy($array, $groupBy, $preserveKeys = false)\n+    {\n+        $result = [];\n+\n+        foreach ($array as $key => $item) {\n+            $groupKey = is_callable($groupBy) ? $groupBy($item, $key) : static::get($item, $groupBy);",
        "comment_created_at": "2025-04-19T05:54:40+00:00",
        "comment_author": "vishal2931",
        "comment_body": "Thanks for the feedback, but that approach looks more readable than this one. \ud83e\udd14",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2096571598",
    "pr_number": 55784,
    "pr_file": "src/Illuminate/Support/Number.php",
    "created_at": "2025-05-19T22:38:42+00:00",
    "commented_code": "throw new RuntimeException('The \"intl\" PHP extension is required to use the ['.$method.'] method.');\n        }\n    }\n\n    /**\n     * Convert an integer into its Roman numeral representation.\n     *\n     * @param  int  $number  The number to convert (must be between 1 and 3999)\n     * @return string The Roman numeral representation\n     *\n     * @throws InvalidArgumentException If the number is not between 1 and 3999\n     */\n    public static function roman(int $number): string\n    {\n        if ($number <= 0 || $number > 3999) {\n            throw new InvalidArgumentException('Number must be between 1 and 3999.');\n        }\n\n        $map = [\n            'M' => 1000,\n            'CM' => 900,\n            'D' => 500,\n            'CD' => 400,\n            'C' => 100,\n            'XC' => 90,\n            'L' => 50,\n            'XL' => 40,\n            'X' => 10,\n            'IX' => 9,\n            'V' => 5,\n            'IV' => 4,\n            'I' => 1,\n        ];\n\n        $result = '';\n\n        foreach ($map as $roman => $value) {\n            while ($number >= $value) {\n                $result .= $roman;\n                $number -= $value;\n            }\n        }",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2096571598",
        "repo_full_name": "laravel/framework",
        "pr_number": 55784,
        "pr_file": "src/Illuminate/Support/Number.php",
        "discussion_id": "2096571598",
        "commented_code": "@@ -427,4 +428,46 @@ protected static function ensureIntlExtensionIsInstalled()\n             throw new RuntimeException('The \"intl\" PHP extension is required to use the ['.$method.'] method.');\n         }\n     }\n+\n+    /**\n+     * Convert an integer into its Roman numeral representation.\n+     *\n+     * @param  int  $number  The number to convert (must be between 1 and 3999)\n+     * @return string The Roman numeral representation\n+     *\n+     * @throws InvalidArgumentException If the number is not between 1 and 3999\n+     */\n+    public static function roman(int $number): string\n+    {\n+        if ($number <= 0 || $number > 3999) {\n+            throw new InvalidArgumentException('Number must be between 1 and 3999.');\n+        }\n+\n+        $map = [\n+            'M' => 1000,\n+            'CM' => 900,\n+            'D' => 500,\n+            'CD' => 400,\n+            'C' => 100,\n+            'XC' => 90,\n+            'L' => 50,\n+            'XL' => 40,\n+            'X' => 10,\n+            'IX' => 9,\n+            'V' => 5,\n+            'IV' => 4,\n+            'I' => 1,\n+        ];\n+\n+        $result = '';\n+\n+        foreach ($map as $roman => $value) {\n+            while ($number >= $value) {\n+                $result .= $roman;\n+                $number -= $value;\n+            }\n+        }",
        "comment_created_at": "2025-05-19T22:38:42+00:00",
        "comment_author": "shaedrich",
        "comment_body": "You could prevent trailing iterations when calculating the result is done, speeding the process slightly more up:\r\n```suggestion\r\n        foreach ($map as $roman => $value) {\r\n            while ($number >= $value) {\r\n                $result .= $roman;\r\n                $number -= $value;\r\n            }\r\n            \r\n            if ($number === 0) {\r\n            \treturn $result;\r\n            }\r\n        }\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1850814073",
    "pr_number": 53596,
    "pr_file": "src/Illuminate/Bus/Dispatcher.php",
    "created_at": "2024-11-20T18:41:45+00:00",
    "commented_code": "{\n        $uses = class_uses_recursive($command);\n\n        if (in_array(InteractsWithQueue::class, $uses) &&\n            in_array(Queueable::class, $uses) &&\n            ! $command->job) {\n        if (isset($uses[InteractsWithQueue::class], $uses[Queueable::class]) && ! $command->job) {",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1850814073",
        "repo_full_name": "laravel/framework",
        "pr_number": 53596,
        "pr_file": "src/Illuminate/Bus/Dispatcher.php",
        "discussion_id": "1850814073",
        "commented_code": "@@ -109,9 +109,7 @@ public function dispatchNow($command, $handler = null)\n     {\n         $uses = class_uses_recursive($command);\n \n-        if (in_array(InteractsWithQueue::class, $uses) &&\n-            in_array(Queueable::class, $uses) &&\n-            ! $command->job) {\n+        if (isset($uses[InteractsWithQueue::class], $uses[Queueable::class]) && ! $command->job) {",
        "comment_created_at": "2024-11-20T18:41:45+00:00",
        "comment_author": "GrahamCampbell",
        "comment_body": "This is an incorrect refactor. isset looks at the keys. in_array looks at the values.",
        "pr_file_module": null
      },
      {
        "comment_id": "1850820663",
        "repo_full_name": "laravel/framework",
        "pr_number": 53596,
        "pr_file": "src/Illuminate/Bus/Dispatcher.php",
        "discussion_id": "1850814073",
        "commented_code": "@@ -109,9 +109,7 @@ public function dispatchNow($command, $handler = null)\n     {\n         $uses = class_uses_recursive($command);\n \n-        if (in_array(InteractsWithQueue::class, $uses) &&\n-            in_array(Queueable::class, $uses) &&\n-            ! $command->job) {\n+        if (isset($uses[InteractsWithQueue::class], $uses[Queueable::class]) && ! $command->job) {",
        "comment_created_at": "2024-11-20T18:47:36+00:00",
        "comment_author": "ralphjsmit",
        "comment_body": "Isn't `class_uses_recursive()` outputting the exact same key as value?\r\n```php\r\n[\r\n   SomeConcern::class => SomeConcern::class,\r\n]\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1850845485",
        "repo_full_name": "laravel/framework",
        "pr_number": 53596,
        "pr_file": "src/Illuminate/Bus/Dispatcher.php",
        "discussion_id": "1850814073",
        "commented_code": "@@ -109,9 +109,7 @@ public function dispatchNow($command, $handler = null)\n     {\n         $uses = class_uses_recursive($command);\n \n-        if (in_array(InteractsWithQueue::class, $uses) &&\n-            in_array(Queueable::class, $uses) &&\n-            ! $command->job) {\n+        if (isset($uses[InteractsWithQueue::class], $uses[Queueable::class]) && ! $command->job) {",
        "comment_created_at": "2024-11-20T19:08:07+00:00",
        "comment_author": "dshafik",
        "comment_body": "@GrahamCampbell as @ralphjsmit points out, the result of `class_uses_recursive()` is a key-value pair with the trait name for _both_, therefore you can use `isset()` to check for the usage of a trait (`O(1)`) rather than traverse the array till you find the value using `in_array()`. (`O(n)`)",
        "pr_file_module": null
      },
      {
        "comment_id": "1851152975",
        "repo_full_name": "laravel/framework",
        "pr_number": 53596,
        "pr_file": "src/Illuminate/Bus/Dispatcher.php",
        "discussion_id": "1850814073",
        "commented_code": "@@ -109,9 +109,7 @@ public function dispatchNow($command, $handler = null)\n     {\n         $uses = class_uses_recursive($command);\n \n-        if (in_array(InteractsWithQueue::class, $uses) &&\n-            in_array(Queueable::class, $uses) &&\n-            ! $command->job) {\n+        if (isset($uses[InteractsWithQueue::class], $uses[Queueable::class]) && ! $command->job) {",
        "comment_created_at": "2024-11-21T00:24:15+00:00",
        "comment_author": "crynobone",
        "comment_body": "This should be fine and we use `isset()` as well for https://github.com/laravel/framework/blob/eb625fa6aa083dbae74b4f2cc7dc6dafcce5ff07/src/Illuminate/Foundation/Testing/Concerns/InteractsWithTestCaseLifecycle.php#L196-L220",
        "pr_file_module": null
      },
      {
        "comment_id": "1851217495",
        "repo_full_name": "laravel/framework",
        "pr_number": 53596,
        "pr_file": "src/Illuminate/Bus/Dispatcher.php",
        "discussion_id": "1850814073",
        "commented_code": "@@ -109,9 +109,7 @@ public function dispatchNow($command, $handler = null)\n     {\n         $uses = class_uses_recursive($command);\n \n-        if (in_array(InteractsWithQueue::class, $uses) &&\n-            in_array(Queueable::class, $uses) &&\n-            ! $command->job) {\n+        if (isset($uses[InteractsWithQueue::class], $uses[Queueable::class]) && ! $command->job) {",
        "comment_created_at": "2024-11-21T02:09:03+00:00",
        "comment_author": "dshafik",
        "comment_body": "@crynobone the `array_flip()` in that example should probably be removed too\u2026 (unrelated to this PR)",
        "pr_file_module": null
      }
    ]
  }
]
