---
title: maintain proper formatting
description: Ensure code and configuration files follow proper formatting standards
  that maintain both syntactic validity and visual readability. This includes correct
  indentation for nested structures and appropriate line length management to prevent
  horizontal scrolling.
repository: serverless/serverless
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 46810
---

Ensure code and configuration files follow proper formatting standards that maintain both syntactic validity and visual readability. This includes correct indentation for nested structures and appropriate line length management to prevent horizontal scrolling.

For nested structures like YAML, maintain consistent indentation for all properties at the same level:

```yaml
# Correct - all properties properly indented
events:
  - serviceBus:
      name: item
      queueName: myqueue
      connection: myconnection

# Incorrect - inconsistent indentation
events:
  - serviceBus:
    name: item  # Wrong indentation level
      queueName: myqueue
```

For long commands or statements, use line continuation to improve readability:

```sh
# Good - broken into readable lines
$ serverless create \
  -u https://github.com/serverless/examples/tree/master/folder-name \
  -n my-project

# Avoid - causes horizontal scrolling
$ serverless create -u https://github.com/serverless/examples/tree/master/folder-name -n my-project
```

Always validate formatting using appropriate tools (YAML validators, linters) to ensure syntactic correctness alongside visual clarity.