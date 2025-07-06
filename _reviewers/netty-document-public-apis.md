---
title: Document public APIs
description: 'All public-facing APIs must be thoroughly documented with clear javadocs.
  This includes:


  1. **Classes and interfaces**: When creating or changing a class/interface to public
  visibility, add comprehensive documentation explaining its purpose and usage.'
repository: netty/netty
label: Documentation
language: Java
comments_count: 9
repository_stars: 34227
---

All public-facing APIs must be thoroughly documented with clear javadocs. This includes:

1. **Classes and interfaces**: When creating or changing a class/interface to public visibility, add comprehensive documentation explaining its purpose and usage.

2. **Methods and constructors**: Document each public method and constructor, including:
   - Method purpose
   - Parameter descriptions and constraints
   - Return value meaning
   - Any exceptions that may be thrown

3. **Deprecated functionality**: Always add `@deprecated` tags with explanations of what alternatives users should use instead.

Example of proper documentation:

```java
/**
 * Decodes DNS response messages into {@link DnsResponse} objects.
 * <p>
 * This decoder supports both UDP and TCP transport protocols for DNS messages.
 * When using TCP, DNS messages are prefixed with a 2-byte length field.
 *
 * @param <A> The type of address used by the decoder (e.g., {@link java.net.InetSocketAddress})
 */
public abstract class DnsResponseDecoder<A extends SocketAddress> {

    /**
     * Decodes a DNS response message with the specified maximum allocation limit.
     *
     * @param maxAllocation The maximum allowed memory allocation per message in bytes.
     *                     A value of 0 means no limit.
     * @return A {@link DnsDecoder} instance with the specified allocation limit
     * @throws IllegalArgumentException if maxAllocation is negative
     */
    public static DnsDecoder newDnsDecoder(int maxAllocation) {
        // implementation
    }
    
    /**
     * @deprecated Use {@link #newDnsDecoder(int)} instead with an appropriate allocation limit
     */
    @Deprecated
    public static DnsDecoder newDnsDecoder() {
        return newDnsDecoder(0);
    }
}
```

Remember that clear documentation helps maintainers understand code intent, improves API usability for consumers, and prevents future bugs from misunderstandings about component behavior.