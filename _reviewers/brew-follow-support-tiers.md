---
title: Follow support tiers
description: 'Configure your Homebrew installation according to the defined support
  tiers to ensure optimal functionality and support. For Tier 1 support (fully supported):'
repository: Homebrew/brew
label: Configurations
language: Markdown
comments_count: 12
repository_stars: 44168
---

Configure your Homebrew installation according to the defined support tiers to ensure optimal functionality and support. For Tier 1 support (fully supported):

- Install in the default prefix (`/opt/homebrew` on Apple Silicon, `/usr/local` on Intel x86_64, `/home/linuxbrew/.linuxbrew` on Linux)
- Use officially supported Apple hardware (not Hackintosh or with OpenCore Legacy Patcher)
- Run on current macOS versions (latest and two previous versions) or supported Linux distributions
- Install on internal storage, not external drives
- Use the appropriate architecture for your platform

Non-standard configurations will receive reduced support (Tier 2 or 3) or may be entirely unsupported. When using shared dotfiles across platforms, use platform detection:

```sh
command -v brew || export PATH="/opt/homebrew/bin:/home/linuxbrew/.linuxbrew/bin:/usr/local/bin"
command -v brew && eval "$(brew shellenv)"
```