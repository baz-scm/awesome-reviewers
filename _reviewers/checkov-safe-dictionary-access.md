---
title: Safe dictionary access
description: Always use safe dictionary access patterns when handling potentially
  null or missing values. This prevents KeyError and AttributeError exceptions that
  can crash your application.
repository: bridgecrewio/checkov
label: Null Handling
language: Python
comments_count: 8
repository_stars: 7667
---

Always use safe dictionary access patterns when handling potentially null or missing values. This prevents KeyError and AttributeError exceptions that can crash your application.

Key practices to follow:
1. Use `.get()` with default values when accessing dictionaries:
   ```python
   # Instead of conf["properties"]["siteConfig"]
   # Use this pattern:
   conf.get("properties", {}).get("siteConfig")
   ```

2. Validate types before performing operations:
   ```python
   # Before accessing nested attributes or methods:
   if isinstance(nic_bloc, dict) and nic_bloc.get('allow_ip_spoofing', [False])[0]:
       # Process nic_bloc
   ```

3. Use explicit checks for None vs. empty collections:
   ```python
   # For dictionaries with empty values vs None
   if each["change"]["before"] is None:  # Check specifically for None
       each["change"]["before"] = {}
   ```

4. Handle deeply nested structures safely:
   ```python
   # For complex nested access:
   inline_suppressions_by_cve = inline_suppressions.get("cves", {}).get("byCve", [])
   for cve_suppression in inline_suppressions_by_cve:
       cve_id = cve_suppression.get("cveId")
       if cve_id:
           cve_by_cve_map[cve_id] = cve_suppression
   ```

This pattern reduces bugs, improves code readability, and eliminates the need for multiple conditional checks.