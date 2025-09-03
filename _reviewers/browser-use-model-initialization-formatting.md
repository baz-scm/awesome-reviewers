---
title: Model initialization formatting
description: Maintain consistent formatting when initializing AI models and agents.
  Use proper spacing around assignment operators and consistent indentation for constructor
  parameters to improve code readability and follow Python style conventions.
repository: browser-use/browser-use
label: AI
language: Other
comments_count: 2
repository_stars: 69139
---

Maintain consistent formatting when initializing AI models and agents. Use proper spacing around assignment operators and consistent indentation for constructor parameters to improve code readability and follow Python style conventions.

Key formatting rules:
- Add spaces around assignment operators (=)
- Use consistent indentation for multi-line constructor parameters
- Align parameters vertically when spanning multiple lines

Example of proper formatting:
```python
# Good: proper spacing and indentation
llm = ChatOpenAI(base_url='https://api.novita.ai/v3/openai', model='deepseek/deepseek-v3-0324', api_key=SecretStr(api_key))

agent = Agent(
    task="Your task here",
    llm=llm,
    planner_llm=planner_llm,
    extend_planner_system_message=extend_planner_system_message
)
```

This ensures AI model initialization code is clean, readable, and follows established Python formatting standards.