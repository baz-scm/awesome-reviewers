---
title: Review consistency assumptions
description: Periodically reassess your database operations based on updated consistency
  guarantees offered by storage technologies. As database services evolve over time,
  operations initially designed to work around consistency limitations may become
  unnecessary overhead that impacts performance.
repository: opentofu/opentofu
label: Database
language: Markdown
comments_count: 2
repository_stars: 25901
---

Periodically reassess your database operations based on updated consistency guarantees offered by storage technologies. As database services evolve over time, operations initially designed to work around consistency limitations may become unnecessary overhead that impacts performance.

For example, in Discussion 2, there was a realization that certain digest verification steps were implemented to work around S3's eventual consistency model before 2020. After S3 became strongly consistent, these checks became redundant:

```go
// This check might have been necessary when S3 was eventually consistent
// but is no longer required with strong consistency guarantees
checkDigest := &s3.GetObjectInput{
    Bucket: aws.String(bucket),
    Key:    aws.String(key + "-md5"),
}
_, err := s3Client.GetObject(checkDigest)
```

When migrating between database technologies (like from DynamoDB to S3), review not just the functional aspects but also consistency guarantees. Remove operations that were added as workarounds for previous limitations. Document the rationale behind these decisions for future maintainers, noting which database features you depend on and potential compatibility concerns with alternative implementations. This practice improves performance while maintaining system integrity.