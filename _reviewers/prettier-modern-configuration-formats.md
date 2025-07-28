---
title: Modern configuration formats
description: Prefer ES module configuration files with TypeScript annotations over
  JSON formats for better developer experience and tooling support. Use `.js` or `.mjs`
  extensions with proper type annotations to enable IDE autocompletion and type safety.
repository: prettier/prettier
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 50772
---

Prefer ES module configuration files with TypeScript annotations over JSON formats for better developer experience and tooling support. Use `.js` or `.mjs` extensions with proper type annotations to enable IDE autocompletion and type safety.

When creating configuration files, especially shared configurations:

1. **Use ES modules instead of JSON**: Choose `prettier.config.js` or `index.js` over `.prettierrc.json` to support dynamic imports and better tooling integration.

2. **Add TypeScript annotations**: Include `/** @type {import("prettier").Config} */` at the top of configuration files to enable IDE autocompletion and type checking.

3. **Set proper package.json fields**: Use `"type": "module"` and `"exports": "./index.js"` for modern module resolution.

4. **Install types as devDependency**: Add `prettier` as a devDependency to support TypeScript annotations.

Example configuration:

```js
/** @type {import("prettier").Config} */
const config = {
  trailingComma: "es5",
  tabWidth: 4,
  singleQuote: true,
};

export default config;
```

Example package.json for shared configs:

```json
{
  "name": "@username/prettier-config",
  "type": "module",
  "exports": "./index.js",
  "devDependencies": {
    "prettier": "^3.3.3"
  }
}
```

This approach provides better IDE support, enables dynamic configuration, and follows modern JavaScript standards while maintaining compatibility with tools like vscode-prettier.