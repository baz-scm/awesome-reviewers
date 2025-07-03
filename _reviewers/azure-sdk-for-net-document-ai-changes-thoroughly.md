---
title: Document AI changes thoroughly
description: When updating AI libraries and SDKs, ensure all changes are thoroughly
  documented in changelogs with clear categorizations (Features Added, Breaking Changes)
  and explicit migration paths for breaking changes. For complex AI features, include
  links to detailed documentation.
repository: Azure/azure-sdk-for-net
label: AI
language: Markdown
comments_count: 2
repository_stars: 5809
---

When updating AI libraries and SDKs, ensure all changes are thoroughly documented in changelogs with clear categorizations (Features Added, Breaking Changes) and explicit migration paths for breaking changes. For complex AI features, include links to detailed documentation.

Example of good documentation:
```markdown
## 1.1.0-beta.3 (2025-06-27)

### Features Added
- Tracing for Agents. More information [here](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Agents.Persistent/README.md#tracing).
- Automatically function toolcalls. More information [here](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Agents.Persistent/README.md#function-call-executed-automatically).

### Breaking Changes
- Support for project connection string and hub-based projects has been discontinued. 
  We recommend creating a new Azure AI Foundry resource utilizing project endpoint. 
  If this is not possible, please pin the version to `1.0.0-beta.8` or earlier.
```

For AI systems where behavior might not be immediately intuitive (like automatic function execution or new endpoint requirements), clear documentation helps users understand system capabilities and limitations, and reduces integration challenges.
