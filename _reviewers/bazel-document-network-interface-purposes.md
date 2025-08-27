---
title: Document network interface purposes
description: When implementing multiple network-related interfaces or classes that
  handle similar operations (like downloading), clearly document the purpose, scope,
  and differences between each interface to prevent confusion and misuse.
repository: bazelbuild/bazel
label: Networking
language: Java
comments_count: 2
repository_stars: 24489
---

When implementing multiple network-related interfaces or classes that handle similar operations (like downloading), clearly document the purpose, scope, and differences between each interface to prevent confusion and misuse.

This is particularly important when you have specialized implementations for different protocols or use cases. For example, if you have both a general `Downloader` interface and a specialized `HttpDownloader` class, or when introducing remote download proxies like `GrpcRemoteDownloader`, each should have clear documentation explaining:

- What specific use cases each interface/class serves
- Why multiple interfaces are needed instead of a unified approach  
- Which methods are available on which interfaces
- How they interact with configuration flags and different execution contexts

Example from the codebase:
```java
public DownloadManager(
    RepositoryCache repositoryCache, 
    Downloader downloader, 
    HttpDownloader httpDownloader) {
  // Document why we need both Downloader and HttpDownloader:
  // - Downloader: General interface, may be GrpcRemoteDownloader for remote asset API
  // - HttpDownloader: Direct HTTP implementation, used by bzlmod for registry access
  // - The bzlmod downloader uses downloadAndReadOneUrl() which only exists on HttpDownloader
}
```

This prevents developers from having to reverse-engineer the differences between interfaces and reduces the likelihood of using the wrong interface for a given use case. It also helps during code reviews to ensure the appropriate download mechanism is being used for each context.