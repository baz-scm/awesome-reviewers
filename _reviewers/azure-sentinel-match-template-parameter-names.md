---
title: Match Template Parameter Names
description: When documenting or wiring configuration inputs for infrastructure/templates,
  use the *exact* identifier names from the underlying template (including casing
  and punctuation), and keep descriptions semantically aligned with the producing
  service.
repository: Azure/Azure-Sentinel
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 6042
---

When documenting or wiring configuration inputs for infrastructure/templates, use the *exact* identifier names from the underlying template (including casing and punctuation), and keep descriptions semantically aligned with the producing service.

Apply this as a checklist:
1. For every documented parameter, copy the name directly from the CloudFormation template and preserve its exact spelling (e.g., `AwsRoleName` vs `AWSRoleName`, `CloudTrailTrailName` vs `CloudTrail-TrailName`).
2. Do not reuse parameter lists from a similar template/README without re-validating each field’s name and meaning (especially boolean toggles like `CreateNewBucket`).
3. Ensure descriptions use the correct domain terminology for the service output (e.g., CloudTrail “logs”, not GuardDuty “findings”).

Example of the kind of naming consistency required (illustrative):
- `AWSRoleName` → `AwsRoleName`
- bucket toggle `BucketName` → `CreateNewBucket`
- `CloudTrail-TrailName` → `CloudTrailTrailName` (remove hyphen)
- `GuardDutyBucketName` → `LogBucketName` (template-specific meaning)