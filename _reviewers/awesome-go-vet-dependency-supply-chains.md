---
title: Vet dependency supply chains
description: 'When adding new dependencies, especially security-related ones, thoroughly
  evaluate them for supply chain attack risks. Look for red flags such as: repositories
  with many empty or automated commits, lack of transparent build processes (prefer
  GitHub Actions over opaque automation), use of unofficial forks instead of original
  packages, and suspicious account...'
repository: avelino/awesome-go
label: Security
language: Markdown
comments_count: 1
repository_stars: 151435
---

When adding new dependencies, especially security-related ones, thoroughly evaluate them for supply chain attack risks. Look for red flags such as: repositories with many empty or automated commits, lack of transparent build processes (prefer GitHub Actions over opaque automation), use of unofficial forks instead of original packages, and suspicious account activity patterns.

Before accepting any dependency, verify:
- The repository has a clean commit history with meaningful changes
- Build and release processes are transparent and auditable  
- Official packages are used rather than forks when available
- The maintainer account shows legitimate development patterns

Example of concerning patterns to reject:
```
// Red flags identified in review:
- Empty commits: "c1a4854ffb9e83f903469490b44d640f233889c8"
- Account automation without visible GitHub Actions
- Packaging unofficial Go fork of asciinema instead of official version
- Underlying tracker with suspicious commit patterns
```

Supply chain attacks are a critical security vector - taking time to properly vet dependencies protects the entire ecosystem from potential compromise.