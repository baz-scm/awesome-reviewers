---
title: Prefer null-safe access
description: 'Always use null-safe access patterns when dealing with potentially undefined
  values to prevent runtime errors and improve code robustness. This includes:'
repository: grafana/grafana
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 68825
---

Always use null-safe access patterns when dealing with potentially undefined values to prevent runtime errors and improve code robustness. This includes:

1. **Use optional chaining (`?.`) for nested property access:**
   ```typescript
   // Instead of assuming objects/properties exist:
   managedBy: ManagerKind[item.metadata.annotations['grafana.com/managed-by']]

   // Use optional chaining:
   managedBy: item.metadata?.annotations?.[AnnoKeyManagerKind]
   ```

2. **Use conditional expressions for null-dependent logic:**
   ```typescript
   // Instead of assuming rule exists:
   const isProvisioned = rulerRuleType.grafana.rule(rule) && Boolean(rule.grafana_alert.provenance);
   
   // Use conditional checking:
   const isProvisioned = rule ? isProvisionedRule(rule) : false;
   ```

3. **Return empty collections instead of null/undefined:**
   ```typescript
   // Instead of special values or undefined:
   return metrics.length === 0 ? MATCH_ALL_LABELS_STR : ...;
   
   // Return empty collections:
   return metrics.length === 0 ? [] : [...];
   ```

4. **Include nullability in type assertions:**
   ```typescript
   // Instead of assuming the type is always present:
   const parsed = loadAll(raw) as Array<{ kind: string }>;
   
   // Account for potential unknown fields and nullability:
   const parsed = loadAll(raw) as Array<Record<string, unknown> & { kind: string }>;
   ```

This approach makes code more defensive and easier to maintain by explicitly handling null cases and preventing "cannot read property of undefined" runtime errors.