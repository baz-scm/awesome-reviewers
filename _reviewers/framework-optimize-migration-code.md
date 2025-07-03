---
title: Optimize migration code
description: 'When writing database migration code, prioritize clarity and efficiency
  to ensure migrations are reliable and maintainable across environments. Apply these
  practices:'
repository: laravel/framework
label: Migrations
language: PHP
comments_count: 4
repository_stars: 33763
---

When writing database migration code, prioritize clarity and efficiency to ensure migrations are reliable and maintainable across environments. Apply these practices:

1. **Use early returns for better flow control**
   Instead of nesting conditions or using complex branching, return early when a condition is met:

   ```php
   // Instead of this:
   if ($this->shouldSkipMigration($migration)) {
       $this->write(Task::class, $name, fn () => MigrationResult::Skipped);
   } else {
       // other operations
   }

   // Prefer this:
   if ($this->shouldSkipMigration($migration)) {
       $this->write(Task::class, $name, fn () => MigrationResult::Skipped);
       return;
   }
   // other operations
   ```

2. **Prefer array emptiness checks over count operations**
   For better readability and potentially better performance:

   ```php
   // Instead of this:
   if (count($options['selected']) > 0) {
       // ...
   }

   // Prefer this:
   if ($options['selected'] !== []) {
       // ...
   }
   ```

3. **Use method reference syntax when appropriate**
   Replace arrow functions with direct method references when the function is simply passing through arguments:

   ```php
   // Instead of this:
   ->keyBy(fn($file) => $this->getMigrationName($file))

   // Prefer this:
   ->keyBy($this->getMigrationName(...))
   ```

These practices help create more readable and maintainable migration code, reducing the chance of errors during database schema changes.


[
  {
    "discussion_id": "2008500679",
    "pr_number": 55011,
    "pr_file": "src/Illuminate/Database/Migrations/Migrator.php",
    "created_at": "2025-03-22T00:25:12+00:00",
    "commented_code": "return $this->pretendToRun($migration, 'up');\n        }\n\n        $this->write(Task::class, $name, fn () => $this->runMigration($migration, 'up'));\n        if ($this->shouldSkipMigration($migration)) {\n            $this->write(Task::class, $name, fn () => MigrationResult::Skipped);",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "2008500679",
        "repo_full_name": "laravel/framework",
        "pr_number": 55011,
        "pr_file": "src/Illuminate/Database/Migrations/Migrator.php",
        "discussion_id": "2008500679",
        "commented_code": "@@ -241,12 +254,16 @@ protected function runUp($file, $batch, $pretend)\n             return $this->pretendToRun($migration, 'up');\n         }\n \n-        $this->write(Task::class, $name, fn () => $this->runMigration($migration, 'up'));\n+        if ($this->shouldSkipMigration($migration)) {\n+            $this->write(Task::class, $name, fn () => MigrationResult::Skipped);",
        "comment_created_at": "2025-03-22T00:25:12+00:00",
        "comment_author": "inmanturbo",
        "comment_body": "Shouldn't this return here instead of the else?\r\n\r\nThis will log the migration even though it was never run? This means that the migration won't get run later either, after the \"feature\" is \"enabled\" or `Migration::shouldRun()` otherwise returns `true`;\r\n\r\n```php\r\n\r\n        if ($this->shouldSkipMigration($migration)) {\r\n            $this->write(Task::class, $name, fn () => MigrationResult::Skipped);\r\n            return;\r\n         }\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2008510104",
        "repo_full_name": "laravel/framework",
        "pr_number": 55011,
        "pr_file": "src/Illuminate/Database/Migrations/Migrator.php",
        "discussion_id": "2008500679",
        "commented_code": "@@ -241,12 +254,16 @@ protected function runUp($file, $batch, $pretend)\n             return $this->pretendToRun($migration, 'up');\n         }\n \n-        $this->write(Task::class, $name, fn () => $this->runMigration($migration, 'up'));\n+        if ($this->shouldSkipMigration($migration)) {\n+            $this->write(Task::class, $name, fn () => MigrationResult::Skipped);",
        "comment_created_at": "2025-03-22T00:32:25+00:00",
        "comment_author": "inmanturbo",
        "comment_body": "Ahh I see, I was confused, you wrapped the `Migrator::log()` call inside the else block. In that case I would suggest just returning early.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1921142352",
    "pr_number": 54250,
    "pr_file": "src/Illuminate/Database/Migrations/Migrator.php",
    "created_at": "2025-01-18T20:00:20+00:00",
    "commented_code": "// We want to pull in the last batch of migrations that ran on the previous\n        // migration operation. We'll then reverse those migrations and run each\n        // of them \"down\" to reverse the last migration \"operation\" which ran.\n        $migrations = $this->getMigrationsForRollback($options);\n        $migrations = isset($options['selected']) && count($options['selected']) > 0 ? $options['selected'] : $this->getMigrationsForRollback($options);",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1921142352",
        "repo_full_name": "laravel/framework",
        "pr_number": 54250,
        "pr_file": "src/Illuminate/Database/Migrations/Migrator.php",
        "discussion_id": "1921142352",
        "commented_code": "@@ -230,7 +231,7 @@ public function rollback($paths = [], array $options = [])\n         // We want to pull in the last batch of migrations that ran on the previous\n         // migration operation. We'll then reverse those migrations and run each\n         // of them \"down\" to reverse the last migration \"operation\" which ran.\n-        $migrations = $this->getMigrationsForRollback($options);\n+        $migrations = isset($options['selected']) && count($options['selected']) > 0 ? $options['selected'] : $this->getMigrationsForRollback($options);",
        "comment_created_at": "2025-01-18T20:00:20+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Function call can be avoided like this:\r\n```suggestion\r\n        $migrations = isset($options['selected']) && $options['selected'] !== [] ? $options['selected'] : $this->getMigrationsForRollback($options);\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1921142441",
    "pr_number": 54250,
    "pr_file": "src/Illuminate/Database/Migrations/Migrator.php",
    "created_at": "2025-01-18T20:01:08+00:00",
    "commented_code": "{\n        $this->events?->dispatch($event);\n    }\n\n    protected function getMigrationBatches($migrations)\n    {\n        $options = $this->resolveOptions($migrations);\n        $selected = $options['selected'] ?? [];\n\n        if (count($selected) > 0) {",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1921142441",
        "repo_full_name": "laravel/framework",
        "pr_number": 54250,
        "pr_file": "src/Illuminate/Database/Migrations/Migrator.php",
        "discussion_id": "1921142441",
        "commented_code": "@@ -754,4 +758,32 @@ public function fireMigrationEvent($event)\n     {\n         $this->events?->dispatch($event);\n     }\n+\n+    protected function getMigrationBatches($migrations)\n+    {\n+        $options = $this->resolveOptions($migrations);\n+        $selected = $options['selected'] ?? [];\n+\n+        if (count($selected) > 0) {",
        "comment_created_at": "2025-01-18T20:01:08+00:00",
        "comment_author": "shaedrich",
        "comment_body": "Same here:\r\n```suggestion\r\n        if ($selected !== []) {\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1921142809",
    "pr_number": 54250,
    "pr_file": "src/Illuminate/Database/Migrations/Migrator.php",
    "created_at": "2025-01-18T20:03:19+00:00",
    "commented_code": "public function getMigrationFiles($paths)\n    {\n        return (new Collection($paths))\n            ->flatMap(fn ($path) => str_ends_with($path, '.php') ? [$path] : $this->files->glob($path.'/*_*.php'))\n            ->flatMap(fn($path) => str_ends_with($path, '.php') ? [$path] : $this->files->glob($path . '/*_*.php'))\n            ->filter()\n            ->values()\n            ->keyBy(fn ($file) => $this->getMigrationName($file))\n            ->sortBy(fn ($file, $key) => $key)\n            ->keyBy(fn($file) => $this->getMigrationName($file))",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1921142809",
        "repo_full_name": "laravel/framework",
        "pr_number": 54250,
        "pr_file": "src/Illuminate/Database/Migrations/Migrator.php",
        "discussion_id": "1921142809",
        "commented_code": "@@ -537,11 +541,11 @@ protected function getMigrationClass(string $migrationName): string\n     public function getMigrationFiles($paths)\n     {\n         return (new Collection($paths))\n-            ->flatMap(fn ($path) => str_ends_with($path, '.php') ? [$path] : $this->files->glob($path.'/*_*.php'))\n+            ->flatMap(fn($path) => str_ends_with($path, '.php') ? [$path] : $this->files->glob($path . '/*_*.php'))\n             ->filter()\n             ->values()\n-            ->keyBy(fn ($file) => $this->getMigrationName($file))\n-            ->sortBy(fn ($file, $key) => $key)\n+            ->keyBy(fn($file) => $this->getMigrationName($file))",
        "comment_created_at": "2025-01-18T20:03:19+00:00",
        "comment_author": "shaedrich",
        "comment_body": "You might be able to replace it with this:\r\n```suggestion\r\n            ->keyBy($this->getMigrationName(...))\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
