---
title: Configurable resource locations
description: Always make file paths, temporary directories, and resource locations
  configurable with reasonable defaults instead of hard-coding them. Users may have
  specific environment requirements such as using SSDs instead of system drives or
  working with constrained environments like Spring Boot.
repository: deeplearning4j/deeplearning4j
label: Configurations
language: Java
comments_count: 4
repository_stars: 14036
---

Always make file paths, temporary directories, and resource locations configurable with reasonable defaults instead of hard-coding them. Users may have specific environment requirements such as using SSDs instead of system drives or working with constrained environments like Spring Boot.

Implement a hierarchical approach to resource configuration:
1. Allow explicit configuration through system properties or configuration files
2. Provide fallback to environment-specific defaults when explicit configuration isn't available
3. Document all configurable paths and their default values

For example, instead of:
```java
File holder = File.createTempFile("FileChunksTracker", "Message");
```

Use a configurable approach:
```java
// Define in a centralized properties class
public static final String FILE_STORAGE_DIR_PROPERTY = "org.nd4j.tempfiles.directory";

// Use in implementation
String tempDir = System.getProperty(FILE_STORAGE_DIR_PROPERTY, System.getProperty("java.io.tmpdir"));
File storageDir = new File(tempDir);
if (!storageDir.exists()) {
    storageDir.mkdirs();
}
File holder = File.createTempFile("FileChunksTracker", "Message", storageDir);
```

This practice improves flexibility across different deployment environments and facilitates troubleshooting when resource loading issues occur.