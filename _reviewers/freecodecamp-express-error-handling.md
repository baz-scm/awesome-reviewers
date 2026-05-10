---
title: Express error handling
description: 'For Express apps, standardize error handling as follows:


  - Define error-handling middleware with the correct signature: `(err, req, res,
  next)`.

  - Register it last in the middleware chain (after routes). If you add a 404 handler,
  place it after routes but before the error handler.'
repository: freeCodeCamp/freeCodeCamp
label: Error Handling
language: Markdown
comments_count: 7
repository_stars: 444449
---

For Express apps, standardize error handling as follows:

- Define error-handling middleware with the correct signature: `(err, req, res, next)`.
- Register it last in the middleware chain (after routes). If you add a 404 handler, place it after routes but before the error handler.
- For async route handlers (especially in Express 4), never rely on Express to catch thrown/rejected async errors—propagate them to the error middleware using `next(err)` via `try/catch` or an `asyncHandler` helper.
- Log full error details server-side, but return user-friendly messages to clients (avoid sending stack traces in production).

Example (safe ordering + async propagation):

```js
const express = require('express');
const app = express();

// Routes
app.get('/', (req, res) => {
  throw new Error('Something went wrong');
});

// 404 handler (after routes, before error handler)
app.use((req, res) => {
  res.status(404).send('Sorry, that route does not exist.');
});

// Async error helper (optional)
function asyncHandler(fn) {
  return (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);
}

app.get('/user', asyncHandler(async (req, res) => {
  const user = await getUserFromDatabase();
  res.send(user);
}));

// Error-handling middleware (LAST)
app.use((err, req, res, next) => {
  console.error(err); // log details internally
  res.status(500).send('Internal Server Error'); // user-friendly response
});
```

Apply this checklist consistently when adding new routes or refactoring middleware order to prevent unhandled promise rejections, ensure consistent HTTP responses, and avoid leaking sensitive error details.