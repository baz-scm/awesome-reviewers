---
title: secure authentication flows
description: Authentication flows should be designed to provide a seamless user experience
  while maintaining security standards. Avoid implementing temporary workarounds that
  require users to perform multiple steps, quit and restart applications, or follow
  complex sequences to authenticate successfully.
repository: google-gemini/gemini-cli
label: Security
language: TSX
comments_count: 1
repository_stars: 65062
---

Authentication flows should be designed to provide a seamless user experience while maintaining security standards. Avoid implementing temporary workarounds that require users to perform multiple steps, quit and restart applications, or follow complex sequences to authenticate successfully.

When designing OAuth or other authentication mechanisms, especially in CLI or no-browser environments, ensure the flow can be completed in a single session without requiring application restarts or complex user interactions. Poor authentication UX often leads to user frustration and may encourage insecure workarounds.

Example of what to avoid:
```typescript
if (
  settings.merged.selectedAuthType === AuthType.LOGIN_WITH_GOOGLE &&
  config.getNoBrowser()
) {
  // This requires users to: select auth type, quit, restart app
  await getOauthClient(settings.merged.selectedAuthType, config);
}
```

Instead, design authentication flows that can handle the complete process in one session, with clear user guidance and fallback options that don't compromise security or require application restarts.