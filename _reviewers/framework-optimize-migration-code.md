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
