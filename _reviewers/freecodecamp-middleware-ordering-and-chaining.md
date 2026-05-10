---
title: Middleware ordering and chaining
description: 'When using Express, treat middleware registration as an HTTP request-processing
  pipeline: middleware executes in the order you add it, and the chain advances only
  if your middleware calls `next()`.'
repository: freeCodeCamp/freeCodeCamp
label: Networking
language: Markdown
comments_count: 5
repository_stars: 444449
---

When using Express, treat middleware registration as an HTTP request-processing pipeline: middleware executes in the order you add it, and the chain advances only if your middleware calls `next()`.

Apply this standard:
- Use the canonical middleware signature in code/docs: `(req, res, next)`.
- Register middleware with `app.use(...)` (and any static middleware) in the exact order you need.
- Call `next()` whenever the request should continue to later middleware/route handlers; if you don’t call it, the request-response cycle stops.
- Stack built-in and third-party middleware intentionally; later middleware can depend on earlier changes to `req`/`res`.

Example:
```js
const express = require('express')
const cors = require('cors')
const morgan = require('morgan')
const app = express()

// 1) Parse/prepare request (built-in)
app.use(express.json())

// 2) Middleware behavior depends on order (third-party)
app.use(cors())
app.use(morgan('tiny'))

// 3) Intercept/transform request, then continue
app.use((req, res, next) => {
  req.requestId = req.header('x-request-id')
  next() // must be called to reach the next middleware/route
})

// 4) Serve static assets via middleware (register intentionally)
app.use(express.static('public'))

app.get('/', (req, res) => res.send('Hello'))

app.listen(3000)
```

Outcome: predictable HTTP behavior, fewer “why didn’t my route run?” issues, and middleware effects (auth, logging, parsing, static serving) that are consistent across the app.