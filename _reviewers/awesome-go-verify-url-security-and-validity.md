---
title: Verify URL security and validity
description: Always ensure external URLs use HTTPS when available and verify that
  links resolve correctly before including them in documentation or code. HTTP links
  expose users to potential security risks through unencrypted connections, while
  broken or incorrect URLs create poor user experience and may indicate outdated dependencies.
repository: avelino/awesome-go
label: Networking
language: Markdown
comments_count: 2
repository_stars: 151435
---

Always ensure external URLs use HTTPS when available and verify that links resolve correctly before including them in documentation or code. HTTP links expose users to potential security risks through unencrypted connections, while broken or incorrect URLs create poor user experience and may indicate outdated dependencies.

When adding external links:
1. Prefer HTTPS over HTTP for security (e.g., use `https://bit.ly/go-slack-signup` instead of `http://bit.ly/go-slack-signup`)
2. Test that URLs actually resolve to the intended resource
3. For repository links, verify the correct path (e.g., `https://github.com/anacrolix/torrent/tree/master/dht` for source code or `https://godoc.org/github.com/anacrolix/torrent/dht` for documentation)

This practice protects users from security vulnerabilities and ensures reliable access to referenced resources.