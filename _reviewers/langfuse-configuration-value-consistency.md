---
title: Configuration value consistency
description: 'Maintain consistency in configuration values across the application
  by following these practices:


  1. **Use properly formatted template strings for configuration keys**'
repository: langfuse/langfuse
label: Configurations
language: TSX
comments_count: 4
repository_stars: 13574
---

Maintain consistency in configuration values across the application by following these practices:

1. **Use properly formatted template strings for configuration keys**
   Template strings for configuration keys should be properly formatted with correct syntax to avoid runtime errors and ensure consistent storage.
   
   ```typescript
   // Incorrect
   const key = `${projectId}-${datasetId-chart-metrics`;
   
   // Correct
   const key = `${projectId}-${datasetId}-chart-metrics`;
   ```

2. **Update identifiers when functionality changes**
   When updating functionality that relies on persistent identifiers (like notifications), update the identifier to ensure proper behavior for all users.
   
   ```typescript
   // When updating a notification:
   // Old
   id: "lw3-1",
   
   // New (when content changes)
   id: "lw3-2",
   ```

3. **Use consistent default values for the same parameter**
   When a parameter is used in multiple places, ensure that default values are consistent to avoid confusing behavior.
   
   ```typescript
   // Inconsistent defaults
   const [selectedTab] = useQueryParam("display", withDefault(StringParam, "details"));
   // vs elsewhere
   onExpand={() => setSelectedTab("preview")}
   
   // Consistent defaults
   const [selectedTab] = useQueryParam("display", withDefault(StringParam, "preview"));
   ```

4. **Avoid hardcoded values in favor of configurable settings**
   Configuration values (especially URLs, endpoints, and service-specific settings) should be configurable rather than hardcoded, allowing for easier environment-specific customization.
   
   ```typescript
   // Hardcoded (avoid)
   case LLMAdapter.Atla:
     return "https://api.atla-ai.com/v1/integrations/langfuse";
   
   // Configurable (preferred)
   case LLMAdapter.Atla:
     return customization?.defaultBaseUrlAtla ?? "";
   ```