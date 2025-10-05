---
title: avoid build side effects
description: Build scripts should avoid performing operations as side effects and
  instead use explicit, dedicated tasks for each operation. Side effects make build
  processes unpredictable, harder to maintain, and difficult to debug when issues
  arise.
repository: facebook/yoga
label: CI/CD
language: JavaScript
comments_count: 2
repository_stars: 18255
---

Build scripts should avoid performing operations as side effects and instead use explicit, dedicated tasks for each operation. Side effects make build processes unpredictable, harder to maintain, and difficult to debug when issues arise.

Instead of creating directories, cleaning files, or performing setup operations implicitly within other tasks, create dedicated tasks with clear responsibilities. This approach improves build reliability, makes the build process more transparent, and allows for better control over execution order.

For example, rather than creating a dist folder as a side effect in the main build configuration:

```javascript
// Avoid this - side effect
module.exports = function(grunt) {
  // Create the dist folder if it doesn't exist. It is deleted by the 'clean' task.
  if (!fs.existsSync('dist')) {
    fs.mkdirSync('dist');
  }
  
  // rest of configuration...
};
```

Use explicit tasks instead:

```javascript
// Prefer this - explicit task
grunt.registerTask('ensure-dirs', function() {
  if (!fs.existsSync('dist')) {
    fs.mkdirSync('dist');
  }
});

grunt.registerTask('build', ['ensure-dirs', 'other-tasks']);
```

This makes the build process more predictable and allows the clean task to properly handle `dist/**` patterns without worrying about implicit directory creation elsewhere.