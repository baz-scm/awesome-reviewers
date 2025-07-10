---
title: Comprehensive authentication notifications
description: Authentication notifications must include specific context about the
  triggering action, clear instructions for legitimate use, expiration details, and
  explicit steps to take if the action was unauthorized. This enhances security by
  helping users identify potential account compromises and take appropriate action.
repository: getsentry/sentry
label: Security
language: Html
comments_count: 1
repository_stars: 41297
---

Authentication notifications must include specific context about the triggering action, clear instructions for legitimate use, expiration details, and explicit steps to take if the action was unauthorized. This enhances security by helping users identify potential account compromises and take appropriate action.

Example:
```html
<p>You've initiated an account merger which requires verification. Please use the code below to confirm:</p>
<p>{{code}}</p>
<p>This code expires in 30 minutes.</p>
<p>If you didn't attempt this action, please secure your account immediately and contact support@sentry.io.</p>
```

Rather than the less secure alternative:
```html
<p>Here is the verification code you requested. It expires in 30 minutes.</p>
<p>{{code}}</p>
<p>If you weren't expecting this email, please ignore it.</p>
```