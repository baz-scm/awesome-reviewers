---
title: validate SVG security context
description: SVG files can execute code when loaded, making them a potential security
  vulnerability. Before using SVGs, evaluate the deployment context and security requirements.
  Different environments have different restrictions - for example, VS Code marketplace
  prohibits user-provided SVGs due to security concerns, while webview-hosted SVGs
  may be acceptable. When...
repository: cline/cline
label: Security
language: Other
comments_count: 1
repository_stars: 48299
---

SVG files can execute code when loaded, making them a potential security vulnerability. Before using SVGs, evaluate the deployment context and security requirements. Different environments have different restrictions - for example, VS Code marketplace prohibits user-provided SVGs due to security concerns, while webview-hosted SVGs may be acceptable. When SVGs pose security risks, consider safer alternatives like base64-encoded images or icon pack fonts. Be especially cautious with user-provided SVG content that could be modified to contain malicious code.

Example of context-aware SVG handling:
```typescript
// Risky: User-provided SVG for marketplace
const userSvg = getUserProvidedSvg(); // Could contain malicious code

// Safer alternatives:
const base64Image = convertToBase64(imageFile);
const iconFont = registerIconPackFont();
const controlledSvg = getStaticSvgFromAssets(); // Known safe content
```