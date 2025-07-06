---
title: Verify documentation links
description: 'Always ensure external links in documentation are valid, secure, and
  point to authoritative sources. This includes:


  1. Use HTTPS instead of HTTP links for security'
repository: octokit/octokit.net
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 2793
---

Always ensure external links in documentation are valid, secure, and point to authoritative sources. This includes:

1. Use HTTPS instead of HTTP links for security
2. Verify that anchors within links actually exist at the destination
3. Link to official repositories and documentation rather than personal sites
4. Test all links before committing documentation changes

For example, instead of:
```markdown
Check out [this guide](http://personal-blog.com/outdated-page#non-existent-section) for more information.
```

Use:
```markdown
Check out [the official documentation](https://github.com/organization/project/blob/main/docs/guide.md#relevant-section) for more information.
```

Broken or insecure links reduce the credibility of documentation and create frustrating experiences for users. Regular verification of links ensures documentation remains reliable and trustworthy over time.