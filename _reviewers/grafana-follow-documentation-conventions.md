---
title: Follow documentation conventions
description: "Ensure documentation adheres to established style guidelines and technical\
  \ standards:\n\n1. **Use proper terminology and formatting:**\n   - Write \"data\
  \ source\" as two words, not \"datasource\""
repository: grafana/grafana
label: Documentation
language: Markdown
comments_count: 7
repository_stars: 68825
---

Ensure documentation adheres to established style guidelines and technical standards:

1. **Use proper terminology and formatting:**
   - Write "data source" as two words, not "datasource"
   - Maintain proper capitalization for technical acronyms (e.g., "API" not "api")
   - Use consistent language in UI descriptions (prefer "display" over "show")

2. **Avoid possessives with product names:**
   ```
   // Incorrect
   Grafana's dashboard features allow users to visualize data.
   Then we can use the following query for our graph panel.
   
   // Correct
   The dashboard features in Grafana allow users to visualize data.
   To call this stored procedure from a graph panel, use the following query.
   ```

3. **Use appropriate linking syntax:**
   - For same-page references:
     ```
     [Supported Resources](#supported-resources)
     ```
   - For project pages, use Hugo shortcodes instead of ref: syntax:
     ```
     {{< relref "./path/to/page" >}}
     ```

4. **Handle deprecated features properly:**
   - Don't mention removed options in documentation
   - Provide clear alternatives for deprecated functionality
   - Add breaking change notices when documenting removed features