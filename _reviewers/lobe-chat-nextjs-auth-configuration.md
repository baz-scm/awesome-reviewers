---
title: Next.js auth configuration
description: Follow auth.js standardized environment variable naming conventions and
  use explicit function declarations for OAuth providers. Use the `AUTH_[PROVIDER_ID]_ID`
  format for environment variables as auth.js automatically reads these. Avoid deprecated
  naming patterns that will be removed in future versions. Explicitly declare scope
  and profile handling...
repository: lobehub/lobe-chat
label: Next
language: TypeScript
comments_count: 2
repository_stars: 65138
---

Follow auth.js standardized environment variable naming conventions and use explicit function declarations for OAuth providers. Use the `AUTH_[PROVIDER_ID]_ID` format for environment variables as auth.js automatically reads these. Avoid deprecated naming patterns that will be removed in future versions. Explicitly declare scope and profile handling functions rather than relying on defaults.

Example:
```typescript
// Use standardized environment variables (auto-read by auth.js)
// AUTH_FEISHU_ID=your_app_id
// AUTH_FEISHU_SECRET=your_secret

function Feishu(): OAuthConfig<FeishuProfileResponse> {
  return {
    authorization: {
      params: {
        scope: '', // Explicitly declare scope
      },
      url: 'https://accounts.feishu.cn/open-apis/authen/v1/authorize',
    },
    // Explicitly declare profile function
    profile(profileResponse) {
      const profile = profileResponse.data;
      return {
        id: profile.union_id,
        image: profile.avatar_url,
        name: profile.name,
        providerAccountId: profile.union_id,
      };
    },
    // ... other config
  };
}
```

For client-side auth components, prefer dynamic imports to optimize bundle size:
```typescript
const { signOut } = await import("next-auth/react");
```