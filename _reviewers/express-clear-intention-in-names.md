---
title: Clear intention in names
description: Choose names that clearly communicate intention and follow established
  conventions. This applies to variables, functions, methods, and architectural components.
repository: expressjs/express
label: Naming Conventions
language: JavaScript
comments_count: 7
repository_stars: 67300
---

Choose names that clearly communicate intention and follow established conventions. This applies to variables, functions, methods, and architectural components.

**Key practices:**

1. Follow architectural naming patterns (e.g., Controller-Service-Repository)
   ```javascript
   // Instead of:
   function NotesUseCase(notesRepository) { ... }
   
   // Prefer:
   function NotesService(notesRepository) { ... }
   ```

2. Use explicit function names rather than anonymous expressions
   ```javascript
   // Instead of:
   var proto = module.exports = function(options) { ... }
   
   // Prefer:
   function router(options) { ... }
   module.exports = router;
   ```

3. Choose distinct names for properties and methods to prevent confusion
   ```javascript
   // Confusing - same name used for different purposes:
   app.router = function() { ... }  // Method
   this.router = new Router();      // Property
   
   // Better - clearly distinguished names:
   app.createRouter = function() { ... }  // Method
   this._router = new Router();           // Property
   ```

4. Use prefixes (like underscore) to indicate private members
   ```javascript
   // No visibility indication:
   this.cache = Object.create(null);
   
   // With visibility indication:
   this._cache = Object.create(null);
   ```

5. Avoid names that could be misinterpreted for other common patterns
   ```javascript
   // Potentially confusing:
   app.dispatch = function(res, event, args) { ... }
   
   // More descriptive of actual purpose:
   app.dispatchEvent = function(res, event, args) { ... }
   ```

6. Choose descriptive names over abbreviated ones
   ```javascript
   // Unclear abbreviation:
   res.addTmplVars(options);
   
   // More descriptive:
   res.addTemplateVariables(options);
   ```

Consistently following these naming conventions improves code readability, maintainability, and helps prevent confusion among team members.