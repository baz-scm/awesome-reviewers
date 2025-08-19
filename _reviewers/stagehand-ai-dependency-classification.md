---
title: AI dependency classification
description: When adding AI/ML libraries to a project, carefully consider whether
  they belong in `dependencies` or `devDependencies`. Libraries used for examples,
  experimentation, or development tooling should be classified as `devDependencies`
  to avoid bloating production bundles. Maintain consistency by avoiding install scripts
  in package.json for dev-only AI...
repository: browserbase/stagehand
label: AI
language: Json
comments_count: 2
repository_stars: 16443
---

When adding AI/ML libraries to a project, carefully consider whether they belong in `dependencies` or `devDependencies`. Libraries used for examples, experimentation, or development tooling should be classified as `devDependencies` to avoid bloating production bundles. Maintain consistency by avoiding install scripts in package.json for dev-only AI libraries.

Example:
```json
// Correct - AI libraries for examples/development
"devDependencies": {
  "@langchain/core": "^0.3.40",
  "@langchain/openai": "^0.4.4"
}

// Avoid install scripts for dev dependencies
"scripts": {
  "example": "npm run build-dom-scripts && tsx examples/example.ts"
  // Not: "langchain": "npm install @langchain/core @langchain/openai && ..."
}
```

This ensures production deployments only include necessary AI dependencies while keeping development and example code properly isolated.