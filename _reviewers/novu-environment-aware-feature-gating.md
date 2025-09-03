---
title: Environment-aware feature gating
description: Always check environment variables, deployment modes, subscription tiers,
  and feature flags before enabling functionality or changing application behavior.
  Combine multiple configuration checks when necessary to ensure features are only
  available in appropriate contexts.
repository: novuhq/novu
label: Configurations
language: TSX
comments_count: 4
repository_stars: 37700
---

Always check environment variables, deployment modes, subscription tiers, and feature flags before enabling functionality or changing application behavior. Combine multiple configuration checks when necessary to ensure features are only available in appropriate contexts.

Key practices:
- Check environment type before enabling development-only features
- Validate subscription tiers before allowing premium functionality  
- Combine feature flags with environment checks for proper gating
- Use different behavior paths for self-hosted vs cloud deployments

Example implementation:
```typescript
// Check environment type for dev-only features
{currentEnvironment?.type === EnvironmentTypeEnum.DEV ? (
  <DevelopmentEditor />
) : (
  <ProductionView />
)}

// Combine subscription tier with feature limits
if (tier === ApiServiceLevelEnum.FREE && data?.layouts?.length >= 1) {
  return <UpgradePrompt />;
}

// Combine feature flags with deployment mode
{isWebhooksManagementEnabled && !IS_SELF_HOSTED && (
  <WebhooksSection />
)}

// Different behavior for deployment modes
{IS_SELF_HOSTED ? 'Contact Sales' : 'Upgrade to Team Tier'}
```

This approach prevents features from being exposed in inappropriate environments and ensures consistent behavior across different deployment scenarios.