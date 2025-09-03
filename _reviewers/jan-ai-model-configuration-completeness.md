---
title: AI model configuration completeness
description: Ensure all necessary AI model parameters are properly configured and
  passed through the system. AI models require comprehensive configuration including
  hardware settings (CPU/GPU allocation, thread counts), model-specific parameters
  (context length, n_gpu_layers), and proper path resolution. Missing configuration
  can lead to runtime failures, suboptimal...
repository: menloresearch/jan
label: AI
language: TypeScript
comments_count: 4
repository_stars: 37620
---

Ensure all necessary AI model parameters are properly configured and passed through the system. AI models require comprehensive configuration including hardware settings (CPU/GPU allocation, thread counts), model-specific parameters (context length, n_gpu_layers), and proper path resolution. Missing configuration can lead to runtime failures, suboptimal performance, or initialization errors.

Key requirements:
- Include hardware settings: CPU threads, GPU layers (ngl), memory allocation
- Specify model parameters: context length (ctx_len), prompt templates, embedding settings  
- Use proper path resolution instead of hardcoded paths
- Validate configuration completeness before model initialization

Example of complete model configuration:
```typescript
const modelSettings = {
  llama_model_path: await joinPath([modelsDir, model.id]),
  ctx_len: model.settings.ctx_len || 2048,
  ngl: model.settings.ngl || 100,
  cpu_threads: nitroResourceProbe.numCpuPhysicalCore,
  prompt_template: model.settings.prompt_template,
  embedding: true
};

// Validate before initialization
if (!modelSettings.llama_model_path || !modelSettings.cpu_threads) {
  throw new Error('Incomplete model configuration');
}
```

This prevents critical issues like models failing to load due to missing parameters or processes spawning before proper configuration is established.