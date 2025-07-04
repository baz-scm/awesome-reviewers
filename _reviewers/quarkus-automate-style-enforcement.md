---
title: Automate style enforcement
description: Implement automated code style enforcement using complementary tools
  rather than relying on manual reviews. Configure multiple tools to work together,
  as each has unique strengths and blind spots.
repository: quarkusio/quarkus
label: Code Style
language: Xml
comments_count: 4
repository_stars: 14667
---

Implement automated code style enforcement using complementary tools rather than relying on manual reviews. Configure multiple tools to work together, as each has unique strengths and blind spots.

Key practices:
- Configure formatters to automatically apply fixes (not just check) to prevent build failures while ensuring consistency
- Use overlapping tools like formatter-maven-plugin, spotless, and PMD together for comprehensive coverage
- Add static analysis rules to catch common style and quality issues
- Automate organizational concerns like import ordering and POM file element sorting

Example configuration:

```xml
<plugin>
    <groupId>com.diffplug.spotless</groupId>
    <artifactId>spotless-maven-plugin</artifactId>
    <configuration>
        <java>
            <removeUnusedImports />
            <formatAnnotations />
            <!-- Additional style rules -->
        </java>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>apply</goal>
            </goals>
            <phase>process-sources</phase>
        </execution>
    </executions>
</plugin>
```

When introducing new tools, prefer those that can automatically fix issues rather than just reporting them. This reduces manual work and ensures consistent style across the codebase.