---
title: "Support flexible logging"
description: "When designing logging interfaces, create flexible APIs that accommodate both standard and custom logging needs. This includes supporting custom log levels, allowing message format customization, and enabling level selection based on context."
repository: "fastify/fastify"
label: "Logging"
language: "JavaScript"
comments_count: 2
repository_stars: 34000
---

When designing logging interfaces, create flexible APIs that accommodate both standard and custom logging needs. This includes:

1. **Support custom log levels**: Don't assume only standard levels (trace, debug, info, warn, error, fatal) will be used. Always check against `logger.levels` which includes any custom levels.

2. **Allow message format customization**: Provide hooks that let users customize log message content.

3. **Enable level selection based on context**: Let users determine the appropriate log level dynamically based on runtime properties.

Example of a flexible logging interface:

```javascript
// Instead of this limited approach:
childLogger.info({ req: request }, 'incoming request')

// Provide a customization hook that gives control over both level and message:
function createRequestLogMessage(childLogger, req) {
  // User can choose log level based on request properties
  const level = req.headers['x-debug'] ? 'debug' : 'info'
  
  // User can customize the message content
  const message = `Incoming ${req.method} request to ${req.url}`
  
  // User controls both level and formatting
  childLogger[level]({ req: req, custom: true }, message)
}

// Usage
if (createRequestLogMessage) {
  createRequestLogMessage(childLogger, req)
} else {
  childLogger.info({ req: request }, 'incoming request')
}
```

This approach increases flexibility without sacrificing simplicity for common use cases.