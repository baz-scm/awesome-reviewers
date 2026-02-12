---
title: centralize configuration values
description: 'Keep layout constants, feature flags, and user-configurable settings
  in centralized configuration modules (not hardcoded in components). Motivation:
  makes it easy to find and change UI "magic" values (e.g., tab width, spacing) and
  ensures behavior can be toggled per-environment or per-user (e.g., suppressing update
  banners when users turn off update checks).'
repository: wavetermdev/waveterm
label: Configurations
language: TSX
comments_count: 2
repository_stars: 17328
---

Keep layout constants, feature flags, and user-configurable settings in centralized configuration modules (not hardcoded in components). Motivation: makes it easy to find and change UI "magic" values (e.g., tab width, spacing) and ensures behavior can be toggled per-environment or per-user (e.g., suppressing update banners when users turn off update checks).

How to apply:
- Create dedicated config files (examples: magiclayout.ts, featureflags.ts, clientConfig.ts) and export named values.
- Import those values in components instead of declaring local constants or conditionals.
- Respect user settings and feature flags when rendering UI; surface updates only via agreed channels if the corresponding setting is disabled.

Examples:
- Move tab width into magiclayout.ts:
  // magiclayout.ts
  export const TAB_WIDTH = 175;

  // tabs.tsx
  import { TAB_WIDTH } from '../../config/magiclayout';

- Check a user setting before showing an update sidebar entry:
  // clientConfig.ts (runtime/user settings)
  export const clientConfig = {
    checkForUpdates: true, // toggled by user
  };

  // sidebar.tsx
  import { clientConfig } from '../../config/clientConfig';
  ...
  {clientConfig.checkForUpdates && clientData?.releaseinfo?.releaseavailable && (
    <If condition>
      ...update banner...
    </If>
  )}

Notes:
- Keep config modules focused and discoverable (group layout constants together, feature flags together).
- Allow environment/user overrides (env vars, persisted settings) and document intent so components remain declarative and testable.