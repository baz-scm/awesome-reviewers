---
title: Update documentation configuration
description: When adding new files or components to the project, ensure that documentation
  configuration is updated accordingly. This includes adding new files to TypeDoc
  options in tsconfig.json to maintain complete API documentation coverage. Additionally,
  clearly mark deprecated components and direct developers to use the recommended
  alternatives instead of extending...
repository: langchain-ai/langchainjs
label: Documentation
language: Json
comments_count: 2
repository_stars: 15004
---

When adding new files or components to the project, ensure that documentation configuration is updated accordingly. This includes adding new files to TypeDoc options in tsconfig.json to maintain complete API documentation coverage. Additionally, clearly mark deprecated components and direct developers to use the recommended alternatives instead of extending deprecated functionality.

Example:
```javascript
// When adding a new file like document_loaders/fs/md.ts
// Remember to update the TypeDoc configuration in tsconfig.json:

"typedocOptions": {
  "entryPoints": [
    // existing entries
    "document_loaders/fs/md.ts"
  ]
}

// For deprecated components, add clear documentation:
/**
 * @deprecated This entrypoint is deprecated. 
 * Please use the community integration instead.
 */
```

This practice ensures comprehensive documentation coverage and provides clear guidance for developers, preventing them from extending deprecated features and helping them locate the proper integration points for new functionality.


[
  {
    "discussion_id": "1605436319",
    "pr_number": 5418,
    "pr_file": "langchain/package.json",
    "created_at": "2024-05-17T19:01:11+00:00",
    "commented_code": null,
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1605436319",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 5418,
        "pr_file": "langchain/package.json",
        "discussion_id": "1605436319",
        "commented_code": null,
        "comment_created_at": "2024-05-17T19:01:11+00:00",
        "comment_author": "bracesproul",
        "comment_body": "The langchain entrypoint is deprecated, so we shouldn't be adding more features to it. Only add to the community integration",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1189846834",
    "pr_number": 1192,
    "pr_file": "langchain/package.json",
    "created_at": "2023-05-10T12:37:04+00:00",
    "commented_code": "\"document_loaders/fs/csv.cjs\",\n    \"document_loaders/fs/csv.js\",\n    \"document_loaders/fs/csv.d.ts\",\n    \"document_loaders/fs/md.cjs\",",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "1189846834",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 1192,
        "pr_file": "langchain/package.json",
        "discussion_id": "1189846834",
        "commented_code": "@@ -199,6 +199,9 @@\n     \"document_loaders/fs/csv.cjs\",\n     \"document_loaders/fs/csv.js\",\n     \"document_loaders/fs/csv.d.ts\",\n+    \"document_loaders/fs/md.cjs\",",
        "comment_created_at": "2023-05-10T12:37:04+00:00",
        "comment_author": "dqbd",
        "comment_body": "Consider adding `document_loaders/fs/md.ts` in `typedocOptions` found in `tsconfig.json`",
        "pr_file_module": null
      }
    ]
  }
]
