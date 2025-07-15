---
title: Access settings properly
description: Always use the provided settings accessor methods (`app.get()`, `app.set()`,
  `app.enabled()`, `app.disabled()`) to access application configuration instead of
  directly accessing the settings object. Direct access to the settings object was
  deprecated and may lead to inconsistent behavior or errors.
repository: expressjs/express
label: Configurations
language: JavaScript
comments_count: 4
repository_stars: 67300
---

Always use the provided settings accessor methods (`app.get()`, `app.set()`, `app.enabled()`, `app.disabled()`) to access application configuration instead of directly accessing the settings object. Direct access to the settings object was deprecated and may lead to inconsistent behavior or errors.

When checking configuration values:

```javascript
// Incorrect
if (app.settings.etag == false) {
  opts.etag = app.settings.etag;
}

// Correct
if (app.disabled('etag')) {
  opts.etag = app.get('etag');
}
```

Similarly, when referencing environment settings:

```javascript
// Incorrect
var space = 2 * process.env.NODE_ENV == 'development';

// Correct
var space = 2 * app.get('env') == 'development';
```

This approach ensures your code respects the configuration system's internal logic, handles default values correctly, and remains compatible with future framework versions. It also makes your code more maintainable as all configuration access follows a consistent pattern.