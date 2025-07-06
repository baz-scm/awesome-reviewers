---
title: Document dependency versions
description: When managing dependency versions in configuration files, provide clear
  documentation to help maintainers understand version choices and relationships.
  Include links to repositories where versions can be verified, keep related versions
  aligned when appropriate, and add explanatory comments for version-related decisions.
repository: quarkusio/quarkus
label: Configurations
language: Xml
comments_count: 3
repository_stars: 14667
---

When managing dependency versions in configuration files, provide clear documentation to help maintainers understand version choices and relationships. Include links to repositories where versions can be verified, keep related versions aligned when appropriate, and add explanatory comments for version-related decisions.

Examples of good practices:

1. Add repository links for easier version checking:
```xml
<!-- When updating, check versions at https://central.sonatype.com/artifact/io.grpc/grpc-core -->
<grpc.version>1.69.1</grpc.version> 
```

2. Explain dependencies between related versions:
```xml
<grpc.version>1.69.1</grpc.version> <!-- when updating, verify if com.google.auth and perfmark.version should not be updated too -->
```

3. When relocating version properties, provide clear location comments:
```xml
<!--jakarta.persistence-api.version is located in the root pom -->
```

4. Document the rationale for version alignment or divergence between related components:
```xml
<!-- Elasticsearch server and client versions can differ but keeping aligned to latest micro is preferred -->
<elasticsearch-server.version>9.0.1</elasticsearch-server.version>
<elasticsearch-client.version>9.0.1</elasticsearch-client.version>
```

Clear version documentation reduces maintenance burden, prevents accidental version mismatches, and helps team members understand the reasoning behind specific version choices.