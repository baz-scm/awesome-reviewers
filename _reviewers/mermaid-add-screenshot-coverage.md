---
title: Add screenshot coverage
description: When adding a new rendering demo or introducing a new configuration/YAML
  option, always update the relevant Cypress integration/screenshot tests so the feature
  is exercised and captured automatically.
repository: mermaid-js/mermaid
label: Testing
language: Html
comments_count: 2
repository_stars: 87952
---

When adding a new rendering demo or introducing a new configuration/YAML option, always update the relevant Cypress integration/screenshot tests so the feature is exercised and captured automatically.

How to apply:
- Find the closest existing rendering/screenshot spec for the feature (e.g., the flowchart v2 rendering spec).
- Add a new `it(...)` case (or extend an existing one) that uses a snapshot helper to render the diagram source plus the exact config/front-matter that the demo uses.
- Ensure the test covers the new behavior/input (e.g., spacing options like `nodeSpacing`/`rankSpacing`, or new YAML config fields like `themeVariables`).

Example pattern (Cypress + snapshot):
```ts
it('Should render subgraphs with different nodeSpacing', () => {
  imgSnapshotTest(`---
title: Subgraph nodeSpacing and rankSpacing example
---
flowchart LR
  X --> Y
  subgraph X
    direction LR
    A
    C
  end
  subgraph Y
    direction LR
    B
    D
  end
`, {
    flowchart: { nodeSpacing: 1, rankSpacing: 1 },
  });
});

// And for new YAML config options:
imgSnapshotTest(`---
config:
  theme: base
  themeVariables:
    lineColor: yellow
---
flowchart LR
subgraph red
A --> B
end
`, {});
```
This keeps automated visual/regression coverage aligned with every user-visible change and every supported config surface.