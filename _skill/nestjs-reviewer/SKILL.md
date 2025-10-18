---
name: nestjs-reviewer
description: "Guidelines for reviewing NestJS framework code, emphasizing security best practices and maintaining backward-compatible public APIs."
license: CC-BY-4.0
---

# NestJS Code Review Guidelines

## Security Best Practices
NestJS code should adhere to strong security practices. One key guideline is to use modern, secure algorithms and protocols by default. For example, always prefer strong cryptographic hashes (like SHA-256) over weaker ones (MD5, SHA-1) for any security-related functionality[70]. If reviewing code that handles passwords or tokens, ensure it’s using a robust algorithm and library. The project’s standards indicate that functions should avoid deprecated algorithms – e.g., if a contributor tries to introduce an `xxh32` hash for a security-sensitive purpose, it should be replaced with a call to `Node`’s `crypto.createHash('sha256')` or a similar secure alternative[71]. Modern algorithms often bring both security and performance benefits, and using them prevents warnings from security audit tools[72]. Also verify that any default configurations (like allowed SSL/TLS versions or JWT signing algorithms) are set to secure choices, and that outdated options are removed or disabled.

## Preserving API Stability
NestJS places importance on not breaking consumers’ code, so public APIs should be extended in a backward-compatible way[73]. When reviewing changes to interfaces, classes, or decorators that external users rely on, ensure that new additions are optional or provide safe defaults. For instance, if adding a new method to an interface, mark it optional (using `?`) so existing implementations don’t suddenly fail to compile[74]. If altering a type alias or union, consider using a union type extension that includes the old type as a subset, rather than replacing it outright[75]. When introducing new features that could conflict with old ones, the changes should either extend existing types or be gated behind configuration flags or version markers[76]. An example is versioned controllers in NestJS: a new feature might only apply when a controller is marked with a newer version, leaving older versions unaffected[77]. Encourage thorough documentation of such changes (like clearly noting from which framework version a new option is available). By following semantic versioning and making incremental, non-breaking changes, NestJS can deliver new capabilities without stranding users on older versions[76][78].
