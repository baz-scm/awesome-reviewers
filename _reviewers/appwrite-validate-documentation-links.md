---
title: Validate documentation links
description: Always verify that URLs in documentation resolve correctly (return HTTP
  200) before merging changes. Broken links create a poor user experience and reduce
  the credibility of documentation.
repository: appwrite/appwrite
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 51959
---

Always verify that URLs in documentation resolve correctly (return HTTP 200) before merging changes. Broken links create a poor user experience and reduce the credibility of documentation.

For important user-facing documents like README files, include a verification step in your review process:

```shell
#!/bin/bash
# Simple script to verify a documentation link
curl -I https://example.com/your/documentation/link | head -n 1
# Should return HTTP/1.1 200 OK
```

If a link points to content that's not yet published (like upcoming blog posts), either:
1. Wait to merge until the content is live
2. Remove the link to avoid broken references
3. Update with a correct alternative URL

This verification is especially important for prominent links in README files or other entry-point documentation that will be immediately visible to users.