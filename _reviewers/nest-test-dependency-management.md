---
title: Test dependency management
description: Testing tools and libraries should be placed in `devDependencies` rather
  than regular dependencies in package.json. Regularly review testing dependencies
  to identify and remove outdated or redundant packages. For example, if a newer testing
  tool now includes functionality previously provided by a separate package (like
  'nyc' now depending on...
repository: nestjs/nest
label: Testing
language: Json
comments_count: 2
repository_stars: 71767
---

Testing tools and libraries should be placed in `devDependencies` rather than regular dependencies in package.json. Regularly review testing dependencies to identify and remove outdated or redundant packages. For example, if a newer testing tool now includes functionality previously provided by a separate package (like 'nyc' now depending on 'istanbul-lib-coverage' instead of 'istanbul'), remove the redundant dependency.

```json
// Good practice:
"devDependencies": {
  "nunjucks": "^3.2.1",  // For integration tests
  "nyc": "^15.0.0"       // Uses istanbul-lib-coverage internally
}

// Avoid:
"dependencies": {
  "nunjucks": "^3.2.1"   // Wrong place for testing tools
},
"devDependencies": {
  "istanbul": "^0.4.5",  // Redundant with nyc
}
```