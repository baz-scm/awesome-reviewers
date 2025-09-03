---
title: Organize documentation content
description: Structure documentation to prevent information overload and improve readability
  by using appropriate organizational elements and callouts judiciously.
repository: langflow-ai/langflow
label: Documentation
language: Markdown
comments_count: 11
repository_stars: 111046
---

Structure documentation to prevent information overload and improve readability by using appropriate organizational elements and callouts judiciously.

**Key principles:**

1. **Break up complex information**: When a single section contains multiple concepts or choices, use tabs, collapsible details, or separate sections to organize the content logically.

2. **Use callouts appropriately**: Reserve "important" admonitions for truly critical information. Use "tip" for helpful but non-essential information, and regular text for general explanations.

3. **Avoid empty headings**: Don't have empty space between headings. Each heading should immediately be followed by content or subheadings.

4. **Group related content**: When documenting multiple related items (like components from the same provider), group them together under a common section.

5. **Minimize visual clutter**: Wrap lengthy code outputs or JSON responses in collapsible `<details>` sections when only specific parts are relevant to the reader.

**Example of good organization:**

```markdown
## Configure MCP servers

### Install the server locally

1. Install the weather server:
   ```bash
   uv pip install mcp_weather_server
   ```

2. Configure the server connection:

<Tabs>
  <TabItem value="json" label="JSON Configuration">
    Configure using JSON format...
  </TabItem>
  <TabItem value="stdio" label="STDIO Configuration">  
    Configure using STDIO format...
  </TabItem>
</Tabs>

:::tip Environment variables
Langflow passes environment variables from the `.env` file to MCP, but not global variables declared in the UI.
:::
```

This approach separates installation from configuration, uses tabs for different options, and reserves the tip callout for helpful supplementary information rather than critical instructions.