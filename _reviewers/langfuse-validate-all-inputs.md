---
title: Validate all inputs
description: All user-controlled inputs must be validated and sanitized before use
  to prevent injection attacks, unauthorized access, and other security vulnerabilities.
  This includes query parameters, environment variables, URLs, and database values.
repository: langfuse/langfuse
label: Security
language: TypeScript
comments_count: 5
repository_stars: 13574
---

All user-controlled inputs must be validated and sanitized before use to prevent injection attacks, unauthorized access, and other security vulnerabilities. This includes query parameters, environment variables, URLs, and database values.

When handling user inputs:
1. **Validate structure and type**: Use schema validation libraries like Zod to enforce expected formats
   ```typescript
   // Validate URL parameters
   baseUrl: z.string().url(),
   
   // Validate security-related environment variables
   LANGFUSE_S3_EVENT_UPLOAD_SSE: z.enum(["AES256", "aws:kms"]).optional(),
   ```

2. **Parameterize database queries**: Never directly interpolate user input into queries
   ```typescript
   // INSECURE: Using string interpolation 
   Prisma.sql`AND ${model} ~ match_pattern`
   
   // SECURE: Using parameterized queries
   Prisma.sql`AND $1 ~ match_pattern`, model
   ```

3. **Validate before use**: Always validate input before using it in sensitive operations
   ```typescript
   // Validate query parameters
   if (!id || typeof id !== 'string') {
     return res.status(400).json({ error: 'Valid ID required' });
   }
   ```

Proper input validation is your first line of defense against many common security vulnerabilities including SQL injection, XSS, CSRF, and path traversal attacks.