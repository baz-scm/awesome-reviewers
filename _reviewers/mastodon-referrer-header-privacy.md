---
title: referrer header privacy
description: When implementing features that link to external sites, carefully consider
  referrer policies to prevent unintended disclosure of sensitive information about
  users or the origin server. HTTP referrer headers can inadvertently expose details
  about what type of community, instance, or service users belong to, which may have
  privacy or safety implications.
repository: mastodon/mastodon
label: Security
language: Yaml
comments_count: 1
repository_stars: 48691
---

When implementing features that link to external sites, carefully consider referrer policies to prevent unintended disclosure of sensitive information about users or the origin server. HTTP referrer headers can inadvertently expose details about what type of community, instance, or service users belong to, which may have privacy or safety implications.

This is particularly important in contexts where the origin server URL itself reveals sensitive information about users' identities, affiliations, or communities. For example, users from specialized community servers (LGBTQ+, political, religious, etc.) could be inadvertently "outed" when clicking external links if the referrer header reveals their origin server.

Consider implementing referrer policies like `no-referrer` or `same-origin` for external links, and provide configuration options to allow administrators to control this behavior based on their community's privacy needs.

Example configuration approach:
```yaml
# config/locales/en.yml
allow_referrer_origin:
  desc: When your users click links to external sites, their browser may send the address of your server as the referrer. Disable this if this would uniquely identify your users, e.g. if this is a personal server.
```