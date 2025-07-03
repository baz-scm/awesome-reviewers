---
title: Explicit null handling
description: 'Use explicit identity comparisons for null checks and leverage modern
  PHP null-handling features to create more reliable, readable code.


  ## Key practices:'
repository: laravel/framework
label: Null Handling
language: PHP
comments_count: 9
repository_stars: 33763
---

Use explicit identity comparisons for null checks and leverage modern PHP null-handling features to create more reliable, readable code.

## Key practices:

### 1. Use identity operators for null checks instead of functions

```php
// Avoid
if (is_null($value)) { ... }
if (empty($path)) { ... }

// Prefer
if ($value === null) { ... }
if ($path === '') { ... }
if ($array === []) { ... }
```

Identity comparisons (`===`, `!==`) are more precise than functions like `is_null()` or `empty()`. They clearly communicate your intent and avoid unexpected behavior with falsy values like `'0'` or `0`.

### 2. Leverage null coalescing operators

```php
// Avoid
$name = (string) (is_null($this->argument('name')) 
    ? $choice 
    : $this->argument('name'));

// Prefer
$name = (string) ($this->argument('name') ?? $choice);
```

The null coalescing operator (`??`) simplifies conditional logic and makes your code more concise and readable.

### 3. Add proper null annotations in docblocks and types

```php
// Avoid
/** @param string $string The input string to sanitize. */
public static function sanitize($string) 
{
    if ($string === null) {
        return null;
    }
}

// Prefer
/** @param string|null $string The input string to sanitize. */
/** @return string|null The sanitized string. */
public static function sanitize(?string $string) 
{
    if ($string === null) {
        return null;
    }
}
```

Accurately document nullable parameters and return types for better static analysis and IDE support.

### 4. Check for null before method calls

```php
// Avoid direct method calls on possibly null values
$using($this->app);

// Prefer
if ($using !== null) {
    $this->app->call($using);
}
```

Always check if variables are null before calling methods on them to prevent null reference exceptions.

### 5. Be careful with null in array and object relationships

```php
// Check if a relation exists before accessing properties
if (isset($relation)) {
    $attributes[$key] = $relation;
}
```

Remember that `isset()` returns false for null values, which may not be what you expect when working with relationships or arrays that might legitimately contain null values.


[
  {
    "discussion_id": "2072707142",
    "pr_number": 55645,
    "pr_file": "src/Illuminate/Container/Container.php",
    "created_at": "2025-05-04T20:43:00+00:00",
    "commented_code": "array_pop($this->buildStack);\n\n        if (!empty($reflector->getAttributes(Lazy::class))) {",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2072707142",
        "repo_full_name": "laravel/framework",
        "pr_number": 55645,
        "pr_file": "src/Illuminate/Container/Container.php",
        "discussion_id": "2072707142",
        "commented_code": "@@ -1058,8 +1059,16 @@ public function build($concrete)\n \n         array_pop($this->buildStack);\n \n+        if (!empty($reflector->getAttributes(Lazy::class))) {",
        "comment_created_at": "2025-05-04T20:43:00+00:00",
        "comment_author": "shaedrich",
        "comment_body": "You could just directly check this\r\n```suggestion\r\n        if ($reflector->getAttributes(Lazy::class) !== []) {\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2073825274",
        "repo_full_name": "laravel/framework",
        "pr_number": 55645,
        "pr_file": "src/Illuminate/Container/Container.php",
        "discussion_id": "2072707142",
        "commented_code": "@@ -1058,8 +1059,16 @@ public function build($concrete)\n \n         array_pop($this->buildStack);\n \n+        if (!empty($reflector->getAttributes(Lazy::class))) {",
        "comment_created_at": "2025-05-05T17:04:20+00:00",
        "comment_author": "olekjs",
        "comment_body": "Does this change bring anything beyond syntax? I\u2019m just asking out of curiosity.",
        "pr_file_module": null
      },
      {
        "comment_id": "2073872455",
        "repo_full_name": "laravel/framework",
        "pr_number": 55645,
        "pr_file": "src/Illuminate/Container/Container.php",
        "discussion_id": "2072707142",
        "commented_code": "@@ -1058,8 +1059,16 @@ public function build($concrete)\n \n         array_pop($this->buildStack);\n \n+        if (!empty($reflector->getAttributes(Lazy::class))) {",
        "comment_created_at": "2025-05-05T17:32:05+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Not much. Technically, a function call is more expensive than a comparison, but this should mostly be optimized away in practice. One _slight_ advantage would be a clear communication that we are working with an array here and don't have to check _any_ structure's emptiness.",
        "pr_file_module": null
      },
      {
        "comment_id": "2078948392",
        "repo_full_name": "laravel/framework",
        "pr_number": 55645,
        "pr_file": "src/Illuminate/Container/Container.php",
        "discussion_id": "2072707142",
        "commented_code": "@@ -1058,8 +1059,16 @@ public function build($concrete)\n \n         array_pop($this->buildStack);\n \n+        if (!empty($reflector->getAttributes(Lazy::class))) {",
        "comment_created_at": "2025-05-08T06:03:12+00:00",
        "comment_author": "macropay-solutions",
        "comment_body": "@olekjs empty function is a trap for future bugs.\r\nWe have a rule in place to never use empty function because of that. \r\n\r\nempty('0') is true for example.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2111059728",
    "pr_number": 55877,
    "pr_file": "src/Illuminate/Foundation/Console/ConfigPublishCommand.php",
    "created_at": "2025-05-28T06:45:12+00:00",
    "commented_code": "return;\n        }\n\n        $name = (string) (is_null($this->argument('name')) ? select(\n            label: 'Which configuration file would you like to publish?',\n            options: (new Collection($config))->map(function (string $path) {\n                return basename($path, '.php');\n            }),\n        ) : $this->argument('name'));\n        $choices = array_map(\n            fn (string $path) => basename($path, '.php'),\n            $config,\n        );\n\n        $choice = windows_os()\n            ? select(\n                'Which configuration file would you like to publish?',\n                $choices,\n                scroll: 15,\n            )\n            : search(\n                label: 'Which configuration file would you like to publish?',\n                placeholder: 'Search...',\n                options: fn ($search) => array_values(array_filter(\n                    $choices,\n                    fn ($choice) => str_contains(strtolower($choice), strtolower($search))\n                )),\n                scroll: 15,\n            );\n\n        $name = (string) (is_null($this->argument('name'))\n            ? $choice\n            : $this->argument('name'));",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2111059728",
        "repo_full_name": "laravel/framework",
        "pr_number": 55877,
        "pr_file": "src/Illuminate/Foundation/Console/ConfigPublishCommand.php",
        "discussion_id": "2111059728",
        "commented_code": "@@ -46,12 +47,30 @@ public function handle()\n             return;\n         }\n \n-        $name = (string) (is_null($this->argument('name')) ? select(\n-            label: 'Which configuration file would you like to publish?',\n-            options: (new Collection($config))->map(function (string $path) {\n-                return basename($path, '.php');\n-            }),\n-        ) : $this->argument('name'));\n+        $choices = array_map(\n+            fn (string $path) => basename($path, '.php'),\n+            $config,\n+        );\n+\n+        $choice = windows_os()\n+            ? select(\n+                'Which configuration file would you like to publish?',\n+                $choices,\n+                scroll: 15,\n+            )\n+            : search(\n+                label: 'Which configuration file would you like to publish?',\n+                placeholder: 'Search...',\n+                options: fn ($search) => array_values(array_filter(\n+                    $choices,\n+                    fn ($choice) => str_contains(strtolower($choice), strtolower($search))\n+                )),\n+                scroll: 15,\n+            );\n+\n+        $name = (string) (is_null($this->argument('name'))\n+            ? $choice\n+            : $this->argument('name'));",
        "comment_created_at": "2025-05-28T06:45:12+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Wouldn't this suffice?\r\n```suggestion\r\n        $name = (string) ($this->argument('name') ?? $choice);\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2102660306",
    "pr_number": 55810,
    "pr_file": "src/Illuminate/Filesystem/FilesystemAdapter.php",
    "created_at": "2025-05-22T14:05:37+00:00",
    "commented_code": "*/\n    protected function concatPathToUrl($url, $path)\n    {\n        if (empty($url) || empty($path)) {",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2102660306",
        "repo_full_name": "laravel/framework",
        "pr_number": 55810,
        "pr_file": "src/Illuminate/Filesystem/FilesystemAdapter.php",
        "discussion_id": "2102660306",
        "commented_code": "@@ -847,6 +847,10 @@ public function temporaryUploadUrl($path, $expiration, array $options = [])\n      */\n     protected function concatPathToUrl($url, $path)\n     {\n+        if (empty($url) || empty($path)) {",
        "comment_created_at": "2025-05-22T14:05:37+00:00",
        "comment_author": "GrahamCampbell",
        "comment_body": "Empty is the wrong function here. It does not check if the variable us the empty string, it checks if it looks like an enmpty-ish value, inc if it's 0. One should compare against `''` instead.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2090368477",
    "pr_number": 55740,
    "pr_file": "src/Illuminate/Foundation/Configuration/ApplicationBuilder.php",
    "created_at": "2025-05-15T06:23:18+00:00",
    "commented_code": "string $apiPrefix = 'api',\n        ?callable $then = null)\n    {\n        if (is_null($using) && (is_string($web) || is_array($web) || is_string($api) || is_array($api) || is_string($pages) || is_string($health)) || is_callable($then)) {\n            $using = $this->buildRoutingCallback($web, $api, $pages, $health, $apiPrefix, $then);\n        if (is_null($using) && (is_string($web) || is_array($web) || is_string($api) || is_array($api) || is_string($pages)) || is_callable($then)) {\n            $using = $this->buildRoutingCallback($web, $api, $pages, $apiPrefix, $then);\n        }\n\n            if (is_string($health)) {\n                PreventRequestsDuringMaintenance::except($health);\n            }\n        if (is_string($health)) {\n            $using = function () use ($health, $using) {\n                $this->buildHealthCheckRoute($health);\n                call_user_func($using, $this->app);",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2090368477",
        "repo_full_name": "laravel/framework",
        "pr_number": 55740,
        "pr_file": "src/Illuminate/Foundation/Configuration/ApplicationBuilder.php",
        "discussion_id": "2090368477",
        "commented_code": "@@ -159,12 +159,17 @@ public function withRouting(?Closure $using = null,\n         string $apiPrefix = 'api',\n         ?callable $then = null)\n     {\n-        if (is_null($using) && (is_string($web) || is_array($web) || is_string($api) || is_array($api) || is_string($pages) || is_string($health)) || is_callable($then)) {\n-            $using = $this->buildRoutingCallback($web, $api, $pages, $health, $apiPrefix, $then);\n+        if (is_null($using) && (is_string($web) || is_array($web) || is_string($api) || is_array($api) || is_string($pages)) || is_callable($then)) {\n+            $using = $this->buildRoutingCallback($web, $api, $pages, $apiPrefix, $then);\n+        }\n \n-            if (is_string($health)) {\n-                PreventRequestsDuringMaintenance::except($health);\n-            }\n+        if (is_string($health)) {\n+            $using = function () use ($health, $using) {\n+                $this->buildHealthCheckRoute($health);\n+                call_user_func($using, $this->app);",
        "comment_created_at": "2025-05-15T06:23:18+00:00",
        "comment_author": "rodrigopedra",
        "comment_body": "This line should be:\r\n\r\n```php\r\n$this->app->call($using);\r\n```\r\n\r\nTo preserve the current behavior, as in:\r\n\r\nhttps://github.com/laravel/framework/blob/df12a087731b37708cfbba72172a4c381363fed2/src/Illuminate/Foundation/Support/Providers/RouteServiceProvider.php#L162",
        "pr_file_module": null
      },
      {
        "comment_id": "2090370825",
        "repo_full_name": "laravel/framework",
        "pr_number": 55740,
        "pr_file": "src/Illuminate/Foundation/Configuration/ApplicationBuilder.php",
        "discussion_id": "2090368477",
        "commented_code": "@@ -159,12 +159,17 @@ public function withRouting(?Closure $using = null,\n         string $apiPrefix = 'api',\n         ?callable $then = null)\n     {\n-        if (is_null($using) && (is_string($web) || is_array($web) || is_string($api) || is_array($api) || is_string($pages) || is_string($health)) || is_callable($then)) {\n-            $using = $this->buildRoutingCallback($web, $api, $pages, $health, $apiPrefix, $then);\n+        if (is_null($using) && (is_string($web) || is_array($web) || is_string($api) || is_array($api) || is_string($pages)) || is_callable($then)) {\n+            $using = $this->buildRoutingCallback($web, $api, $pages, $apiPrefix, $then);\n+        }\n \n-            if (is_string($health)) {\n-                PreventRequestsDuringMaintenance::except($health);\n-            }\n+        if (is_string($health)) {\n+            $using = function () use ($health, $using) {\n+                $this->buildHealthCheckRoute($health);\n+                call_user_func($using, $this->app);",
        "comment_created_at": "2025-05-15T06:25:02+00:00",
        "comment_author": "rodrigopedra",
        "comment_body": "Also, `$using` in this point, can be `null`. A check for that should be added.\r\n\r\nAn app can be built without specifying no routes, by just providing the `$commands` and/or the `$channels` parameters.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1953114524",
    "pr_number": 54582,
    "pr_file": "src/Illuminate/View/Compilers/BladeCompiler.php",
    "created_at": "2025-02-12T17:32:47+00:00",
    "commented_code": "if (is_null($alias)) {",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1953114524",
        "repo_full_name": "laravel/framework",
        "pr_number": 54582,
        "pr_file": "src/Illuminate/View/Compilers/BladeCompiler.php",
        "discussion_id": "1953114524",
        "commented_code": "@@ -762,14 +768,14 @@ public function component($class, $alias = null, $prefix = '')\n \n         if (is_null($alias)) {",
        "comment_created_at": "2025-02-12T17:32:47+00:00",
        "comment_author": "shaedrich",
        "comment_body": "You can avoid the function call like this:\r\n```suggestion\r\n        if ($alias === null) {\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1923809576",
    "pr_number": 54285,
    "pr_file": "src/Illuminate/Support/Str.php",
    "created_at": "2025-01-21T14:16:17+00:00",
    "commented_code": "static::$camelCache = [];\n        static::$studlyCache = [];\n    }\n\n    /**\n     * Sanitize the given string.\n     *\n     *\n     * See: https://symfony.com/doc/current/html_sanitizer.html\n     *\n     * @param  string  $string  The input string to sanitize.\n     * @param  HtmlSanitizerConfig|null  $config  Custom configuration to use for sanitizing.\n     * @return string The sanitized string.\n     */\n    public static function sanitize($string, ?HtmlSanitizerConfig $config = null)\n    {\n        if (is_null($string)) {",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1923809576",
        "repo_full_name": "laravel/framework",
        "pr_number": 54285,
        "pr_file": "src/Illuminate/Support/Str.php",
        "discussion_id": "1923809576",
        "commented_code": "@@ -2014,4 +2016,28 @@ public static function flushCache()\n         static::$camelCache = [];\n         static::$studlyCache = [];\n     }\n+\n+    /**\n+     * Sanitize the given string.\n+     *\n+     *\n+     * See: https://symfony.com/doc/current/html_sanitizer.html\n+     *\n+     * @param  string  $string  The input string to sanitize.\n+     * @param  HtmlSanitizerConfig|null  $config  Custom configuration to use for sanitizing.\n+     * @return string The sanitized string.\n+     */\n+    public static function sanitize($string, ?HtmlSanitizerConfig $config = null)\n+    {\n+        if (is_null($string)) {",
        "comment_created_at": "2025-01-21T14:16:17+00:00",
        "comment_author": "shaedrich",
        "comment_body": "According to your `is_null()` call, your string can be `null`. This should be reflected in the PHPDoc comment type as well:\r\n```suggestion\r\n     * @param  string|null  $string  The input string to sanitize.\r\n     * @param  HtmlSanitizerConfig|null  $config  Custom configuration to use for sanitizing.\r\n     * @return string The sanitized string.\r\n     */\r\n    public static function sanitize($string, ?HtmlSanitizerConfig $config = null)\r\n    {\r\n        if ($string === null) {\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1923810842",
    "pr_number": 54285,
    "pr_file": "src/Illuminate/Support/Str.php",
    "created_at": "2025-01-21T14:17:05+00:00",
    "commented_code": "static::$camelCache = [];\n        static::$studlyCache = [];\n    }\n\n    /**\n     * Sanitize the given string.\n     *\n     *\n     * See: https://symfony.com/doc/current/html_sanitizer.html\n     *\n     * @param  string  $string  The input string to sanitize.\n     * @param  HtmlSanitizerConfig|null  $config  Custom configuration to use for sanitizing.\n     * @return string The sanitized string.\n     */\n    public static function sanitize($string, ?HtmlSanitizerConfig $config = null)\n    {\n        if (is_null($string)) {\n            return null;",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1923810842",
        "repo_full_name": "laravel/framework",
        "pr_number": 54285,
        "pr_file": "src/Illuminate/Support/Str.php",
        "discussion_id": "1923810842",
        "commented_code": "@@ -2014,4 +2016,28 @@ public static function flushCache()\n         static::$camelCache = [];\n         static::$studlyCache = [];\n     }\n+\n+    /**\n+     * Sanitize the given string.\n+     *\n+     *\n+     * See: https://symfony.com/doc/current/html_sanitizer.html\n+     *\n+     * @param  string  $string  The input string to sanitize.\n+     * @param  HtmlSanitizerConfig|null  $config  Custom configuration to use for sanitizing.\n+     * @return string The sanitized string.\n+     */\n+    public static function sanitize($string, ?HtmlSanitizerConfig $config = null)\n+    {\n+        if (is_null($string)) {\n+            return null;",
        "comment_created_at": "2025-01-21T14:17:05+00:00",
        "comment_author": "shaedrich",
        "comment_body": "According to your `is_null()` call, the method can return `null`. This should be reflected in the PHPDoc comment type as well:\r\n```suggestion\r\n     * @return string|null The sanitized string.\r\n     */\r\n    public static function sanitize($string, ?HtmlSanitizerConfig $config = null)\r\n    {\r\n        if (is_null($string)) {\r\n            return null;\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1884704097",
    "pr_number": 53872,
    "pr_file": "src/Illuminate/Http/Response.php",
    "created_at": "2024-12-14T01:28:04+00:00",
    "commented_code": "return $this;\n    }\n\n    /**\n     * Gets the current response content.\n     */\n    #[\\Override]\n    public function getContent(): string|false\n    {\n        return transform(parent::getContent(), fn ($content) => $content, '');",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1884704097",
        "repo_full_name": "laravel/framework",
        "pr_number": 53872,
        "pr_file": "src/Illuminate/Http/Response.php",
        "discussion_id": "1884704097",
        "commented_code": "@@ -75,6 +75,15 @@ public function setContent(mixed $content): static\n         return $this;\n     }\n \n+    /**\n+     * Gets the current response content.\n+     */\n+    #[\\Override]\n+    public function getContent(): string|false\n+    {\n+        return transform(parent::getContent(), fn ($content) => $content, '');",
        "comment_created_at": "2024-12-14T01:28:04+00:00",
        "comment_author": "rodrigopedra",
        "comment_body": "Why not just?\r\n\r\n```php\r\nreturn parent::getContent() ?? '';\r\n```\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1689591772",
    "pr_number": 51956,
    "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
    "created_at": "2024-07-24T11:15:45+00:00",
    "commented_code": "// If the relation value has been set, we will set it on this attributes\n            // list for returning. If it was not arrayable or null, we'll not set\n            // the value on the array because it is some type of invalid value.\n            if (isset($relation) || is_null($value)) {\n            if (isset($relation)) {",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1689591772",
        "repo_full_name": "laravel/framework",
        "pr_number": 51956,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1689591772",
        "commented_code": "@@ -394,7 +394,7 @@ public function relationsToArray()\n             // If the relation value has been set, we will set it on this attributes\n             // list for returning. If it was not arrayable or null, we'll not set\n             // the value on the array because it is some type of invalid value.\n-            if (isset($relation) || is_null($value)) {\n+            if (isset($relation)) {",
        "comment_created_at": "2024-07-24T11:15:45+00:00",
        "comment_author": "pxpm",
        "comment_body": "Doesn't this change the behavior? `null` values should enter the condition. Removing the `|| is_null()` they will not enter anymore as the `isset()` without the `is_null()` check would exclude them. \r\n\r\n```php\r\n$relation, $value = null;\r\n\r\nif (isset($relation)) {\r\n// we don't reach this code\r\n}\r\n\r\nif (isset($relation) || is_null($value)) {\r\n// this code is executed\r\n}\r\n```\r\nIf this is some kind of bug fixing it shouldn't be part of this PR IMO. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1689784138",
        "repo_full_name": "laravel/framework",
        "pr_number": 51956,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1689591772",
        "commented_code": "@@ -394,7 +394,7 @@ public function relationsToArray()\n             // If the relation value has been set, we will set it on this attributes\n             // list for returning. If it was not arrayable or null, we'll not set\n             // the value on the array because it is some type of invalid value.\n-            if (isset($relation) || is_null($value)) {\n+            if (isset($relation)) {",
        "comment_created_at": "2024-07-24T13:16:01+00:00",
        "comment_author": "calebdw",
        "comment_body": "This yielded the following error:\r\n\r\n```\r\n ------ ------------------------------------------------------------------------------------------------------------------ \r\n  Line   Illuminate/Database/Eloquent/Concerns/HasAttributes.php (in context of class Illuminate\\Database\\Eloquent\\Model)  \r\n ------ ------------------------------------------------------------------------------------------------------------------ \r\n  398    Variable $relation might not be defined.                                                                          \r\n         \ud83e\udeaa  variable.undefined         \r\n```\r\n\r\nThe `is_null($value)` is already checked above:\r\n\r\nhttps://github.com/laravel/framework/blob/46297e441252d495713fb30223ffcfb325a4f120/src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php#L380-L385\r\n\r\nAnd you'll notice that `$value` is not referenced inside the `if` body and therefore should not be referenced inside the condition. The only thing that matters is checking that the `$relation` isset before assigning it.",
        "pr_file_module": null
      },
      {
        "comment_id": "1689815593",
        "repo_full_name": "laravel/framework",
        "pr_number": 51956,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1689591772",
        "commented_code": "@@ -394,7 +394,7 @@ public function relationsToArray()\n             // If the relation value has been set, we will set it on this attributes\n             // list for returning. If it was not arrayable or null, we'll not set\n             // the value on the array because it is some type of invalid value.\n-            if (isset($relation) || is_null($value)) {\n+            if (isset($relation)) {",
        "comment_created_at": "2024-07-24T13:31:40+00:00",
        "comment_author": "pxpm",
        "comment_body": "Hey @calebdw I think we are talking different things here. \r\n\r\nThe first check for `is_null($value)` just sets the `$relation` value to `null`. The check you removed sets `$attributes[$key] = $relation;` when `$value = null **OR** isset($relation)`. \r\n\r\nThe fact that `$value` is not used inside the if, does not mean you can remove it from the condition as that would turn up not setting `$attributes[$key] = null` like was previously done. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1689824977",
        "repo_full_name": "laravel/framework",
        "pr_number": 51956,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1689591772",
        "commented_code": "@@ -394,7 +394,7 @@ public function relationsToArray()\n             // If the relation value has been set, we will set it on this attributes\n             // list for returning. If it was not arrayable or null, we'll not set\n             // the value on the array because it is some type of invalid value.\n-            if (isset($relation) || is_null($value)) {\n+            if (isset($relation)) {",
        "comment_created_at": "2024-07-24T13:36:20+00:00",
        "comment_author": "calebdw",
        "comment_body": "If `$value === null`, then `$relation` isset.",
        "pr_file_module": null
      },
      {
        "comment_id": "1689830616",
        "repo_full_name": "laravel/framework",
        "pr_number": 51956,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1689591772",
        "commented_code": "@@ -394,7 +394,7 @@ public function relationsToArray()\n             // If the relation value has been set, we will set it on this attributes\n             // list for returning. If it was not arrayable or null, we'll not set\n             // the value on the array because it is some type of invalid value.\n-            if (isset($relation) || is_null($value)) {\n+            if (isset($relation)) {",
        "comment_created_at": "2024-07-24T13:39:03+00:00",
        "comment_author": "calebdw",
        "comment_body": "Hmm, apparently there's some idiosyncrasies with [isset](https://www.php.net/manual/en/function.isset.php):\r\n\r\n> Determine if a variable is considered set, this means if a variable is declared and is different than [null](https://www.php.net/manual/en/reserved.constants.php#constant.null). ",
        "pr_file_module": null
      },
      {
        "comment_id": "1689855018",
        "repo_full_name": "laravel/framework",
        "pr_number": 51956,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1689591772",
        "commented_code": "@@ -394,7 +394,7 @@ public function relationsToArray()\n             // If the relation value has been set, we will set it on this attributes\n             // list for returning. If it was not arrayable or null, we'll not set\n             // the value on the array because it is some type of invalid value.\n-            if (isset($relation) || is_null($value)) {\n+            if (isset($relation)) {",
        "comment_created_at": "2024-07-24T13:51:01+00:00",
        "comment_author": "pxpm",
        "comment_body": "Indeed @calebdw that was the issue with your reasoning, as you were considering `$relation` set when it's `null`. \ud83d\udc4d ",
        "pr_file_module": null
      },
      {
        "comment_id": "1689893235",
        "repo_full_name": "laravel/framework",
        "pr_number": 51956,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1689591772",
        "commented_code": "@@ -394,7 +394,7 @@ public function relationsToArray()\n             // If the relation value has been set, we will set it on this attributes\n             // list for returning. If it was not arrayable or null, we'll not set\n             // the value on the array because it is some type of invalid value.\n-            if (isset($relation) || is_null($value)) {\n+            if (isset($relation)) {",
        "comment_created_at": "2024-07-24T14:09:10+00:00",
        "comment_author": "calebdw",
        "comment_body": "It turns out there's not a straightforward way in PHP to check if a variable isset / declared (null values being acceptable). Even using `isset($relation) || is_null($relation)` fails because `is_null` returns true when the variable does not exist :roll_eyes: .\r\n\r\nThanks for pointing this out! I also added a test since this is rather tricky",
        "pr_file_module": null
      },
      {
        "comment_id": "1689940559",
        "repo_full_name": "laravel/framework",
        "pr_number": 51956,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1689591772",
        "commented_code": "@@ -394,7 +394,7 @@ public function relationsToArray()\n             // If the relation value has been set, we will set it on this attributes\n             // list for returning. If it was not arrayable or null, we'll not set\n             // the value on the array because it is some type of invalid value.\n-            if (isset($relation) || is_null($value)) {\n+            if (isset($relation)) {",
        "comment_created_at": "2024-07-24T14:37:04+00:00",
        "comment_author": "pxpm",
        "comment_body": "Well, theoretically you can do a `get_defined_vars()` and a `array_key_exists()` to check if a variable is actually defined disregarding it's value: \r\n\r\n```php\r\n$test = null;\r\n\r\nisset($test); // return false\r\narray_key_exists('test', get_defined_vars()); // return true\r\n```\r\n\r\nNote that `get_defined_vars()` gets the variables depending on the scope it's called. https://www.php.net/manual/en/function.get-defined-vars.php\r\n\r\nCheers",
        "pr_file_module": null
      },
      {
        "comment_id": "1689947777",
        "repo_full_name": "laravel/framework",
        "pr_number": 51956,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1689591772",
        "commented_code": "@@ -394,7 +394,7 @@ public function relationsToArray()\n             // If the relation value has been set, we will set it on this attributes\n             // list for returning. If it was not arrayable or null, we'll not set\n             // the value on the array because it is some type of invalid value.\n-            if (isset($relation) || is_null($value)) {\n+            if (isset($relation)) {",
        "comment_created_at": "2024-07-24T14:41:33+00:00",
        "comment_author": "calebdw",
        "comment_body": "Yes, I considered that, however, phpstan doesn't recognize that the `$relation` is defined inside the `if` so you'd still need an `@phpstan-ignore` call",
        "pr_file_module": null
      },
      {
        "comment_id": "1689967349",
        "repo_full_name": "laravel/framework",
        "pr_number": 51956,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1689591772",
        "commented_code": "@@ -394,7 +394,7 @@ public function relationsToArray()\n             // If the relation value has been set, we will set it on this attributes\n             // list for returning. If it was not arrayable or null, we'll not set\n             // the value on the array because it is some type of invalid value.\n-            if (isset($relation) || is_null($value)) {\n+            if (isset($relation)) {",
        "comment_created_at": "2024-07-24T14:53:35+00:00",
        "comment_author": "pxpm",
        "comment_body": "You can probably use `$relation ?? null` to avoid the phpstan error ?",
        "pr_file_module": null
      }
    ]
  }
]
