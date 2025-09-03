---
title: Contextual error handling
description: Implement error handling that is both architecturally localized and contextually
  specific to provide better user experience and system resilience. Use localized
  error boundaries to prevent cascading failures while ensuring error messages are
  specific to the actual problem and provide actionable guidance.
repository: lobehub/lobe-chat
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 65138
---

Implement error handling that is both architecturally localized and contextually specific to provide better user experience and system resilience. Use localized error boundaries to prevent cascading failures while ensuring error messages are specific to the actual problem and provide actionable guidance.

For architectural design, prefer localized error boundaries over relying solely on global error handlers. This allows different sections of the application to fail independently without affecting other areas, as demonstrated in the discussion: "外面是全页面的，里面加的话可以做到分区出现" (sectional error display) and "其他地方就不会挂掉" (other areas won't crash).

For error messaging, replace generic error messages with specific, actionable ones. Instead of broad messages like "请求服务出错" (service request error), use specific messages like "未找到该本地模型，请通过 Ollama 下载后重试" (model not found, please download via Ollama and retry). This helps users understand exactly what went wrong and what they can do to resolve it.

Example implementation:
```tsx
// Localized error boundary for specific feature
<ErrorBoundary fallback={<InvalidOllamaModel />}>
  <ConversationComponent />
</ErrorBoundary>

// Specific error component with actionable message
function InvalidOllamaModel() {
  return (
    <div>
      <p>未找到该本地模型，请通过 Ollama 下载后重试</p>
      <button>下载模型</button>
    </div>
  );
}
```