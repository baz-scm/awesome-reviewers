---
title: Handle AI provider inconsistencies
description: When integrating with AI model providers, implement defensive programming
  to handle API inconsistencies, bugs, and unexpected return types. AI provider libraries
  often have implementation bugs or return different types than documented, requiring
  robust error handling and type checking.
repository: SWE-agent/SWE-agent
label: AI
language: Python
comments_count: 2
repository_stars: 16839
---

When integrating with AI model providers, implement defensive programming to handle API inconsistencies, bugs, and unexpected return types. AI provider libraries often have implementation bugs or return different types than documented, requiring robust error handling and type checking.

Key practices:
- Add type checking for different possible return types from AI APIs
- Implement fallbacks for provider-specific bugs or limitations  
- Use existing token counting methods from other providers as pragmatic workarounds
- Calculate token limits correctly (e.g., max_tokens = context_length - input_tokens)

Example from LiteLLM tokenizer bug workaround:
```python
def count_tokens(text: str) -> int:
    enc = tokenizer_json["tokenizer"].encode(text)
    if isinstance(enc, list):
        return len(enc)
    elif hasattr(enc, "ids"):
        return len(enc.ids)
    else:
        raise TypeError(f"Unexpected return type from encode: {type(enc)}")
```

This approach ensures your AI model integrations remain robust even when underlying provider APIs have bugs or inconsistent behavior.