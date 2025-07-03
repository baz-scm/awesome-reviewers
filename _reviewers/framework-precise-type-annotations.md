---
title: Precise type annotations
description: 'Always use the most specific and accurate type information possible
  in PHPDoc comments to improve static analysis, IDE autocompletion, and code clarity.
  Pay special attention to array types using appropriate syntax:'
repository: laravel/framework
label: Documentation
language: PHP
comments_count: 8
repository_stars: 33763
---

Always use the most specific and accurate type information possible in PHPDoc comments to improve static analysis, IDE autocompletion, and code clarity. Pay special attention to array types using appropriate syntax:

- For associative arrays with string keys: `array<string, mixed>` instead of just `array`
- For arrays of strings: `string[]` rather than generic `array`
- For complex generics: maintain template type parameters like `Collection<int, TPivotModel>`
- For method parameters accepting string or array of strings: `string|string[]` instead of `string|array`

Include full namespaces in type references (e.g., `\Illuminate\Support\Collection` instead of just `Collection`).

When documenting specialized types, use appropriate annotations:
```php
/**
 * Get JSON casting flags for the specified attribute.
 *
 * @param  string  $key
 * @return int-mask-of<JSON_*>
 */
protected function getJsonCastingFlags($key)
```

Precise type annotations help both developers and tools understand your code better, reducing potential errors and improving maintainability.


[
  {
    "discussion_id": "2144424524",
    "pr_number": 56028,
    "pr_file": "src/Illuminate/Cache/MemoizedStore.php",
    "created_at": "2025-06-13T07:53:41+00:00",
    "commented_code": "/**\n     * Store multiple items in the cache for a given number of seconds.\n     *\n     * @param  array  $values",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2144424524",
        "repo_full_name": "laravel/framework",
        "pr_number": 56028,
        "pr_file": "src/Illuminate/Cache/MemoizedStore.php",
        "discussion_id": "2144424524",
        "commented_code": "@@ -108,6 +108,7 @@ public function put($key, $value, $seconds)\n     /**\n      * Store multiple items in the cache for a given number of seconds.\n      *\n+     * @param  array  $values",
        "comment_created_at": "2025-06-13T07:53:41+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Since `prefix()` expects a `string`, so this can be reflected here:\r\n```suggestion\r\n     * @param  array<string, mixed>  $values\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2102803004",
    "pr_number": 55821,
    "pr_file": "src/Illuminate/Support/Str.php",
    "created_at": "2025-05-22T15:08:00+00:00",
    "commented_code": "static::$camelCache = [];\n        static::$studlyCache = [];\n    }\n\n    /**\n     * Split a string by a given separator.\n     *\n     * @param  string  $separator\n     * @param  string  $string\n     * @param  int  $limit\n     * @return array",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2102803004",
        "repo_full_name": "laravel/framework",
        "pr_number": 55821,
        "pr_file": "src/Illuminate/Support/Str.php",
        "discussion_id": "2102803004",
        "commented_code": "@@ -2083,4 +2083,17 @@ public static function flushCache()\n         static::$camelCache = [];\n         static::$studlyCache = [];\n     }\n+\n+    /**\n+     * Split a string by a given separator.\n+     *\n+     * @param  string  $separator\n+     * @param  string  $string\n+     * @param  int  $limit\n+     * @return array",
        "comment_created_at": "2025-05-22T15:08:00+00:00",
        "comment_author": "shaedrich",
        "comment_body": "The `array` will either consist of strings or be empty, so we can narrow this further as well:\r\n```suggestion\r\n     * @return string[]\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2102806447",
        "repo_full_name": "laravel/framework",
        "pr_number": 55821,
        "pr_file": "src/Illuminate/Support/Str.php",
        "discussion_id": "2102803004",
        "commented_code": "@@ -2083,4 +2083,17 @@ public static function flushCache()\n         static::$camelCache = [];\n         static::$studlyCache = [];\n     }\n+\n+    /**\n+     * Split a string by a given separator.\n+     *\n+     * @param  string  $separator\n+     * @param  string  $string\n+     * @param  int  $limit\n+     * @return array",
        "comment_created_at": "2025-05-22T15:09:35+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Ah, damn, sorry, hadn't submitted it and didn't see that it was closed when I hit the 'submit' button an hour later \ud83d\ude05",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2085688431",
    "pr_number": 55721,
    "pr_file": "src/Illuminate/Database/Eloquent/Relations/MorphToMany.php",
    "created_at": "2025-05-12T23:36:35+00:00",
    "commented_code": "}\n\n    /**\n     * Get the pivot models that are currently attached.\n     * Get the pivot models that are currently attached, filtered by related model keys.\n     *\n     * @return \\Illuminate\\Support\\Collection<int, TPivotModel>\n     * @param  mixed  $ids\n     * @return \\Illuminate\\Support\\Collection",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2085688431",
        "repo_full_name": "laravel/framework",
        "pr_number": 55721,
        "pr_file": "src/Illuminate/Database/Eloquent/Relations/MorphToMany.php",
        "discussion_id": "2085688431",
        "commented_code": "@@ -121,13 +121,14 @@ public function getRelationExistenceQuery(Builder $query, Builder $parentQuery,\n     }\n \n     /**\n-     * Get the pivot models that are currently attached.\n+     * Get the pivot models that are currently attached, filtered by related model keys.\n      *\n-     * @return \\Illuminate\\Support\\Collection<int, TPivotModel>\n+     * @param  mixed  $ids\n+     * @return \\Illuminate\\Support\\Collection",
        "comment_created_at": "2025-05-12T23:36:35+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Shouldn't this stay\r\n```suggestion\r\n     * @return \\Illuminate\\Support\\Collection<int, TPivotModel>\r\n```\r\n? If there is trouble with static analysis, the [PHPDoc comment in `InteractsWithPivotTable`](https://github.com/laravel/framework/blob/12.x/src/Illuminate/Database/Eloquent/Relations/Concerns/InteractsWithPivotTable.php#L496) should be adjusted accordingly",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2077010982",
    "pr_number": 55663,
    "pr_file": "src/Illuminate/Database/Query/Builder.php",
    "created_at": "2025-05-07T07:45:32+00:00",
    "commented_code": "/**\n     * Set the columns to be selected.\n     *\n     * @param  array|mixed  $columns\n     * @param  array<mixed>|mixed  $columns",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2077010982",
        "repo_full_name": "laravel/framework",
        "pr_number": 55663,
        "pr_file": "src/Illuminate/Database/Query/Builder.php",
        "discussion_id": "2077010982",
        "commented_code": "@@ -278,7 +278,7 @@ public function __construct(\n     /**\n      * Set the columns to be selected.\n      *\n-     * @param  array|mixed  $columns\n+     * @param  array<mixed>|mixed  $columns",
        "comment_created_at": "2025-05-07T07:45:32+00:00",
        "comment_author": "shaedrich",
        "comment_body": "This is not primarily to be read by humans but by tools and for them `mixed` and your proposed alternative make a **huge** difference. If you want to make it more bite-sized, you can always resort to `@phpstan-type` or the like",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1993214446",
    "pr_number": 54992,
    "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
    "created_at": "2025-03-13T10:25:43+00:00",
    "commented_code": "return $value;\n    }\n\n    /**\n     * Get JSON casting flags for the specified attribute.\n     *\n     * @param  string  $key\n     * @return int",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1993214446",
        "repo_full_name": "laravel/framework",
        "pr_number": 54992,
        "pr_file": "src/Illuminate/Database/Eloquent/Concerns/HasAttributes.php",
        "discussion_id": "1993214446",
        "commented_code": "@@ -1324,15 +1326,33 @@ protected function castAttributeAsJson($key, $value)\n         return $value;\n     }\n \n+    /**\n+     * Get JSON casting flags for the specified attribute.\n+     *\n+     * @param  string  $key\n+     * @return int",
        "comment_created_at": "2025-03-13T10:25:43+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Therefore, you can narrow the return here as well:\r\n```suggestion\r\n     * @return int-mask-of<JSON_*>\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1842638038",
    "pr_number": 53427,
    "pr_file": "src/Illuminate/Console/Scheduling/Schedule.php",
    "created_at": "2024-11-14T17:33:19+00:00",
    "commented_code": "use Illuminate\\Support\\Traits\\Macroable;\nuse RuntimeException;\n\n/**\n * @mixin ScheduleAttributes",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1842638038",
        "repo_full_name": "laravel/framework",
        "pr_number": 53427,
        "pr_file": "src/Illuminate/Console/Scheduling/Schedule.php",
        "discussion_id": "1842638038",
        "commented_code": "@@ -17,9 +18,14 @@\n use Illuminate\\Support\\Traits\\Macroable;\n use RuntimeException;\n \n+/**\n+ * @mixin ScheduleAttributes",
        "comment_created_at": "2024-11-14T17:33:19+00:00",
        "comment_author": "stevebauman",
        "comment_body": "This should be the full namespace:\r\n\r\n```suggestion\r\n * @mixin \\Illuminate\\Console\\Scheduling\\ScheduleAttributes\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1910208001",
    "pr_number": 54148,
    "pr_file": "src/Illuminate/Routing/Controllers/HasMiddleware.php",
    "created_at": "2025-01-10T10:57:00+00:00",
    "commented_code": "/**\n     * Get the middleware that should be assigned to the controller.\n     *\n     * @return \\Illuminate\\Routing\\Controllers\\Middleware[]\n     * @return array<int,\\Illuminate\\Routing\\Controllers\\Middleware|\\Closure|string>",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1910208001",
        "repo_full_name": "laravel/framework",
        "pr_number": 54148,
        "pr_file": "src/Illuminate/Routing/Controllers/HasMiddleware.php",
        "discussion_id": "1910208001",
        "commented_code": "@@ -7,7 +7,7 @@ interface HasMiddleware\n     /**\n      * Get the middleware that should be assigned to the controller.\n      *\n-     * @return \\Illuminate\\Routing\\Controllers\\Middleware[]\n+     * @return array<int,\\Illuminate\\Routing\\Controllers\\Middleware|\\Closure|string>",
        "comment_created_at": "2025-01-10T10:57:00+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Wouldn't this have sufficed?\r\n```suggestion\r\n     * @return (\\Illuminate\\Routing\\Controllers\\Middleware|\\Closure|string)[]\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1910211747",
        "repo_full_name": "laravel/framework",
        "pr_number": 54148,
        "pr_file": "src/Illuminate/Routing/Controllers/HasMiddleware.php",
        "discussion_id": "1910208001",
        "commented_code": "@@ -7,7 +7,7 @@ interface HasMiddleware\n     /**\n      * Get the middleware that should be assigned to the controller.\n      *\n-     * @return \\Illuminate\\Routing\\Controllers\\Middleware[]\n+     * @return array<int,\\Illuminate\\Routing\\Controllers\\Middleware|\\Closure|string>",
        "comment_created_at": "2025-01-10T11:00:12+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Also, is `string` the closest we can get? Have you tried `callable`?\r\n```suggestion\r\n     * @return array<int,\\Illuminate\\Routing\\Controllers\\Middleware|callable>\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1910225592",
        "repo_full_name": "laravel/framework",
        "pr_number": 54148,
        "pr_file": "src/Illuminate/Routing/Controllers/HasMiddleware.php",
        "discussion_id": "1910208001",
        "commented_code": "@@ -7,7 +7,7 @@ interface HasMiddleware\n     /**\n      * Get the middleware that should be assigned to the controller.\n      *\n-     * @return \\Illuminate\\Routing\\Controllers\\Middleware[]\n+     * @return array<int,\\Illuminate\\Routing\\Controllers\\Middleware|\\Closure|string>",
        "comment_created_at": "2025-01-10T11:11:42+00:00",
        "comment_author": "willpower232",
        "comment_body": "using `(...)[]` seems to work just as well but I can't say I have seen that syntax before and tend to defer to the error output from phpstan which currently uses `array<...>`\r\n\r\nit does seem I can remove `\\Closure|string` and replace with `callable` so that is a nice improvement\r\n\r\nI have also seen `list<...>` is valid now so technically `@return list<\\Illuminate\\Routing\\Controllers\\Middleware|callable>` is an option in this case\r\n\r\nI'll wait for github to support polls and or others to vote on the best combination and way forward :sweat_smile: ",
        "pr_file_module": null
      },
      {
        "comment_id": "1910258359",
        "repo_full_name": "laravel/framework",
        "pr_number": 54148,
        "pr_file": "src/Illuminate/Routing/Controllers/HasMiddleware.php",
        "discussion_id": "1910208001",
        "commented_code": "@@ -7,7 +7,7 @@ interface HasMiddleware\n     /**\n      * Get the middleware that should be assigned to the controller.\n      *\n-     * @return \\Illuminate\\Routing\\Controllers\\Middleware[]\n+     * @return array<int,\\Illuminate\\Routing\\Controllers\\Middleware|\\Closure|string>",
        "comment_created_at": "2025-01-10T11:39:49+00:00",
        "comment_author": "shaedrich",
        "comment_body": "That would actually be great for such cases \ud83d\ude02\ud83d\udc4d\ud83c\udffb ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1898688064",
    "pr_number": 54025,
    "pr_file": "src/Illuminate/Database/Schema/Blueprint.php",
    "created_at": "2024-12-27T19:42:45+00:00",
    "commented_code": "return $this->indexCommand('index', $columns, $name, $algorithm);\n    }\n\n    /**\n     * Specify a functional index for the table.\n     *\n     * This method allows you to create a functional index using MySQL expressions\n     * like `LOWER`, `UPPER`, or other supported functions directly on columns.\n     *\n     * @param  string|array  $columns  The column(s) to include in the index.",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1898688064",
        "repo_full_name": "laravel/framework",
        "pr_number": 54025,
        "pr_file": "src/Illuminate/Database/Schema/Blueprint.php",
        "discussion_id": "1898688064",
        "commented_code": "@@ -678,6 +678,37 @@ public function index($columns, $name = null, $algorithm = null)\n         return $this->indexCommand('index', $columns, $name, $algorithm);\n     }\n \n+    /**\n+     * Specify a functional index for the table.\n+     *\n+     * This method allows you to create a functional index using MySQL expressions\n+     * like `LOWER`, `UPPER`, or other supported functions directly on columns.\n+     *\n+     * @param  string|array  $columns  The column(s) to include in the index.",
        "comment_created_at": "2024-12-27T19:42:45+00:00",
        "comment_author": "shaedrich",
        "comment_body": "This could be improved to read:\r\n```suggestion\r\n     * @param  string|string[]  $columns  The column(s) to include in the index.\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
