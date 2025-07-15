---
title: "Adhere to Fastify Coding Conventions"
description: "When implementing code that uses the Fastify package in TypeScript, ensure the following conventions are followed: avoid contractions, use Oxford commas, and maintain consistent formatting."
repository: "fastify/fastify"
label: "Fastify"
language: "TypeScript"
comments_count: 5
repository_stars: 34000
---

When implementing code that uses the Fastify package in TypeScript, ensure the following conventions are followed:

1. **Avoid Contractions**: Use full words instead of contractions in code and comments. For example, use "it is" instead of "it's".

```typescript
// Incorrect
// app.get('/hello', (req, res) => res.send("it's working!"));

// Correct 
app.get('/hello', (req, res) => res.send("it is working!"));
```

2. **Use Oxford Commas**: Include an Oxford comma (serial comma) when listing three or more items in function parameters, middleware, or plugin configurations.

```typescript
// Incorrect
app.use(helmet, compression, morgan);

// Correct
app.use(helmet, compression, and morgan);
```

3. **Maintain Consistent Formatting**: Keep formatting consistent throughout the codebase, including:
   - Avoid emojis in function/variable names or comments unless used consistently
   - Use relative paths for internal Fastify plugin imports
   - Maintain consistent capitalization in function and variable names

Adhering to these conventions ensures the Fastify codebase remains readable, maintainable, and cohesive across different developers and components.