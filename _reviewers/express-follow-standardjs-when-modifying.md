---
title: Follow StandardJS when modifying
description: When modifying existing code, update the touched lines to follow StandardJS
  conventions while preserving the style of untouched code. This ensures gradual,
  consistent adoption of StandardJS formatting.
repository: expressjs/express
label: Code Style
language: JavaScript
comments_count: 7
repository_stars: 67300
---

When modifying existing code, update the touched lines to follow StandardJS conventions while preserving the style of untouched code. This ensures gradual, consistent adoption of StandardJS formatting.

Key StandardJS rules to apply:
- Use multiple const declarations instead of comma-separated ones
- Omit semicolons
- Add space after function keyword
- Don't indent chained method calls

Example of updating code to StandardJS:

```javascript
// Before
var express = require('../..'),
    bodyParser = require('body-parser'),
    session = require('express-session');

app.get('/', function(req, res){
  res.send('Hello form root route.');
});

// After
const express = require('../..')
const bodyParser = require('body-parser')
const session = require('express-session')

app.get('/', function (req, res) {
  res.send('Hello from root route.')
})
```

Only update lines you're actively modifying - don't reformat entire files just for style consistency. This enables gradual adoption while maintaining codebase stability.