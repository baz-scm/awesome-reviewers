---
title: Bundle Static Assets
description: Avoid directly linking UI/static assets (e.g., icons, images) to external
  domains. Keep them inside the repository and reference them via local paths so builds
  don’t depend on third-party availability, reduce tracking/privacy exposure, and
  minimize supply-chain risk.
repository: mermaid-js/mermaid
label: Security
language: Other
comments_count: 1
repository_stars: 87952
---

Avoid directly linking UI/static assets (e.g., icons, images) to external domains. Keep them inside the repository and reference them via local paths so builds don’t depend on third-party availability, reduce tracking/privacy exposure, and minimize supply-chain risk.

Example (local assets instead of remote URLs):

```ts
// Instead of:
// iconUrl: 'https://static.mermaidchart.dev/assets/icon-public.svg'

import iconPublic from '@/assets/icons/icon-public.svg';
import iconTerminal from '@/assets/icons/icon-terminal.svg';
import iconWhiteboard from '@/assets/icons/icon-whiteboard.svg';

interface Feature {
  iconUrl: string;
  featureName: string;
}

const featureColumns = ref<Feature[][]>([
  [
    { iconUrl: iconPublic, featureName: 'Diagram stored in URL' },
    { iconUrl: iconTerminal, featureName: 'Code editor' },
    { iconUrl: iconWhiteboard, featureName: 'Whiteboard' },
  ],
]);
```

Apply this rule to all static resources used in the UI (icons, SVGs, logos, fonts) unless there is an explicit, approved exception with documented risk acceptance.