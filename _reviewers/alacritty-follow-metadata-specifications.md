---
title: Follow metadata specifications
description: When writing metadata files (such as AppStream, package manifests, or
  configuration files), always consult and follow the official specifications precisely.
  Pay special attention to case-sensitive identifiers, valid values, and required
  formats.
repository: alacritty/alacritty
label: Documentation
language: Xml
comments_count: 3
repository_stars: 59675
---

When writing metadata files (such as AppStream, package manifests, or configuration files), always consult and follow the official specifications precisely. Pay special attention to case-sensitive identifiers, valid values, and required formats.

Key practices:
- Verify case-sensitivity requirements for identifiers (e.g., "Apache-2.0" not "APACHE-2.0" for SPDX license IDs)
- Check that values are from approved lists (e.g., only specific licenses are valid for AppStream metadata_license)
- Use validators to ensure compliance before submission
- Include both modern and legacy tags when maintaining backward compatibility
- Reference official documentation sources in comments when standards are unclear

Example from AppStream metadata:
```xml
<!-- Correct: Case-sensitive SPDX license ID -->
<project_license>Apache-2.0</project_license>
<!-- Valid metadata license from approved list -->
<metadata_license>MIT</metadata_license>

<!-- Modern tag with legacy compatibility -->
<developer_name>Developer Name</developer_name>
<developer id="org.example">
  <name>Developer Name</name>
</developer>
```

This prevents validation failures, ensures compatibility across different parsers, and maintains professional documentation standards.