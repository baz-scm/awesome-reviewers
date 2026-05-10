---
title: Middleware and Status Semantics
description: 'When building API endpoints with Express, make request lifecycle control-flow
  and response semantics explicit and consistent:


  - Middleware chaining: only call `next()` when you intend to continue to the next
  middleware/handler; if you don’t call `next()`, the request-response cycle will
  stop.'
repository: freeCodeCamp/freeCodeCamp
label: API
language: Markdown
comments_count: 5
repository_stars: 444449
---

When building API endpoints with Express, make request lifecycle control-flow and response semantics explicit and consistent:

- Middleware chaining: only call `next()` when you intend to continue to the next middleware/handler; if you don’t call `next()`, the request-response cycle will stop.
- Ordering: rely on the fact middleware executes in the order it’s added; mount router modules intentionally.
- Response outcomes: in each terminal handler, return an HTTP status code that matches the outcome (e.g., `400` for bad requests, `200` for success, `500` for server errors) and use an appropriate body format (string vs JSON).

Example:
```js
const express = require('express');
const app = express();

// Global middleware (runs in order)
app.use((req, res, next) => {
  console.log(req.method, req.url);
  next(); // continue the lifecycle
});

const api = express.Router();
api.use('/v1', (req, res, next) => {
  // router-level middleware
  next();
});

api.get('/v1/resource', (req, res) => {
  // terminal handler: choose status code + body that match the outcome
  return res.status(200).json({ ok: true });
});

api.post('/v1/resource', express.json(), (req, res) => {
  if (!req.body || !req.body.name) {
    return res.status(400).send('Bad Request');
  }
  return res.status(201).json({ created: true });
});

app.use(api);
app.listen(3000);
```

Use this checklist in reviews:
1) Does every middleware either call `next()` or send a response (intentionally terminating)?
2) Are middleware/routers mounted in the intended order/module boundaries?
3) Do your route handlers return status codes and response bodies that accurately represent success/client error/server error?
