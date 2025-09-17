---
title: API consistency standards
description: Maintain consistent patterns across all API endpoints, including naming
  conventions, response structures, HTTP status codes, and interface design. This
  ensures a predictable and professional API surface that follows established conventions.
repository: emcie-co/parlant
label: API
language: Python
comments_count: 8
repository_stars: 12205
---

Maintain consistent patterns across all API endpoints, including naming conventions, response structures, HTTP status codes, and interface design. This ensures a predictable and professional API surface that follows established conventions.

Key consistency requirements:
- Use kebab-case (dashes) for endpoint paths, not snake_case: `/end-users` not `/end_users`, `/context-variables` not `/context_variables`
- Return appropriate HTTP status codes: 200 for updates that return data, 204 for updates without response body, 422 for semantic validation errors
- Follow consistent response patterns: create dedicated response DTOs like `ReadEvaluationResponse` instead of returning internal DTOs directly
- Use uniform naming across similar operations: avoid having multiple methods for identical functionality
- Maintain consistent response model specifications: either specify `response_model` everywhere or nowhere within the same module

Example of consistent endpoint design:
```python
@router.patch("/{customer_id}", response_model=CustomerDTO)
async def update_customer(params: CustomerUpdateParamsDTO) -> CustomerDTO:
    # Returns 200 OK with updated entity
    
@router.get("/{evaluation_id}")  
async def get_evaluation(evaluation_id: EvaluationId) -> ReadEvaluationResponse:
    # Dedicated response DTO, not direct internal model
```

This prevents API fragmentation and reduces cognitive load for API consumers by establishing predictable patterns they can rely on across all endpoints.