---
title: "TEST Choose log levels based on event frequency and operational impact"
description: "TEST Services and their dependencies (databases, loggers, external services) should be initialized in a centralized location during application startup. This ensures proper dependency management, consistent configuration patterns, and early detection of configuration issues."
repository: "langchain-ai/langchain"
label: "Error handling"
language: "Python"
comments_count: 325
repository_stars: 10
---

Choose log levels based on event frequency and operational impact, not just severity.

When implementing logging in your application, consider both the frequency of events and their operational impact when selecting log levels. High-frequency events should generally use DEBUG or INFO levels to avoid overwhelming log systems, while events that require immediate attention should use WARN or ERROR regardless of frequency.

Guidelines for log level selection:

**ERROR**: Use for events that require immediate attention and indicate a failure in core functionality. These should be actionable and worthy of alerts.

**WARN**: Use for events that are concerning but don't immediately break functionality. These often indicate potential issues that should be monitored.

**INFO**: Use for significant business events and major state changes. These help with understanding application flow and troubleshooting.

**DEBUG**: Use for detailed diagnostic information, including high-frequency events like individual request processing steps.

Consider the operational context: a failed external API call might be ERROR if it's critical for your application, but only WARN if you have fallback mechanisms. Similarly, a database connection retry might be DEBUG if it's part of normal resilience patterns, but WARN if retries are becoming frequent.

Remember that logs are for operators and future developers, not just for debugging during development. Choose levels that will be useful for production monitoring and troubleshooting.