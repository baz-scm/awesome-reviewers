---
title: Optimize algorithmic choices
description: When implementing algorithms, prioritize both correctness and efficiency
  by selecting the most appropriate data structures and computational approaches for
  each specific task. Ensure mathematical calculations follow established specifications
  and standards, and choose data structures that match the operation's requirements.
repository: facebook/react-native
label: Algorithms
language: Objective-C
comments_count: 2
repository_stars: 123178
---

When implementing algorithms, prioritize both correctness and efficiency by selecting the most appropriate data structures and computational approaches for each specific task. Ensure mathematical calculations follow established specifications and standards, and choose data structures that match the operation's requirements.

For geometric calculations, verify that mathematical transformations account for all relevant parameters. For example, when calculating inner corner radii with border insets, adjust the radii based on border thickness according to specifications like the W3C CSS spec.

For data operations, select the most efficient data structure. Instead of using regular expressions for simple character filtering operations, consider more direct approaches like NSCharacterSet:

```objc
// Less efficient: regex for simple character filtering
NSRegularExpression *regex = [NSRegularExpression regularExpressionWithPattern:@"[^a-z0-9_]" options:0 error:nil];

// More efficient: character set for the same operation
NSCharacterSet *allowedChars = [NSCharacterSet characterSetWithCharactersInString:@"abcdefghijklmnopqrstuvwxyz0123456789_"];
```

This approach reduces computational overhead while maintaining code clarity and correctness.