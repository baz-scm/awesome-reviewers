---
title: Modern TypeScript style
description: 'Use modern TypeScript syntax and conventions throughout the codebase.
  This includes:

  - Using `const` instead of `var` for variable declarations unless reassignment is
  needed'
repository: expressjs/express
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 67300
---

Use modern TypeScript syntax and conventions throughout the codebase. This includes:
- Using `const` instead of `var` for variable declarations unless reassignment is needed
- Using ES module syntax (`import express from 'express'`) instead of CommonJS `require()`
- Explicitly typing function parameters and return values

Example (before):
```typescript
const express = require("express");

const app: import("express").Application = module.exports = express();

app.get('/', function(request, response) {
    console.log(request.url);
```

Example (after):
```typescript
import express from 'express';
import { Request, Response } from 'express';

const app = express();

app.get('/', function(request: Request, response: Response) {
    console.log(request.url);
});
```