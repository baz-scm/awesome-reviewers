---
title: Follow standard naming
description: "Use established naming patterns and correct capitalization throughout\
  \ the codebase and documentation. \n\nFor test fixtures and recordings, follow common\
  \ conventions like `__snapshots__` instead of custom directory names:"
repository: langchain-ai/langchainjs
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 15004
---

Use established naming patterns and correct capitalization throughout the codebase and documentation. 

For test fixtures and recordings, follow common conventions like `__snapshots__` instead of custom directory names:

```javascript
// Preferred
// store test recordings in __snapshots__ directory
const testData = require('./__snapshots__/test-response.json');

// Avoid
// using custom or inconsistent directory names
const testData = require('./__data__/test-response.json');
```

For product and technology names, use proper capitalization and complete names:

```markdown
// Correct
# Oracle AI Vector Search with LangChain.js Integration

// Incorrect
# Oracle Vector Search with LangchainJS Integration
```

Consistent naming improves readability, maintainability, and shows professionalism in your code and documentation.


[
  {
    "discussion_id": "2169419919",
    "pr_number": 8416,
    "pr_file": "internal/net-mocks/README.md",
    "created_at": "2025-06-26T16:10:00+00:00",
    "commented_code": "# @langchain/net-mocks\n\nThis is an internal utility used within LangChain to record & mock network activity for use in tests. Here's how it works:\n\n1. **Record:** When running tests for the first time, `net-mocks` intercepts outgoing HTTP requests and records them, along with the corresponding responses, into a `.har` file. These files are stored in a `__data__` directory (by default) alongside the tests.",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2169419919",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8416,
        "pr_file": "internal/net-mocks/README.md",
        "discussion_id": "2169419919",
        "commented_code": "@@ -0,0 +1,107 @@\n+# @langchain/net-mocks\n+\n+This is an internal utility used within LangChain to record & mock network activity for use in tests. Here's how it works:\n+\n+1. **Record:** When running tests for the first time, `net-mocks` intercepts outgoing HTTP requests and records them, along with the corresponding responses, into a `.har` file. These files are stored in a `__data__` directory (by default) alongside the tests.",
        "comment_created_at": "2025-06-26T16:10:00+00:00",
        "comment_author": "dqbd",
        "comment_body": "_nit_: should we follow the `__snapshots__` convention instead? ",
        "pr_file_module": null
      },
      {
        "comment_id": "2169436990",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8416,
        "pr_file": "internal/net-mocks/README.md",
        "discussion_id": "2169419919",
        "commented_code": "@@ -0,0 +1,107 @@\n+# @langchain/net-mocks\n+\n+This is an internal utility used within LangChain to record & mock network activity for use in tests. Here's how it works:\n+\n+1. **Record:** When running tests for the first time, `net-mocks` intercepts outgoing HTTP requests and records them, along with the corresponding responses, into a `.har` file. These files are stored in a `__data__` directory (by default) alongside the tests.",
        "comment_created_at": "2025-06-26T16:20:09+00:00",
        "comment_author": "hntrl",
        "comment_body": "~~I called it `__data__` since that's what we call it in the few other places where we have mocking in langchain today (google packages are probably the best example). I won't die on this hill if you think this is better though~~\r\n\r\nnvm I like snapshots more",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2099212550",
    "pr_number": 8007,
    "pr_file": "cookbook/oraclevs.md",
    "created_at": "2025-05-21T03:06:47+00:00",
    "commented_code": "# Oracle AI Vector Search with LangchainJS Integration",
    "repo_full_name": "langchain-ai/langchainjs",
    "discussion_comments": [
      {
        "comment_id": "2099212550",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8007,
        "pr_file": "cookbook/oraclevs.md",
        "discussion_id": "2099212550",
        "commented_code": "@@ -0,0 +1,273 @@\n+# Oracle AI Vector Search with LangchainJS Integration",
        "comment_created_at": "2025-05-21T03:06:47+00:00",
        "comment_author": "cjbj",
        "comment_body": "It would be nice to use the correct product name ",
        "pr_file_module": null
      },
      {
        "comment_id": "2101482613",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8007,
        "pr_file": "cookbook/oraclevs.md",
        "discussion_id": "2099212550",
        "commented_code": "@@ -0,0 +1,273 @@\n+# Oracle AI Vector Search with LangchainJS Integration",
        "comment_created_at": "2025-05-22T02:09:37+00:00",
        "comment_author": "hackerdave",
        "comment_body": "Not sure if you are referring to Oracle AI Vector Search? This is how the feature is being referred to, e.g., https://www.oracle.com/database/ai-vector-search/ and https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/overview-ai-vector-search.html. However, did change other places where we referred to Oracle as Oracle Database.",
        "pr_file_module": null
      },
      {
        "comment_id": "2101494767",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8007,
        "pr_file": "cookbook/oraclevs.md",
        "discussion_id": "2099212550",
        "commented_code": "@@ -0,0 +1,273 @@\n+# Oracle AI Vector Search with LangchainJS Integration",
        "comment_created_at": "2025-05-22T02:21:55+00:00",
        "comment_author": "cjbj",
        "comment_body": "What is \"LangchainJS\"? Did you mean LangChain or perhaps LangChain.js or something else?",
        "pr_file_module": null
      },
      {
        "comment_id": "2102580670",
        "repo_full_name": "langchain-ai/langchainjs",
        "pr_number": 8007,
        "pr_file": "cookbook/oraclevs.md",
        "discussion_id": "2099212550",
        "commented_code": "@@ -0,0 +1,273 @@\n+# Oracle AI Vector Search with LangchainJS Integration",
        "comment_created_at": "2025-05-22T13:34:36+00:00",
        "comment_author": "hackerdave",
        "comment_body": "In this case LangChain.js. Changed all to proper case so they should be either LangChain or LangChain.js",
        "pr_file_module": null
      }
    ]
  }
]
