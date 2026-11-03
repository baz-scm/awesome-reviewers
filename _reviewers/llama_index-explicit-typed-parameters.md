---
title: Explicit typed parameters
description: Public constructors and methods should expose explicit, named, and well-documented
  parameters instead of swallowing configuration into generic `**kwargs`. Generic
  kwargs hide the actual contract, make autocompletion/documentation worthless, and
  force users to dig through source to discover valid options. When a parameter only
  accepts a fixed set of values,...
repository: run-llama/llama_index
label: API
language: Python
comments_count: 6
repository_stars: 52785
---

Public constructors and methods should expose explicit, named, and well-documented parameters instead of swallowing configuration into generic `**kwargs`. Generic kwargs hide the actual contract, make autocompletion/documentation worthless, and force users to dig through source to discover valid options. When a parameter only accepts a fixed set of values, declare it as a `Literal[...]` (or an `Enum` backed by pydantic validation) rather than a bare `str`, so invalid values are rejected at construction time instead of failing deep in some API call. For binary on/off behavior, prefer a simple, conventionally-named boolean flag (e.g. `raise_on_error: bool = True`) over a string/enum with only two meaningful states, matching the pattern already used elsewhere in the codebase — this keeps the DevX consistent across integrations.

Example:

```python
# Avoid
class IsaacusEmbedding(BaseEmbedding):
    task: Optional[str] = Field(default=None, description="Task type.")
    overflow_strategy: Optional[str] = Field(default="drop_end")

class SlidingWindowRateLimiter(BaseModel):
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)

# Prefer
class IsaacusEmbedding(BaseEmbedding):
    task: Optional[Literal["retrieval/query", "retrieval/document"]] = Field(
        default=None, description="Task type."
    )
    overflow_strategy: Literal["drop_end", "truncate", "error"] = Field(
        default="drop_end"
    )

class SlidingWindowRateLimiter(BaseModel):
    def __init__(
        self,
        requests_per_minute: Optional[float] = None,
        request_burst: float = 0.0,
        tokens_per_minute: Optional[float] = None,
        token_burst: float = 0.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            requests_per_minute=requests_per_minute,
            request_burst=request_burst,
            tokens_per_minute=tokens_per_minute,
            token_burst=token_burst,
            **kwargs,
        )
```

Reserve `**kwargs` only for truly open-ended pass-through (e.g. forwarding to a third-party client), and in that case document what is accepted. This improves discoverability, lets pydantic enforce correctness, and keeps the public API self-describing.