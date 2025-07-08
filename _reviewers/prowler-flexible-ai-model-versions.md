---
title: Flexible AI model versions
description: When integrating LLM or AI models into your application, implement model
  selection in a way that accommodates the rapid evolution of AI capabilities without
  requiring frequent code deployments.
repository: prowler-cloud/prowler
label: AI
language: Python
comments_count: 2
repository_stars: 11834
---

When integrating LLM or AI models into your application, implement model selection in a way that accommodates the rapid evolution of AI capabilities without requiring frequent code deployments.

Use Django enums or similar in-code definitions for validation while avoiding database-level constraints like Postgres enums that are difficult to modify:

```python
# Recommended approach:
class AIModelConfig(models.Model):
    # Define choices in code for validation
    MODEL_CHOICES = [
        "gpt-4o",
        "gpt-4o-mini",
        # Add new models here without database migrations
    ]
    
    # Use CharField with validation in clean() instead of ChoiceField
    model = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text="Must be one of the supported model names"
    )
    
    def clean(self):
        # Validate model name
        if self.model not in self.MODEL_CHOICES:
            raise ValidationError(
                f"Model must be one of: {', '.join(self.MODEL_CHOICES)}"
            )
```

This pattern allows you to add support for new AI models by updating the MODEL_CHOICES list without requiring database migrations or application updates, while still maintaining validation to ensure only supported models are used.