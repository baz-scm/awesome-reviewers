---
title: Name indicates clear purpose
description: Names should clearly indicate their purpose, type, and behavior. This
  applies to methods, variables, and parameters. Choose names that are self-documenting
  and unambiguous.
repository: laravel/framework
label: Naming Conventions
language: PHP
comments_count: 6
repository_stars: 33763
---

Names should clearly indicate their purpose, type, and behavior. This applies to methods, variables, and parameters. Choose names that are self-documenting and unambiguous.

Key guidelines:
- Use prefixes for boolean methods (is, has, can)
- Use accurate type indicators (integer vs number)
- Choose domain-specific terms (digits vs length for numbers)
- Avoid abbreviated or ambiguous names

Example:
```php
// Unclear naming
public function pan($value) { }
public function num($len = 6) { }

// Clear naming
public function formatPanNumber($value) { }
public function generateRandomInteger(int $digits = 6) { }

// Boolean method naming
public function arrayable($value) { }     // Unclear purpose
public function isArrayable($value) { }   // Clear purpose
```

This standard helps prevent confusion, makes code self-documenting, and maintains consistency across the codebase.


[
  {
    "discussion_id": "2174034334",
    "pr_number": 56169,
    "pr_file": "tests/Database/DatabaseEloquentBuilderFindOrFailWithEnumTest.php",
    "created_at": "2025-06-30T00:51:53+00:00",
    "commented_code": "<?php\n\nnamespace Illuminate\\Tests\\Database;\n\nuse Illuminate\\Database\\Eloquent\\Model;\nuse Illuminate\\Database\\Eloquent\\ModelNotFoundException;\nuse Illuminate\\Database\\Schema\\Blueprint;\nuse Illuminate\\Support\\Facades\\Schema;\nuse Orchestra\\Testbench\\TestCase;\nuse PHPUnit\\Framework\\Attributes\\Test;\n\nclass DatabaseEloquentBuilderFindOrFailWithEnumTest extends TestCase\n{\n    protected function setUp(): void\n    {\n        parent::setUp();\n\n        $this->createSchema();\n    }\n\n    protected function tearDown(): void\n    {\n        Schema::drop('test_models');\n\n        parent::tearDown();\n    }\n\n    protected function getEnvironmentSetUp($app)\n    {\n        $app['config']->set('database.default', 'testing');\n    }\n\n    #[Test]\n    public function it_finds_existing_model_when_using_enum_id()\n    {\n        EloquentBuilderFindOrFailWithEnumTestModel::create(['id' => 1, 'name' => 'one']);\n\n        $model = EloquentBuilderFindOrFailWithEnumTestModel::findOrFail(EloquentBuilderFindOrFailWithEnumTestBackedEnum::One);\n\n        $this->assertInstanceOf(EloquentBuilderFindOrFailWithEnumTestModel::class, $model);\n        $this->assertTrue($model->exists);\n        $this->assertEquals(1, $model->id);\n    }\n\n    #[Test]\n    public function it_throws_exception_when_enum_id_does_not_exist()",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2174034334",
        "repo_full_name": "laravel/framework",
        "pr_number": 56169,
        "pr_file": "tests/Database/DatabaseEloquentBuilderFindOrFailWithEnumTest.php",
        "discussion_id": "2174034334",
        "commented_code": "@@ -0,0 +1,74 @@\n+<?php\n+\n+namespace Illuminate\\Tests\\Database;\n+\n+use Illuminate\\Database\\Eloquent\\Model;\n+use Illuminate\\Database\\Eloquent\\ModelNotFoundException;\n+use Illuminate\\Database\\Schema\\Blueprint;\n+use Illuminate\\Support\\Facades\\Schema;\n+use Orchestra\\Testbench\\TestCase;\n+use PHPUnit\\Framework\\Attributes\\Test;\n+\n+class DatabaseEloquentBuilderFindOrFailWithEnumTest extends TestCase\n+{\n+    protected function setUp(): void\n+    {\n+        parent::setUp();\n+\n+        $this->createSchema();\n+    }\n+\n+    protected function tearDown(): void\n+    {\n+        Schema::drop('test_models');\n+\n+        parent::tearDown();\n+    }\n+\n+    protected function getEnvironmentSetUp($app)\n+    {\n+        $app['config']->set('database.default', 'testing');\n+    }\n+\n+    #[Test]\n+    public function it_finds_existing_model_when_using_enum_id()\n+    {\n+        EloquentBuilderFindOrFailWithEnumTestModel::create(['id' => 1, 'name' => 'one']);\n+\n+        $model = EloquentBuilderFindOrFailWithEnumTestModel::findOrFail(EloquentBuilderFindOrFailWithEnumTestBackedEnum::One);\n+\n+        $this->assertInstanceOf(EloquentBuilderFindOrFailWithEnumTestModel::class, $model);\n+        $this->assertTrue($model->exists);\n+        $this->assertEquals(1, $model->id);\n+    }\n+\n+    #[Test]\n+    public function it_throws_exception_when_enum_id_does_not_exist()",
        "comment_created_at": "2025-06-30T00:51:53+00:00",
        "comment_author": "crynobone",
        "comment_body": "We don't use `Test` attribute in the framework, prefix the method name with `test` and use studly case.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2084631773",
    "pr_number": 55715,
    "pr_file": "src/Illuminate/Collections/Arr.php",
    "created_at": "2025-05-12T13:05:05+00:00",
    "commented_code": "return is_array($value) || $value instanceof ArrayAccess;\n    }\n\n    /**\n     * Determine whether the given value is arrayable.\n     *\n     * @param  mixed  $value\n     * @return bool\n     */\n    public static function arrayable($value)",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2084631773",
        "repo_full_name": "laravel/framework",
        "pr_number": 55715,
        "pr_file": "src/Illuminate/Collections/Arr.php",
        "discussion_id": "2084631773",
        "commented_code": "@@ -23,6 +28,21 @@ public static function accessible($value)\n         return is_array($value) || $value instanceof ArrayAccess;\n     }\n \n+    /**\n+     * Determine whether the given value is arrayable.\n+     *\n+     * @param  mixed  $value\n+     * @return bool\n+     */\n+    public static function arrayable($value)",
        "comment_created_at": "2025-05-12T13:05:05+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Wouldn't it make sense to use a prefix here to indicate the return value? Because, I would expect the method to convert it from array-like values to `Arrayable` instances\r\n```suggestion\r\n    public static function isArrayable($value)\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2084658378",
        "repo_full_name": "laravel/framework",
        "pr_number": 55715,
        "pr_file": "src/Illuminate/Collections/Arr.php",
        "discussion_id": "2084631773",
        "commented_code": "@@ -23,6 +28,21 @@ public static function accessible($value)\n         return is_array($value) || $value instanceof ArrayAccess;\n     }\n \n+    /**\n+     * Determine whether the given value is arrayable.\n+     *\n+     * @param  mixed  $value\n+     * @return bool\n+     */\n+    public static function arrayable($value)",
        "comment_created_at": "2025-05-12T13:18:12+00:00",
        "comment_author": "daniser",
        "comment_body": "I followed naming convention used in `Arr::accessible`.",
        "pr_file_module": null
      },
      {
        "comment_id": "2084679790",
        "repo_full_name": "laravel/framework",
        "pr_number": 55715,
        "pr_file": "src/Illuminate/Collections/Arr.php",
        "discussion_id": "2084631773",
        "commented_code": "@@ -23,6 +28,21 @@ public static function accessible($value)\n         return is_array($value) || $value instanceof ArrayAccess;\n     }\n \n+    /**\n+     * Determine whether the given value is arrayable.\n+     *\n+     * @param  mixed  $value\n+     * @return bool\n+     */\n+    public static function arrayable($value)",
        "comment_created_at": "2025-05-12T13:28:41+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Ah, thanks for the explanation \ud83d\udc4d\ud83c\udffb ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1898695749",
    "pr_number": 54027,
    "pr_file": "src/Illuminate/Support/Number.php",
    "created_at": "2024-12-27T20:06:02+00:00",
    "commented_code": "return static::$currency;\n    }\n\n    /**\n     * Generate a random number of the given length.",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1898695749",
        "repo_full_name": "laravel/framework",
        "pr_number": 54027,
        "pr_file": "src/Illuminate/Support/Number.php",
        "discussion_id": "1898695749",
        "commented_code": "@@ -367,6 +367,30 @@ public static function defaultCurrency()\n         return static::$currency;\n     }\n \n+    /**\n+     * Generate a random number of the given length.",
        "comment_created_at": "2024-12-27T20:06:02+00:00",
        "comment_author": "shaedrich",
        "comment_body": "\"number\" might be misleading here:\r\n```suggestion\r\n     * Generate a random integer of the given length.\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1898696764",
    "pr_number": 54027,
    "pr_file": "src/Illuminate/Support/Number.php",
    "created_at": "2024-12-27T20:08:52+00:00",
    "commented_code": "return static::$currency;\n    }\n\n    /**\n     * Generate a random number of the given length.\n     *\n     * @param  int  $length\n     * @return int\n     */\n    public static function random(int $length = 6): int\n    {\n        $maxLength = strlen((string) PHP_INT_MAX);\n\n        if ($length < 1 || $length > $maxLength) {\n            return 0;\n        }\n\n        $min = 10 ** ($length - 1);\n        $max = (10 ** $length) - 1;\n\n        if ($length == $maxLength) {",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1898696764",
        "repo_full_name": "laravel/framework",
        "pr_number": 54027,
        "pr_file": "src/Illuminate/Support/Number.php",
        "discussion_id": "1898696764",
        "commented_code": "@@ -367,6 +367,30 @@ public static function defaultCurrency()\n         return static::$currency;\n     }\n \n+    /**\n+     * Generate a random number of the given length.\n+     *\n+     * @param  int  $length\n+     * @return int\n+     */\n+    public static function random(int $length = 6): int\n+    {\n+        $maxLength = strlen((string) PHP_INT_MAX);\n+\n+        if ($length < 1 || $length > $maxLength) {\n+            return 0;\n+        }\n+\n+        $min = 10 ** ($length - 1);\n+        $max = (10 ** $length) - 1;\n+\n+        if ($length == $maxLength) {",
        "comment_created_at": "2024-12-27T20:08:52+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Even though, you are using `strlen()` here, I'd say, \"digits\" is the more correct term when dealing with numbers:\r\n```suggestion\r\n     * Generate a random number with the given amount of digits.\r\n     *\r\n     * @param  int  $digits\r\n     * @return int\r\n     */\r\n    public static function random(int $digits = 6): int\r\n    {\r\n        $maxDigits = strlen((string) PHP_INT_MAX);\r\n\r\n        if ($digits < 1 || $digits > $maxDigits) {\r\n            return 0;\r\n        }\r\n\r\n        $min = 10 ** ($digits - 1);\r\n        $max = (10 ** $digits) - 1;\r\n\r\n        if ($digits == $maxDigits) {\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1900456982",
        "repo_full_name": "laravel/framework",
        "pr_number": 54027,
        "pr_file": "src/Illuminate/Support/Number.php",
        "discussion_id": "1898696764",
        "commented_code": "@@ -367,6 +367,30 @@ public static function defaultCurrency()\n         return static::$currency;\n     }\n \n+    /**\n+     * Generate a random number of the given length.\n+     *\n+     * @param  int  $length\n+     * @return int\n+     */\n+    public static function random(int $length = 6): int\n+    {\n+        $maxLength = strlen((string) PHP_INT_MAX);\n+\n+        if ($length < 1 || $length > $maxLength) {\n+            return 0;\n+        }\n+\n+        $min = 10 ** ($length - 1);\n+        $max = (10 ** $length) - 1;\n+\n+        if ($length == $maxLength) {",
        "comment_created_at": "2025-01-01T20:30:55+00:00",
        "comment_author": "dilovanmatini",
        "comment_body": "Yes, it is more readable.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1470746887",
    "pr_number": 49900,
    "pr_file": "src/Illuminate/Translation/Translator.php",
    "created_at": "2024-01-30T08:14:28+00:00",
    "commented_code": "// the translator was instantiated. Then, we can load the lines and return.\n            $locales = $fallback ? $this->localeArray($locale) : [$locale];\n\n            foreach ($locales as $locale) {\n            foreach ($locales as $_locale) {\n                if (! is_null($line = $this->getLine(\n                    $namespace, $group, $locale, $item, $replace\n                    $namespace, $group, $_locale, $item, $replace",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1470746887",
        "repo_full_name": "laravel/framework",
        "pr_number": 49900,
        "pr_file": "src/Illuminate/Translation/Translator.php",
        "discussion_id": "1470746887",
        "commented_code": "@@ -160,9 +160,9 @@ public function get($key, array $replace = [], $locale = null, $fallback = true)\n             // the translator was instantiated. Then, we can load the lines and return.\n             $locales = $fallback ? $this->localeArray($locale) : [$locale];\n \n-            foreach ($locales as $locale) {\n+            foreach ($locales as $_locale) {\n                 if (! is_null($line = $this->getLine(\n-                    $namespace, $group, $locale, $item, $replace\n+                    $namespace, $group, $_locale, $item, $replace",
        "comment_created_at": "2024-01-30T08:14:28+00:00",
        "comment_author": "driesvints",
        "comment_body": "Use `$languageLineLocale` instead here. `$_` isn't a syntax we use anywhere.",
        "pr_file_module": null
      },
      {
        "comment_id": "1470754575",
        "repo_full_name": "laravel/framework",
        "pr_number": 49900,
        "pr_file": "src/Illuminate/Translation/Translator.php",
        "discussion_id": "1470746887",
        "commented_code": "@@ -160,9 +160,9 @@ public function get($key, array $replace = [], $locale = null, $fallback = true)\n             // the translator was instantiated. Then, we can load the lines and return.\n             $locales = $fallback ? $this->localeArray($locale) : [$locale];\n \n-            foreach ($locales as $locale) {\n+            foreach ($locales as $_locale) {\n                 if (! is_null($line = $this->getLine(\n-                    $namespace, $group, $locale, $item, $replace\n+                    $namespace, $group, $_locale, $item, $replace",
        "comment_created_at": "2024-01-30T08:21:24+00:00",
        "comment_author": "VicGUTT",
        "comment_body": "Sure. I was wondering about it myself.\r\n\r\nThanks for the feedback; done in: [549de01](https://github.com/laravel/framework/pull/49900/commits/549de01ea9f7fa17b272d9baa04be0fe186b9c26)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1714804417",
    "pr_number": 52461,
    "pr_file": "src/Illuminate/Database/Eloquent/Concerns/PreventsCircularRecursion.php",
    "created_at": "2024-08-13T07:26:20+00:00",
    "commented_code": "<?php\n\nnamespace Illuminate\\Database\\Eloquent\\Concerns;\n\nuse Illuminate\\Support\\Arr;\nuse Illuminate\\Support\\Onceable;\n\ntrait PreventsCircularRecursion\n{\n    /**\n     * The cache of objects processed to prevent infinite recursion.\n     *\n     * @var \\WeakMap<static, array<string, mixed>>\n     */\n    protected static $recursionCache;\n\n    /**\n     * Get the current recursion cache being used by the model.\n     *\n     * @return \\WeakMap\n     */\n    protected static function getRecursionCache()\n    {\n        return static::$recursionCache ??= new \\WeakMap();\n    }\n\n    /**\n     * Get the current stack of methods being called recursively.\n     *\n     * @param  object  $object\n     * @return array\n     */\n    protected static function getRecursiveCallStack($object): array\n    {\n        return static::getRecursionCache()->offsetExists($object)\n            ? static::getRecursionCache()->offsetGet($object)\n            : [];\n    }\n\n    /**\n     * Prevent a method from being called multiple times on the same object within the same call stack.\n     *\n     * @param  callable  $callback\n     * @param  mixed  $default\n     * @return mixed\n     */\n    protected function once($callback, $default = null)",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1714804417",
        "repo_full_name": "laravel/framework",
        "pr_number": 52461,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/PreventsCircularRecursion.php",
        "discussion_id": "1714804417",
        "commented_code": "@@ -0,0 +1,74 @@\n+<?php\n+\n+namespace Illuminate\\Database\\Eloquent\\Concerns;\n+\n+use Illuminate\\Support\\Arr;\n+use Illuminate\\Support\\Onceable;\n+\n+trait PreventsCircularRecursion\n+{\n+    /**\n+     * The cache of objects processed to prevent infinite recursion.\n+     *\n+     * @var \\WeakMap<static, array<string, mixed>>\n+     */\n+    protected static $recursionCache;\n+\n+    /**\n+     * Get the current recursion cache being used by the model.\n+     *\n+     * @return \\WeakMap\n+     */\n+    protected static function getRecursionCache()\n+    {\n+        return static::$recursionCache ??= new \\WeakMap();\n+    }\n+\n+    /**\n+     * Get the current stack of methods being called recursively.\n+     *\n+     * @param  object  $object\n+     * @return array\n+     */\n+    protected static function getRecursiveCallStack($object): array\n+    {\n+        return static::getRecursionCache()->offsetExists($object)\n+            ? static::getRecursionCache()->offsetGet($object)\n+            : [];\n+    }\n+\n+    /**\n+     * Prevent a method from being called multiple times on the same object within the same call stack.\n+     *\n+     * @param  callable  $callback\n+     * @param  mixed  $default\n+     * @return mixed\n+     */\n+    protected function once($callback, $default = null)",
        "comment_created_at": "2024-08-13T07:26:20+00:00",
        "comment_author": "Tofandel",
        "comment_body": "I do think following laravel's pattern this should be renamed to `withoutInfiniteRecursion` or `withoutCircularRecursion`\r\n\r\nAs you've explained it has a very different behavior than the once helper and could be confusing from a readability standpoint",
        "pr_file_module": null
      },
      {
        "comment_id": "1714811116",
        "repo_full_name": "laravel/framework",
        "pr_number": 52461,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/PreventsCircularRecursion.php",
        "discussion_id": "1714804417",
        "commented_code": "@@ -0,0 +1,74 @@\n+<?php\n+\n+namespace Illuminate\\Database\\Eloquent\\Concerns;\n+\n+use Illuminate\\Support\\Arr;\n+use Illuminate\\Support\\Onceable;\n+\n+trait PreventsCircularRecursion\n+{\n+    /**\n+     * The cache of objects processed to prevent infinite recursion.\n+     *\n+     * @var \\WeakMap<static, array<string, mixed>>\n+     */\n+    protected static $recursionCache;\n+\n+    /**\n+     * Get the current recursion cache being used by the model.\n+     *\n+     * @return \\WeakMap\n+     */\n+    protected static function getRecursionCache()\n+    {\n+        return static::$recursionCache ??= new \\WeakMap();\n+    }\n+\n+    /**\n+     * Get the current stack of methods being called recursively.\n+     *\n+     * @param  object  $object\n+     * @return array\n+     */\n+    protected static function getRecursiveCallStack($object): array\n+    {\n+        return static::getRecursionCache()->offsetExists($object)\n+            ? static::getRecursionCache()->offsetGet($object)\n+            : [];\n+    }\n+\n+    /**\n+     * Prevent a method from being called multiple times on the same object within the same call stack.\n+     *\n+     * @param  callable  $callback\n+     * @param  mixed  $default\n+     * @return mixed\n+     */\n+    protected function once($callback, $default = null)",
        "comment_created_at": "2024-08-13T07:31:08+00:00",
        "comment_author": "samlev",
        "comment_body": "I had actuall named it `withoutRecursion()` originally then changed it to `once()`",
        "pr_file_module": null
      },
      {
        "comment_id": "1714829338",
        "repo_full_name": "laravel/framework",
        "pr_number": 52461,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/PreventsCircularRecursion.php",
        "discussion_id": "1714804417",
        "commented_code": "@@ -0,0 +1,74 @@\n+<?php\n+\n+namespace Illuminate\\Database\\Eloquent\\Concerns;\n+\n+use Illuminate\\Support\\Arr;\n+use Illuminate\\Support\\Onceable;\n+\n+trait PreventsCircularRecursion\n+{\n+    /**\n+     * The cache of objects processed to prevent infinite recursion.\n+     *\n+     * @var \\WeakMap<static, array<string, mixed>>\n+     */\n+    protected static $recursionCache;\n+\n+    /**\n+     * Get the current recursion cache being used by the model.\n+     *\n+     * @return \\WeakMap\n+     */\n+    protected static function getRecursionCache()\n+    {\n+        return static::$recursionCache ??= new \\WeakMap();\n+    }\n+\n+    /**\n+     * Get the current stack of methods being called recursively.\n+     *\n+     * @param  object  $object\n+     * @return array\n+     */\n+    protected static function getRecursiveCallStack($object): array\n+    {\n+        return static::getRecursionCache()->offsetExists($object)\n+            ? static::getRecursionCache()->offsetGet($object)\n+            : [];\n+    }\n+\n+    /**\n+     * Prevent a method from being called multiple times on the same object within the same call stack.\n+     *\n+     * @param  callable  $callback\n+     * @param  mixed  $default\n+     * @return mixed\n+     */\n+    protected function once($callback, $default = null)",
        "comment_created_at": "2024-08-13T07:44:44+00:00",
        "comment_author": "Tofandel",
        "comment_body": "That also works, as long as it makes the code more readable in `Model` so you can understand without having to take a look inside the function",
        "pr_file_module": null
      },
      {
        "comment_id": "1715001879",
        "repo_full_name": "laravel/framework",
        "pr_number": 52461,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/PreventsCircularRecursion.php",
        "discussion_id": "1714804417",
        "commented_code": "@@ -0,0 +1,74 @@\n+<?php\n+\n+namespace Illuminate\\Database\\Eloquent\\Concerns;\n+\n+use Illuminate\\Support\\Arr;\n+use Illuminate\\Support\\Onceable;\n+\n+trait PreventsCircularRecursion\n+{\n+    /**\n+     * The cache of objects processed to prevent infinite recursion.\n+     *\n+     * @var \\WeakMap<static, array<string, mixed>>\n+     */\n+    protected static $recursionCache;\n+\n+    /**\n+     * Get the current recursion cache being used by the model.\n+     *\n+     * @return \\WeakMap\n+     */\n+    protected static function getRecursionCache()\n+    {\n+        return static::$recursionCache ??= new \\WeakMap();\n+    }\n+\n+    /**\n+     * Get the current stack of methods being called recursively.\n+     *\n+     * @param  object  $object\n+     * @return array\n+     */\n+    protected static function getRecursiveCallStack($object): array\n+    {\n+        return static::getRecursionCache()->offsetExists($object)\n+            ? static::getRecursionCache()->offsetGet($object)\n+            : [];\n+    }\n+\n+    /**\n+     * Prevent a method from being called multiple times on the same object within the same call stack.\n+     *\n+     * @param  callable  $callback\n+     * @param  mixed  $default\n+     * @return mixed\n+     */\n+    protected function once($callback, $default = null)",
        "comment_created_at": "2024-08-13T09:44:11+00:00",
        "comment_author": "samlev",
        "comment_body": "I've updated this back to `withoutRecursion()`",
        "pr_file_module": null
      }
    ]
  }
]
