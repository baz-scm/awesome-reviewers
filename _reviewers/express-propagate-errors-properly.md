---
title: Propagate errors properly
description: Always forward errors to the framework's error handling pipeline instead
  of swallowing them or handling them inconsistently. This enables centralized error
  handling, consistent user experiences, and proper error logging.
repository: expressjs/express
label: Error Handling
language: JavaScript
comments_count: 5
repository_stars: 67300
---

Always forward errors to the framework's error handling pipeline instead of swallowing them or handling them inconsistently. This enables centralized error handling, consistent user experiences, and proper error logging.

**Bad practice:**
```javascript
try {
  await someAsyncOperation();
} catch (err) {
  res.status(404).json(err.message); // Direct response, bypassing error pipeline
}
```

**Good practice:**
```javascript
try {
  await someAsyncOperation();
} catch (err) {
  // Forward to Express error handling middleware
  return next(err); 
}
```

For "fire-and-forget" operations where you don't want to interrupt the main flow:
```javascript
try {
  // Non-critical operation
  await redisClient.hSet('online_users', user, now.toString());
} catch (err) {
  console.error('Error setting user activity:', err);
  // Don't call next(err) for non-critical errors
}
```

When handling streams or events, properly forward errors but be mindful of potential recursive error handling:
```javascript
inputStream.on('error', (err) => {
  // Remove handlers first to avoid recursive error handling
  inputStream.removeAllListeners();
  res.removeAllListeners('error');
  
  // Then forward the error
  next(err);
});
```

Using the error handling pipeline allows your application to:
1. Provide consistent error responses
2. Centralize error logging
3. Customize error pages based on environment (development vs production)
4. Set appropriate HTTP status codes based on error types