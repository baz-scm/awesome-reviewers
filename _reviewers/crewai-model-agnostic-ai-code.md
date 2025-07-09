---
title: Model-agnostic AI code
description: When building applications that interact with AI models, avoid hardcoding
  model-specific behavior and instead design for flexibility across different LLM
  providers and versions. This approach increases resilience and makes your code more
  maintainable as the AI ecosystem evolves.
repository: crewaiinc/crewai
label: AI
language: Python
comments_count: 5
repository_stars: 33945
---

When building applications that interact with AI models, avoid hardcoding model-specific behavior and instead design for flexibility across different LLM providers and versions. This approach increases resilience and makes your code more maintainable as the AI ecosystem evolves.

Key practices:
1. Allow LLM instances to be passed as parameters rather than hardcoding model names
2. Implement provider-specific handling through abstraction rather than special cases
3. Validate LLM instances early to prevent runtime errors
4. Use dependency injection for LLM components to make testing easier

Example:

```python
# Instead of this:
def process_with_ai(prompt, model="gpt-4o"):
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Do this:
def process_with_ai(prompt, llm=None):
    llm = llm or get_default_llm()
    
    # Validate LLM instance early
    if not hasattr(llm, 'call') or not callable(llm.call):
        raise ValueError("Invalid LLM instance: missing call method")
    
    # Use provider-agnostic interface
    return llm.call([{"role": "user", "content": prompt}])

def get_default_llm():
    # Create default LLM instance with appropriate config
    return BaseLLM(model="default-model")
```

This approach lets you easily switch models, test with mock LLMs, and adapt to new model APIs without changing your core application logic.