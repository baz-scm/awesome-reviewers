---
title: Semantic naming patterns
description: 'Names should clearly communicate purpose, relationships, and domain
  context. Choose identifiers that reveal intent and accurately describe what they
  represent:'
repository: crewaiinc/crewai
label: Naming Conventions
language: Python
comments_count: 8
repository_stars: 33945
---

Names should clearly communicate purpose, relationships, and domain context. Choose identifiers that reveal intent and accurately describe what they represent:

1. **Class/component names should reflect relationships** - Name components to show their relationship with other entities. For example, prefer `TaskGuardrail` over `GuardrailTask` to indicate it's a guardrail for tasks, not a task type.

2. **Use domain-specific naming** - Avoid generic names when domain-specific terms can provide context. For instance, use `crewai_events` instead of generic `event_bus` to clearly indicate the domain.

3. **Method names should indicate actions** - Name methods with verbs that describe what they do:
   ```python
   # Good - name clearly indicates action
   def _get_context(self, task, task_outputs):
       # Method retrieves context
   
   # Confusing - doesn't clearly indicate if setting or getting
   def _context(self, task, task_outputs):
       # Purpose unclear from name
   ```

4. **Parameter names should indicate limitations** - When parameters have specific constraints, reflect this in the name:
   ```python
   # Good - name indicates specific model type support
   def __init__(self, openai_model_name: str):
       self.model = openai_model_name
   
   # Misleading - suggests any model type works
   def __init__(self, model: str):
       self.model = model  # Actually only works with OpenAI
   ```

5. **Interface naming should follow conventions** - Use recognized naming patterns for interfaces and abstract classes (e.g., `AgentInterface` rather than `AgentWrapperParent`).