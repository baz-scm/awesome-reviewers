---
title: Resilient UI Failure Handling
description: Make UI behavior robust to failure scenarios by aligning (a) what you
  validate, (b) what you treat as success, and (c) how state is updated when partial
  failures happen.
repository: aaif-goose/goose
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 51876
---

Make UI behavior robust to failure scenarios by aligning (a) what you validate, (b) what you treat as success, and (c) how state is updated when partial failures happen.

Apply these rules:
1) Don’t treat async work as successful until it resolves. Show success toasts only after awaiting; catch and handle rejections.
2) Avoid brittle callback chains when operations aren’t atomic. Prefer authoritative, event-driven state updates that carry enough context to remain consistent under partial failure.
3) Prevent “hidden required field” failures by gating submit and validating only the inputs that are actually rendered/required.

Example pattern:

```ts
// 1) Async success after await
const handleCopyMarkdown = async () => {
  try {
    const markdown = conversationToMarkdown(messages, session?.name);
    await navigator.clipboard.writeText(markdown);
    toast.success(intl.formatMessage(i18n.copiedMarkdown));
  } catch {
    toast.error(intl.formatMessage(i18n.copyFailed));
  }
};

// 2) Gate actions to avoid hidden required-field failures
const requiredNonOAuthKeys = /* compute required keys that are rendered */;
const canSubmit = hasOAuth ? requiredNonOAuthKeys.length > 0 : true;

// render footer only when canSubmit, and validate only those keys
const handleSubmitForm = () => validateAndSubmit(requiredNonOAuthKeys);

// 3) For multi-step updates, prefer authoritative event/state updates
// rather than relying on an 'onComplete' callback that may not fire
// when step N succeeds and step N+1 fails.
// e.g., update header from a full 'config_option_update' payload.
```