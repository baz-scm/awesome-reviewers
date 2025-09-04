---
title: AI configuration documentation
description: Ensure AI model configurations and related documentation use precise
  terminology and provide clear, complete setup instructions without overwhelming
  users.
repository: stanfordnlp/dspy
label: AI
language: Markdown
comments_count: 6
repository_stars: 27813
---

Ensure AI model configurations and related documentation use precise terminology and provide clear, complete setup instructions without overwhelming users.

When documenting AI models, LLMs, and related infrastructure:

1. **Use precise terminology**: Distinguish between "parameters" (learned values) and "hyperparameters" (values that control the learning process). For example, demonstration examples are parameters, while `max_labeled_demos` and `temperature` are hyperparameters.

2. **Provide complete configuration examples**: Include all required parameters, environment variables, and credentials users need. For instance, when documenting model clients, specify required connection parameters and API keys:

```python
# Good: Complete configuration
lm = dspy.Snowflake(
    model="mixtral-8x7b",
    credentials={
        "account": "your_account",
        "user": "your_username", 
        "password": "your_password",
        "warehouse": "your_warehouse"
    }
)

# Environment variables required:
# OPENAI_API_KEY="your-openai-api-key"
```

3. **Start simple, then expand**: Begin with essential configurations before introducing advanced options. Avoid overwhelming users with complex features upfront - start with basic functionality like `llms.txt` before introducing `llms-full.txt`.

4. **Include performance considerations**: Document recommended settings for better performance, such as async configurations and optimal hyperparameters:

```python
dspy.settings.configure(lm=lm, async_capacity=16)  # max 16 concurrent DSPy programs
dspy_model = dspy.asyncify(dspy.ChainOfThought("question -> answer"))
```

This approach ensures developers can successfully configure AI systems while understanding the underlying concepts and performance implications.