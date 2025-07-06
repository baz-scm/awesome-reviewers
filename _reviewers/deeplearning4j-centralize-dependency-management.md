---
title: Centralize dependency management
description: 'Manage dependencies at the top level using `<dependencyManagement>`
  to ensure version consistency across modules and prevent conflicts. Define version
  properties in one place and reference them throughout the project:'
repository: deeplearning4j/deeplearning4j
label: Configurations
language: Xml
comments_count: 10
repository_stars: 14036
---

Manage dependencies at the top level using `<dependencyManagement>` to ensure version consistency across modules and prevent conflicts. Define version properties in one place and reference them throughout the project:

```xml
<!-- In parent pom.xml -->
<properties>
    <jackson.version>2.15.0</jackson.version>
    <jmh.version>1.33</jmh.version>
</properties>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>${jackson.version}</version>
        </dependency>
        <dependency>
            <groupId>io.netty</groupId>
            <artifactId>netty-all</artifactId>
            <version>${netty.version}</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

In module pom files, reference dependencies without version numbers:

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
</dependency>
```

Avoid:
- Release candidate (RC) or SNAPSHOT versions in production code
- Downgrading library versions
- Using generic version references like `${project.version}` or `${project.parent.version}`
- Different versions of the same underlying libraries (e.g., JavaCPP)

For related but distinct libraries (like Netty 3.x vs 4.x), create separate version properties (e.g., `netty3.version` and `netty.version`) to clearly distinguish them.