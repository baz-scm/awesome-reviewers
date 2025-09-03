---
title: validate LLM reliability
description: Always validate LLM capabilities before deployment and implement robust
  handling for unreliable responses. LLMs can vary significantly in capability and
  may return empty, invalid, or hallucinated responses that can break your application.
repository: browser-use/browser-use
label: AI
language: Python
comments_count: 4
repository_stars: 69139
---

Always validate LLM capabilities before deployment and implement robust handling for unreliable responses. LLMs can vary significantly in capability and may return empty, invalid, or hallucinated responses that can break your application.

Implement capability testing with realistic prompts that match your actual usage patterns. Use simple knowledge tests to establish a minimum intelligence bar and filter out low-power models that struggle with basic instructions.

```python
def _test_tool_calling_method(self, method: str) -> bool:
    """Test if a specific tool calling method works with the current LLM."""
    try:
        # Test with realistic prompt matching actual usage
        test_message = HumanMessage(content='What is the capital of France? Respond with valid JSON.')
        
        if method == 'raw':
            response = self.llm.invoke([test_message])
            # Validate both response format and basic intelligence
            if not response or 'Paris' not in response.content:
                return False
        
        return True
    except Exception:
        return False
```

Always validate LLM outputs against original inputs to detect hallucination, and implement retry logic with fallback actions for empty or invalid responses:

```python
if not model_output.action or all(action.model_dump() == {} for action in model_output.action):
    logger.warning('Model returned empty action. Retrying...')
    retry_messages = input_messages + [clarification_message]
    model_output = await self.get_next_action(retry_messages)
    
    if not model_output.action:
        # Safe fallback action
        action_instance = self.ActionModel(done={
            'success': False,
            'text': 'No next action returned by LLM!',
        })
```

This approach significantly reduces support load from broken or low-capability models while ensuring your application remains functional even when LLMs behave unpredictably.