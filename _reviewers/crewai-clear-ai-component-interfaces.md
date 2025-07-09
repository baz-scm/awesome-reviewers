---
title: Clear AI component interfaces
description: 'When designing AI components and tools, use domain-specific terminology
  and provide clear interface documentation to enhance usability and integration.
  This includes:'
repository: crewaiinc/crewai
label: AI
language: Other
comments_count: 3
repository_stars: 33945
---

When designing AI components and tools, use domain-specific terminology and provide clear interface documentation to enhance usability and integration. This includes:

1. Use precise, domain-specific naming that clearly indicates the component's purpose and functionality in the AI ecosystem. For example, prefer `LLMGuardrail` over generic terms like `Validator` when the component specifically handles language model outputs.

2. Document how AI agents and LLMs will interact with your tools, including expected inputs, outputs, and parameter definitions. This helps other developers understand how the AI will interpret and use the tool.

3. Provide complete usage examples that demonstrate real-world integration patterns.

Example:

```python
# Good practice with clear naming and documentation
from crewai import Task
from crewai.llm import LLM

task = Task(
    description="Generate JSON data",
    expected_output="Valid JSON object",
    guardrail=LLMGuardrail(  # Specific name indicates it works with LLMs
        instructions="Ensure the response is a valid JSON object",
        examples=[{"valid": {"key": "value"}}]
    )
)

# Example showing tool integration with clear documentation of parameters
from crewai_tools import AISearchTool  # Name indicates AI-specific functionality

# Document how the AI will use this tool
search_tool = AISearchTool(
    name="Web Search",  # Clear name for AI to reference
    description="Search the web for up-to-date information on a given topic",
    input_schema={"query": "The search term or question to look up online"}
)

agent = Agent(
    role="Research Analyst",
    goal="Provide up-to-date market analysis",
    tools=[search_tool]
)
```

Clear interfaces improve maintainability, make your code more intuitive for other developers, and help language models better understand how to interact with your components.