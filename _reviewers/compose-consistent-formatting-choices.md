---
title: consistent formatting choices
description: Maintain consistent formatting and style choices throughout your codebase
  to improve readability and maintainability. This includes consistent variable syntax,
  proper quoting practices, and organized list formatting.
repository: docker/compose
label: Code Style
language: Other
comments_count: 4
repository_stars: 35858
---

Maintain consistent formatting and style choices throughout your codebase to improve readability and maintainability. This includes consistent variable syntax, proper quoting practices, and organized list formatting.

Key practices:
- Use consistent variable syntax (either always use braces `${VAR}` or don't, but be consistent within the same file/project)
- Apply consistent quoting for shell variables, especially for file paths and values that might contain spaces
- Format package lists and similar multi-item declarations one-per-line, sorted alphabetically for better maintainability

Example of good formatting:
```bash
# Consistent variable quoting
docker build -f "${DOCKERFILE}" -t "${TAG}" --target "${DOCKER_BUILD_TARGET}" .

# Well-formatted package list
RUN pip install \
    tox==2.1.1 \
    virtualenv==16.2.0
```

Consistent formatting reduces cognitive load for code reviewers and makes diffs cleaner when modifications are needed.