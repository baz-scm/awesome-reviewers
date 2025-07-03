---
title: Dependency verification configuration
description: When adding new dependencies to build.gradle.kts files, always update
  the corresponding verification metadata to prevent build failures. Use the Gradle
  command `./gradlew --write-verification-metadata md5,sha256 help` to generate the
  necessary metadata, but review the output carefully as it may add more dependencies
  than required. Consider manually adding...
repository: JetBrains/kotlin
label: Configurations
language: Xml
comments_count: 2
repository_stars: 50857
---

When adding new dependencies to build.gradle.kts files, always update the corresponding verification metadata to prevent build failures. Use the Gradle command `./gradlew --write-verification-metadata md5,sha256 help` to generate the necessary metadata, but review the output carefully as it may add more dependencies than required. Consider manually adding only the necessary verification entries if the automated command adds excessive dependencies.

Example workflow:
```
// 1. Add dependency to build.gradle.kts
dependencies {
    implementation("io.github.java-diff-utils:java-diff-utils:4.10")
}

// 2. Generate verification metadata
// Run: ./gradlew --write-verification-metadata md5,sha256 help

// 3. Review generated changes in verification-metadata.xml and retain only necessary entries
<component group="io.github.java-diff-utils" name="java-diff-utils" version="4.10">
  // Keep only required verification entries
</component>
```
