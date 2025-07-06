---
title: Complete documentation coverage
description: 'Documentation should comprehensively cover all supported options, variations,
  and potential future use cases. When creating documentation:


  1. Use generic titles and structures that can accommodate future additions'
repository: ollama/ollama
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 145705
---

Documentation should comprehensively cover all supported options, variations, and potential future use cases. When creating documentation:

1. Use generic titles and structures that can accommodate future additions
   - Example: Instead of "AMD iGPU 780m Guide", use "AMD iGPU Guide" to allow for documenting additional GPU models

2. Include examples for all supported options and environments
   - Example: When documenting shell commands, provide examples for all supported shells:
   ```
   # For bash
   echo "source <(ollama completion bash)" >> ~/.bashrc
   
   # For zsh
   echo "source <(ollama completion zsh)" >> ~/.zshrc
   
   # For fish
   ollama completion fish > ~/.config/fish/completions/ollama.fish
   ```

3. Document complete workflows from beginning to end

4. Verify that all links are current and functional

Comprehensive documentation reduces the need for clarifications, helps users across different environments, and ensures documentation remains relevant as software evolves.