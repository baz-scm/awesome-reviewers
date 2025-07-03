---
title: Optimize for code readability
description: 'Prioritize code readability over clever solutions by:

  1. Using early returns to reduce nesting

  2. Leveraging modern PHP features when they improve clarity'
repository: laravel/framework
label: Code Style
language: PHP
comments_count: 10
repository_stars: 33763
---

Prioritize code readability over clever solutions by:
1. Using early returns to reduce nesting
2. Leveraging modern PHP features when they improve clarity
3. Maintaining consistent style patterns
4. Simplifying complex logic

Example - Before:
```php
protected function parseIds($value)
{
    if (is_null($value)) {
        return [];
    }

    if (is_string($value)) {
        return array_map('trim', explode(',', $value));
    }

    check_type($value, 'array', $key, 'Environment');

    return $value;
}
```

Example - After:
```php
protected function parseIds($value)
{
    return match (true) {
        $value === null => [],
        is_string($value) => array_map('trim', explode(',', $value)),
        default => check_type($value, 'array', $key, 'Environment'),
    };
}
```

The improved version:
- Uses match expression for cleaner flow control
- Maintains consistent null comparison style
- Reduces nesting and cognitive load
- Leverages modern PHP features appropriately

Choose simpler constructs when they improve readability, but avoid sacrificing clarity for brevity. The goal is to write code that is easy to understand and maintain.


[
  {
    "discussion_id": "2101199329",
    "pr_number": 55810,
    "pr_file": "src/Illuminate/Filesystem/FilesystemAdapter.php",
    "created_at": "2025-05-21T21:27:36+00:00",
    "commented_code": "*/\n    public function url($path)\n    {\n        if (isset($this->config['prefix'])) {\n        if (isset($this->config['prefix']) && ! empty($this->config['prefix'])) {\n            $path = $this->concatPathToUrl($this->config['prefix'], $path);",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2101199329",
        "repo_full_name": "laravel/framework",
        "pr_number": 55810,
        "pr_file": "src/Illuminate/Filesystem/FilesystemAdapter.php",
        "discussion_id": "2101199329",
        "commented_code": "@@ -725,7 +725,7 @@ public function writeStream($path, $resource, array $options = [])\n      */\n     public function url($path)\n     {\n-        if (isset($this->config['prefix'])) {\n+        if (isset($this->config['prefix']) && ! empty($this->config['prefix'])) {\n             $path = $this->concatPathToUrl($this->config['prefix'], $path);",
        "comment_created_at": "2025-05-21T21:27:36+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Shouldn't this be handled _inside_ the `concatPathToUrl()` method?",
        "pr_file_module": null
      },
      {
        "comment_id": "2101227158",
        "repo_full_name": "laravel/framework",
        "pr_number": 55810,
        "pr_file": "src/Illuminate/Filesystem/FilesystemAdapter.php",
        "discussion_id": "2101199329",
        "commented_code": "@@ -725,7 +725,7 @@ public function writeStream($path, $resource, array $options = [])\n      */\n     public function url($path)\n     {\n-        if (isset($this->config['prefix'])) {\n+        if (isset($this->config['prefix']) && ! empty($this->config['prefix'])) {\n             $path = $this->concatPathToUrl($this->config['prefix'], $path);",
        "comment_created_at": "2025-05-21T21:50:07+00:00",
        "comment_author": "MrTuffaha",
        "comment_body": "good point",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2101260253",
    "pr_number": 55810,
    "pr_file": "src/Illuminate/Filesystem/FilesystemAdapter.php",
    "created_at": "2025-05-21T22:12:45+00:00",
    "commented_code": "*/\n    protected function concatPathToUrl($url, $path)\n    {\n        if (empty($url)) {\n            return trim($path, '/');\n        }\n\n        if (empty($path)) {\n            return trim($url, '/');\n        }\n\n        return rtrim($url, '/').'/'.ltrim($path, '/');",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2101260253",
        "repo_full_name": "laravel/framework",
        "pr_number": 55810,
        "pr_file": "src/Illuminate/Filesystem/FilesystemAdapter.php",
        "discussion_id": "2101260253",
        "commented_code": "@@ -847,6 +847,14 @@ public function temporaryUploadUrl($path, $expiration, array $options = [])\n      */\n     protected function concatPathToUrl($url, $path)\n     {\n+        if (empty($url)) {\n+            return trim($path, '/');\n+        }\n+\n+        if (empty($path)) {\n+            return trim($url, '/');\n+        }\n+\n         return rtrim($url, '/').'/'.ltrim($path, '/');",
        "comment_created_at": "2025-05-21T22:12:45+00:00",
        "comment_author": "shaedrich",
        "comment_body": "You could even shorten that, if you want:\r\n```suggestion\r\n        return match (true) {\r\n            empty($url) => trim($path, '/'),\r\n            empty($path) => trim($url, '/'),\r\n            default => rtrim($url, '/').'/'.ltrim($path, '/'),\r\n        };\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2101264645",
        "repo_full_name": "laravel/framework",
        "pr_number": 55810,
        "pr_file": "src/Illuminate/Filesystem/FilesystemAdapter.php",
        "discussion_id": "2101260253",
        "commented_code": "@@ -847,6 +847,14 @@ public function temporaryUploadUrl($path, $expiration, array $options = [])\n      */\n     protected function concatPathToUrl($url, $path)\n     {\n+        if (empty($url)) {\n+            return trim($path, '/');\n+        }\n+\n+        if (empty($path)) {\n+            return trim($url, '/');\n+        }\n+\n         return rtrim($url, '/').'/'.ltrim($path, '/');",
        "comment_created_at": "2025-05-21T22:17:40+00:00",
        "comment_author": "MrTuffaha",
        "comment_body": "While i do like shorter code, i do belive that my code is easier to inderstand/more readable, at least at first glance.",
        "pr_file_module": null
      },
      {
        "comment_id": "2102187470",
        "repo_full_name": "laravel/framework",
        "pr_number": 55810,
        "pr_file": "src/Illuminate/Filesystem/FilesystemAdapter.php",
        "discussion_id": "2101260253",
        "commented_code": "@@ -847,6 +847,14 @@ public function temporaryUploadUrl($path, $expiration, array $options = [])\n      */\n     protected function concatPathToUrl($url, $path)\n     {\n+        if (empty($url)) {\n+            return trim($path, '/');\n+        }\n+\n+        if (empty($path)) {\n+            return trim($url, '/');\n+        }\n+\n         return rtrim($url, '/').'/'.ltrim($path, '/');",
        "comment_created_at": "2025-05-22T10:11:49+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Yeah, no problem \ud83d\ude03 :+1:",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1975059131",
    "pr_number": 54845,
    "pr_file": "src/Illuminate/Validation/Validator.php",
    "created_at": "2025-02-28T09:05:49+00:00",
    "commented_code": "*/\n    protected function validateUsingCustomRule($attribute, $value, $rule)\n    {\n        $attribute = $this->replacePlaceholderInString($attribute);\n        $originalAttribute = $this->replacePlaceholderInString($attribute);\n\n        $attribute = match (true) {\n            $rule instanceof Rules\\File => $attribute,\n            default => $originalAttribute,\n        };",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1975059131",
        "repo_full_name": "laravel/framework",
        "pr_number": 54845,
        "pr_file": "src/Illuminate/Validation/Validator.php",
        "discussion_id": "1975059131",
        "commented_code": "@@ -872,7 +872,12 @@ protected function hasNotFailedPreviousRuleIfPresenceRule($rule, $attribute)\n      */\n     protected function validateUsingCustomRule($attribute, $value, $rule)\n     {\n-        $attribute = $this->replacePlaceholderInString($attribute);\n+        $originalAttribute = $this->replacePlaceholderInString($attribute);\n+\n+        $attribute = match (true) {\n+            $rule instanceof Rules\\File => $attribute,\n+            default => $originalAttribute,\n+        };",
        "comment_created_at": "2025-02-28T09:05:49+00:00",
        "comment_author": "shaedrich",
        "comment_body": "match statements with only two cases kinda defeat the purpose, I'd say\r\n```suggestion\r\n        $originalAttribute = $this->replacePlaceholderInString($attribute);\r\n\r\n        $attribute = $rule instanceof Rules\\File\r\n            ? $attribute\r\n            : $this->replacePlaceholderInString($attribute);\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1868256502",
    "pr_number": 53748,
    "pr_file": "src/Illuminate/Database/Console/PruneCommand.php",
    "created_at": "2024-12-03T19:08:18+00:00",
    "commented_code": "protected function getPath()\n    {\n        if (! empty($path = $this->option('path'))) {\n            return (new Collection($path))->map(function ($path) {\n                return base_path($path);\n            })->all();\n            return (new Collection($path))\n                ->map(fn ($path) => base_path($path))",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1868256502",
        "repo_full_name": "laravel/framework",
        "pr_number": 53748,
        "pr_file": "src/Illuminate/Database/Console/PruneCommand.php",
        "discussion_id": "1868256502",
        "commented_code": "@@ -157,9 +157,9 @@ protected function models()\n     protected function getPath()\n     {\n         if (! empty($path = $this->option('path'))) {\n-            return (new Collection($path))->map(function ($path) {\n-                return base_path($path);\n-            })->all();\n+            return (new Collection($path))\n+                ->map(fn ($path) => base_path($path))",
        "comment_created_at": "2024-12-03T19:08:18+00:00",
        "comment_author": "shaedrich",
        "comment_body": "This can be just\r\n```suggestion\r\n                ->map('base_path')\r\n```\r\nor\r\n```suggestion\r\n                ->map(base_path(...))\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1868258127",
    "pr_number": 53748,
    "pr_file": "src/Illuminate/Database/Eloquent/Model.php",
    "created_at": "2024-12-03T19:09:48+00:00",
    "commented_code": "*/\n    public function qualifyColumns($columns)\n    {\n        return (new BaseCollection($columns))->map(function ($column) {\n            return $this->qualifyColumn($column);\n        })->all();\n        return (new BaseCollection($columns))\n            ->map(fn ($column) => $this->qualifyColumn($column))",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1868258127",
        "repo_full_name": "laravel/framework",
        "pr_number": 53748,
        "pr_file": "src/Illuminate/Database/Eloquent/Model.php",
        "discussion_id": "1868258127",
        "commented_code": "@@ -600,9 +600,9 @@ public function qualifyColumn($column)\n      */\n     public function qualifyColumns($columns)\n     {\n-        return (new BaseCollection($columns))->map(function ($column) {\n-            return $this->qualifyColumn($column);\n-        })->all();\n+        return (new BaseCollection($columns))\n+            ->map(fn ($column) => $this->qualifyColumn($column))",
        "comment_created_at": "2024-12-03T19:09:48+00:00",
        "comment_author": "shaedrich",
        "comment_body": "This can just be\r\n```suggestion\r\n            ->map([ $this, 'qualifyColumn' ])\r\n```\r\n\r\nor\r\n```suggestion\r\n            ->map($this->qualifyColumn(...))\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1868261023",
    "pr_number": 53748,
    "pr_file": "src/Illuminate/Database/Query/Grammars/PostgresGrammar.php",
    "created_at": "2024-12-03T19:12:24+00:00",
    "commented_code": "{\n        $quote = func_num_args() === 2 ? func_get_arg(1) : \"'\";\n\n        return (new Collection($path))->map(function ($attribute) {\n            return $this->parseJsonPathArrayKeys($attribute);\n        })->collapse()->map(function ($attribute) use ($quote) {\n            return filter_var($attribute, FILTER_VALIDATE_INT) !== false\n                        ? $attribute\n                        : $quote.$attribute.$quote;\n        })->all();\n        return (new Collection($path))\n            ->map(fn ($attribute) => $this->parseJsonPathArrayKeys($attribute))",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1868261023",
        "repo_full_name": "laravel/framework",
        "pr_number": 53748,
        "pr_file": "src/Illuminate/Database/Query/Grammars/PostgresGrammar.php",
        "discussion_id": "1868261023",
        "commented_code": "@@ -734,13 +736,15 @@ protected function wrapJsonPathAttributes($path)\n     {\n         $quote = func_num_args() === 2 ? func_get_arg(1) : \"'\";\n \n-        return (new Collection($path))->map(function ($attribute) {\n-            return $this->parseJsonPathArrayKeys($attribute);\n-        })->collapse()->map(function ($attribute) use ($quote) {\n-            return filter_var($attribute, FILTER_VALIDATE_INT) !== false\n-                        ? $attribute\n-                        : $quote.$attribute.$quote;\n-        })->all();\n+        return (new Collection($path))\n+            ->map(fn ($attribute) => $this->parseJsonPathArrayKeys($attribute))",
        "comment_created_at": "2024-12-03T19:12:24+00:00",
        "comment_author": "shaedrich",
        "comment_body": "This can be simplified to just\r\n```suggestion\r\n            ->map([ $this, 'parseJsonPathArrayKeys' ])\r\n```\r\n\r\nor\r\n```suggestion\r\n            ->map($this->parseJsonPathArrayKeys(...))\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1977480863",
    "pr_number": 54874,
    "pr_file": "src/Illuminate/Collections/helpers.php",
    "created_at": "2025-03-03T12:59:21+00:00",
    "commented_code": "}\n}\n\nif (! function_exists('deepCollect')) {\n    /**\n     * Recursively convert an array and its nested arrays into Laravel collections.\n     *\n     * This function takes an array (or any iterable) and transforms it into an instance\n     * of Laravel's Collection class. It applies the transformation to all nested arrays,\n     * ensuring that every level of the array structure is converted into collections.\n     *\n     * @param  mixed  $value  The input value, which can be an array, an iterable, or any other data type.\n     * @return mixed If the value is an array, a Collection instance is returned with all nested arrays\n     *               converted. If the value is not an array, it is returned as-is.\n     */\n    function deepCollect($value)\n    {\n        // If the value is an array, convert it into a Collection and apply deepCollect recursively\n        if (is_array($value)) {\n            return collect($value)->map(fn ($item) => deepCollect($item));",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1977480863",
        "repo_full_name": "laravel/framework",
        "pr_number": 54874,
        "pr_file": "src/Illuminate/Collections/helpers.php",
        "discussion_id": "1977480863",
        "commented_code": "@@ -19,6 +19,30 @@ function collect($value = [])\n     }\n }\n \n+if (! function_exists('deepCollect')) {\n+    /**\n+     * Recursively convert an array and its nested arrays into Laravel collections.\n+     *\n+     * This function takes an array (or any iterable) and transforms it into an instance\n+     * of Laravel's Collection class. It applies the transformation to all nested arrays,\n+     * ensuring that every level of the array structure is converted into collections.\n+     *\n+     * @param  mixed  $value  The input value, which can be an array, an iterable, or any other data type.\n+     * @return mixed If the value is an array, a Collection instance is returned with all nested arrays\n+     *               converted. If the value is not an array, it is returned as-is.\n+     */\n+    function deepCollect($value)\n+    {\n+        // If the value is an array, convert it into a Collection and apply deepCollect recursively\n+        if (is_array($value)) {\n+            return collect($value)->map(fn ($item) => deepCollect($item));",
        "comment_created_at": "2025-03-03T12:59:21+00:00",
        "comment_author": "shaedrich",
        "comment_body": "You might be able to use first-class callable syntax here:\r\n```suggestion\r\n            return collect($value)->map(deepCollect(...));\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1953107378",
    "pr_number": 54582,
    "pr_file": "src/Illuminate/Database/Eloquent/Filterable.php",
    "created_at": "2025-02-12T17:28:02+00:00",
    "commented_code": "<?php\n\nnamespace Illuminate\\Database\\Eloquent;\n\nuse Illuminate\\Database\\Eloquent\\Builder;\n\ntrait Filterable\n{\n\n    protected $filterNamespace = 'App\\Filters\\\\';\n\n    public function scopeFilter(Builder $builder, array $params): void\n    {\n        if (is_array($params) and !empty($params)) {\n\n            foreach ($params as $class => $methodOrValue) {\n\n                $className = $this->filterNamespace . ucfirst($class);\n\n                if (class_exists($className)) {\n\n                    if (method_exists($className, $methodOrValue))\n                        $className::{$methodOrValue}($builder);\n\n                    if (method_exists($className, 'apply'))\n                        $className::apply($builder, $methodOrValue);\n                }\n            }\n        }\n    }",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1953107378",
        "repo_full_name": "laravel/framework",
        "pr_number": 54582,
        "pr_file": "src/Illuminate/Database/Eloquent/Filterable.php",
        "discussion_id": "1953107378",
        "commented_code": "@@ -0,0 +1,36 @@\n+<?php\n+\n+namespace Illuminate\\Database\\Eloquent;\n+\n+use Illuminate\\Database\\Eloquent\\Builder;\n+\n+trait Filterable\n+{\n+\n+    protected $filterNamespace = 'App\\Filters\\\\';\n+\n+    public function scopeFilter(Builder $builder, array $params): void\n+    {\n+        if (is_array($params) and !empty($params)) {\n+\n+            foreach ($params as $class => $methodOrValue) {\n+\n+                $className = $this->filterNamespace . ucfirst($class);\n+\n+                if (class_exists($className)) {\n+\n+                    if (method_exists($className, $methodOrValue))\n+                        $className::{$methodOrValue}($builder);\n+\n+                    if (method_exists($className, 'apply'))\n+                        $className::apply($builder, $methodOrValue);\n+                }\n+            }\n+        }\n+    }",
        "comment_created_at": "2025-02-12T17:28:02+00:00",
        "comment_author": "shaedrich",
        "comment_body": "You might want to use early returns here:\r\n```suggestion\r\n    public function scopeFilter(Builder $builder, array $params): void\r\n    {\r\n        if (!is_array($params) || $params === []) {\r\n        \treturn;\r\n        }\r\n\r\n        foreach ($params as $class => $methodOrValue) {\r\n            $className = $this->filterNamespace . ucfirst($class);\r\n\r\n            if (!class_exists($className)) {\r\n\t\t\t\tcontinue;\r\n            }\r\n\r\n            if (method_exists($className, $methodOrValue)) {\r\n                $className::{$methodOrValue}($builder);\r\n            }\r\n\r\n            if (method_exists($className, 'apply')) {\r\n                $className::apply($builder, $methodOrValue);\r\n            }\r\n        }\r\n    }\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1953141984",
    "pr_number": 54582,
    "pr_file": "src/Illuminate/View/Compilers/Concerns/CompilesApplied.php",
    "created_at": "2025-02-12T17:49:06+00:00",
    "commented_code": "<?php\n\nnamespace Illuminate\\View\\Compilers\\Concerns;\n\nuse Illuminate\\Contracts\\View\\ViewCompilationException;\n\ntrait CompilesApplied\n{\n    /**\n     * Compile the conditional applied statement into valid PHP.\n     */\n    protected function compileApplied(string|null $expression): string\n    {\n        preg_match('/^\\(([\\'\"])([^\\'\"]+)\\1,\\1([^\\'\"]+)\\1,\\1([^\\'\"]+)\\1\\)$/', $expression ?? '', $matches);\n\n        if (count($matches) === 0)\n            throw new ViewCompilationException('Malformed @applied statement.');\n\n        $expression = str_replace('(', '', $expression);\n        $expression = str_replace(')', '', $expression);\n        $result = explode(',', $expression);",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1953141984",
        "repo_full_name": "laravel/framework",
        "pr_number": 54582,
        "pr_file": "src/Illuminate/View/Compilers/Concerns/CompilesApplied.php",
        "discussion_id": "1953141984",
        "commented_code": "@@ -0,0 +1,30 @@\n+<?php\n+\n+namespace Illuminate\\View\\Compilers\\Concerns;\n+\n+use Illuminate\\Contracts\\View\\ViewCompilationException;\n+\n+trait CompilesApplied\n+{\n+    /**\n+     * Compile the conditional applied statement into valid PHP.\n+     */\n+    protected function compileApplied(string|null $expression): string\n+    {\n+        preg_match('/^\\(([\\'\"])([^\\'\"]+)\\1,\\1([^\\'\"]+)\\1,\\1([^\\'\"]+)\\1\\)$/', $expression ?? '', $matches);\n+\n+        if (count($matches) === 0)\n+            throw new ViewCompilationException('Malformed @applied statement.');\n+\n+        $expression = str_replace('(', '', $expression);\n+        $expression = str_replace(')', '', $expression);\n+        $result = explode(',', $expression);",
        "comment_created_at": "2025-02-12T17:49:06+00:00",
        "comment_author": "shaedrich",
        "comment_body": "You can avoid intermediate variables:\r\n```suggestion\r\n        $result = Str::of($expression)\r\n        \t->replace('(', '')\r\n        \t->replace(')', '')\r\n        \t->explode(',');\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1935718228",
    "pr_number": 54417,
    "pr_file": "src/Illuminate/Validation/ValidationRuleParser.php",
    "created_at": "2025-01-30T14:37:26+00:00",
    "commented_code": "return Arr::wrap($this->prepareRule($rule, $attribute));\n        }\n\n        $rules = [];\n\n        foreach ($rule as $value) {\n            if ($value instanceof Date) {\n                $rules = array_merge($rules, explode('|', (string) $value));\n            } else {\n                $rules[] = $this->prepareRule($value, $attribute);\n            }\n        }\n\n        return $rules;\n        return array_map(\n            [$this, 'prepareRule'],",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1935718228",
        "repo_full_name": "laravel/framework",
        "pr_number": 54417,
        "pr_file": "src/Illuminate/Validation/ValidationRuleParser.php",
        "discussion_id": "1935718228",
        "commented_code": "@@ -96,17 +95,11 @@ protected function explodeExplicitRule($rule, $attribute)\n             return Arr::wrap($this->prepareRule($rule, $attribute));\n         }\n \n-        $rules = [];\n-\n-        foreach ($rule as $value) {\n-            if ($value instanceof Date) {\n-                $rules = array_merge($rules, explode('|', (string) $value));\n-            } else {\n-                $rules[] = $this->prepareRule($value, $attribute);\n-            }\n-        }\n-\n-        return $rules;\n+        return array_map(\n+            [$this, 'prepareRule'],",
        "comment_created_at": "2025-01-30T14:37:26+00:00",
        "comment_author": "shaedrich",
        "comment_body": "You could use first-class callable syntax here:\r\n```suggestion\r\n            $this->prepareRule(...),\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
