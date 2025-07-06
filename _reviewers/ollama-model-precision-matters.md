---
title: Model precision matters
description: When deploying AI models on specialized hardware accelerators (GPUs,
  NPUs), ensure you're using compatible model precision formats. Different hardware
  platforms have different optimal precision requirements that significantly impact
  performance and compatibility.
repository: ollama/ollama
label: AI
language: Shell
comments_count: 2
repository_stars: 145705
---

When deploying AI models on specialized hardware accelerators (GPUs, NPUs), ensure you're using compatible model precision formats. Different hardware platforms have different optimal precision requirements that significantly impact performance and compatibility.

For example, when working with Ascend NPUs, fp16 models often work better than higher precision formats:

```bash
# When compiling AI frameworks for Ascend NPUs
export CUSTOM_CPU_FLAGS=cann
make --no-print-directory -f make/Makefile.cann

# When running models, verify hardware is properly detected
./ollama serve  # Should show detected NPUs in logs
# If models run on CPU despite hardware detection, try fp16 model variants
./ollama run model-name-f16  # Explicitly use fp16 version
```

Even when hardware is properly detected, models may still default to CPU execution if precision formats are incompatible with the acceleration hardware. Always test multiple precision variants (fp16, fp32, int8) to determine the optimal configuration for your target hardware.