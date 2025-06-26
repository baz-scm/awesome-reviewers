---
title: "Write clear documentation"
description: "Documentation should be clear, precise, and self-contained while following established style conventions. When writing technical documentation, use precise language, make documentation self-contained, follow style conventions, and create accessible links."
repository: "fastify/fastify"
label: "Documentation"
language: "Markdown"
comments_count: 8
repository_stars: 34000
---

Documentation should be clear, precise, and self-contained while following established style conventions. When writing technical documentation:

1. **Use precise language**: Clearly describe how APIs work, including any restrictions or requirements.
   ```js
   // Good
   // The function must be synchronous, and must not throw an error.
   fastify.setGenReqId(function (rawReq) { return 'request-id' })
   
   // Bad
   // This function can be used to set a request ID.
   fastify.setGenReqId(function (rawReq) { return 'request-id' })
   ```

2. **Make documentation self-contained**: Include all necessary context within the document itself rather than relying on external links.
   ```js
   // Good
   // The `preHandler` hook allows you to specify a function that is executed before
   // routes' handler.
   
   // Bad
   // See Issue #1234 for more details on the preHandler hook.
   ```

3. **Follow style conventions**: 
   - Avoid using "you" in reference documentation
   - Avoid contractions in formal documentation
   - Use proper formatting for headers, lists, and code blocks
   
   ```js
   // Good
   // When request logging is enabled, request logs can be customized by
   // supplying a createRequestLogMessage() function.
   
   // Bad
   // You can customize your request logs by using a createRequestLogMessage() function.
   ```

4. **Create accessible links**: Provide meaningful context in link text rather than using generic phrases.
   ```md
   <!-- Good -->
   [TypeScript no-floating-promises configuration](https://typescript-eslint.io/rules/no-floating-promises/)
   
   <!-- Bad -->
   Click [here](https://typescript-eslint.io/rules/no-floating-promises/) for more information.
   ```