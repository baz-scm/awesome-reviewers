---
title: Centralize AI code
description: Move AI-specific functionality (especially prompts) to dedicated services
  rather than scattering them throughout the codebase. This improves maintainability
  and follows team conventions.
repository: getsentry/sentry
label: AI
language: Python
comments_count: 3
repository_stars: 41297
---

Move AI-specific functionality (especially prompts) to dedicated services rather than scattering them throughout the codebase. This improves maintainability and follows team conventions.

Specifically:
1. Place AI prompts in dedicated AI services (like Seer) rather than embedding them in general application code
2. Use structured output formats instead of regex parsing for AI responses
3. Make AI connections explicit by moving AI-specific functions to appropriate modules

Example - Instead of:
```python
def make_input_prompt(feedbacks):
    feedbacks_string = "\n".join(f"- {msg}" for msg in feedbacks)
    return f"""Task:
    Instructions: You are an AI assistant that analyzes customer feedback.
    Create a summary based on the user feedbacks...
    """

SUMMARY_REGEX = re.compile(r"Summary:\s*(.*)", re.DOTALL)
```

Prefer:
```python
# In AI service module
def get_feedback_summary(feedbacks):
    # Call centralized AI service with structured response format
    response = ai_service.complete_prompt(
        usecase="feedback_summary",
        inputs={"feedbacks": feedbacks},
        output_schema={"summary": str}
    )
    return response.summary
```