---
title: Generate dynamic configurations
description: Always generate configuration files programmatically when they contain
  dynamic content that changes frequently or needs to stay in sync with the application
  (like version numbers, release dates, or build timestamps). Manual maintenance of
  such files is tedious, error-prone, and creates maintenance overhead.
repository: ghostty-org/ghostty
label: Configurations
language: Xml
comments_count: 2
repository_stars: 32864
---

Always generate configuration files programmatically when they contain dynamic content that changes frequently or needs to stay in sync with the application (like version numbers, release dates, or build timestamps). Manual maintenance of such files is tedious, error-prone, and creates maintenance overhead.

For example, instead of manually updating version information in XML metadata files:

```xml
<!-- Avoid manual updates like this -->
<releases>
  <release version="1.0.1" date="2024-12-31">
    <url type="details">https://ghostty.org/docs/install/release-notes/1-0-1</url>
  </release>
</releases>
```

Generate these files during the build process:

```bash
# Generate at build time to ensure consistency with application version
generate_appdata_xml --version="$APP_VERSION" --build-date="$(date +%Y-%m-%d)" --release-notes-url="https://ghostty.org/docs/install/release-notes/$APP_VERSION"
```

This approach ensures configuration files stay synchronized with the application state and eliminates manual update errors.