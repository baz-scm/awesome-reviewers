---
title: Consistent error patterns
description: 'Implement consistent error handling patterns throughout your codebase
  to improve readability and maintainability.


  **Key guidelines:**


  1. Use named error variables instead of inline error creation'
repository: gin-gonic/gin
label: Error Handling
language: Go
comments_count: 4
repository_stars: 83022
---

Implement consistent error handling patterns throughout your codebase to improve readability and maintainability.

**Key guidelines:**

1. Use named error variables instead of inline error creation
   ```go
   // Instead of
   return errors.New("invalid request")
   
   // Use
   var ErrInvalidRequest = errors.New("invalid request")
   return ErrInvalidRequest
   ```

2. Add explicit returns after error handling to avoid nested conditionals and improve readability
   ```go
   // Instead of
   if err != nil {
       c.JSON(http.StatusInternalServerError, gin.H{
           "error": err.Error(),
       })
   } else {
       c.JSON(http.StatusOK, gin.H{
           "result": data,
       })
   }
   
   // Use
   if err != nil {
       c.JSON(http.StatusInternalServerError, gin.H{
           "error": err.Error(),
       })
       return
   }
   c.JSON(http.StatusOK, gin.H{
       "result": data,
   })
   ```

3. Reduce duplication in error handling by separating decision logic from response actions
   ```go
   // Instead of duplicating similar code
   if errors.As(err, &maxBytesErr) {
       c.AbortWithError(http.StatusRequestEntityTooLarge, err).SetType(ErrorTypeBind)
   } else {
       c.AbortWithError(http.StatusBadRequest, err).SetType(ErrorTypeBind)
   }
   
   // Use
   var statusCode int
   switch {
   case errors.As(err, &maxBytesErr):
       statusCode = http.StatusRequestEntityTooLarge
   default:
       statusCode = http.StatusBadRequest
   }
   c.AbortWithError(statusCode, err).SetType(ErrorTypeBind)
   ```

Consistent error handling patterns make code more predictable, reduce bugs, and make it easier for other developers to understand error flows.