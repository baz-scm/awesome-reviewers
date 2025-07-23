---
title: Consistent output path specification
description: Configuration files defining operations that generate data outputs must
  always include a `<save_to>` element specifying the output location. Follow established
  patterns for similar operations, typically using predictable paths like `.roo/temp/pr-[PR_NUMBER]/[operation]-output.{json|diff}`.
  This ensures operation outputs are consistently stored and easily...
repository: RooCodeInc/Roo-Code
label: Configurations
language: Xml
comments_count: 4
repository_stars: 17288
---

Configuration files defining operations that generate data outputs must always include a `<save_to>` element specifying the output location. Follow established patterns for similar operations, typically using predictable paths like `.roo/temp/pr-[PR_NUMBER]/[operation]-output.{json|diff}`. This ensures operation outputs are consistently stored and easily locatable by other processes.

Example:
```xml
<operation name="fetch_comments">
  <description>Get all comments on the PR</description>
  <command>gh pr view [PR_NUMBER] --repo [owner]/[repo] --json comments --jq '.comments'</command>
  <output_format>JSON array of comments</output_format>
  <save_to>.roo/temp/pr-[PR_NUMBER]/pr-comments.json</save_to>
</operation>
```