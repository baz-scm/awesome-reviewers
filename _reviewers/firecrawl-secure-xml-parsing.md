---
title: secure XML parsing
description: When configuring XML parsing options, carefully evaluate security implications
  of each setting, especially those that enable potentially risky features like DTD
  processing. Document the business justification for enabling such features and verify
  that the chosen library provides adequate protection against common XML-based attacks
  (XXE, DTD attacks, etc.).
repository: firecrawl/firecrawl
label: Security
language: Rust
comments_count: 1
repository_stars: 54535
---

When configuring XML parsing options, carefully evaluate security implications of each setting, especially those that enable potentially risky features like DTD processing. Document the business justification for enabling such features and verify that the chosen library provides adequate protection against common XML-based attacks (XXE, DTD attacks, etc.).

Example of secure XML parsing configuration:
```rust
let doc = roxmltree::Document::parse_with_options(
    xml_content,
    roxmltree::ParsingOptions { 
        allow_dtd: true, // Enable only when necessary for business requirements
        ..Default::default() 
    },
)?;
```

Always include comments explaining why potentially dangerous options are enabled and confirm the library's security guarantees against relevant attack vectors.