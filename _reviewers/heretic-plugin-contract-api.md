---
title: plugin contract API
description: 'Define a clear, minimal plugin contract and loader API for all external/
  built-in plugins. Motivation: plugins (taggers/scorers) are the public extension
  points of the system and must declare what data they need, how they initialize,
  and be loadable from arbitrary modules so users can provide custom implementations
  without modifying the project.'
repository: p-e-w/heretic
label: API
language: Python
comments_count: 9
repository_stars: 5002
---

Define a clear, minimal plugin contract and loader API for all external/ built-in plugins. Motivation: plugins (taggers/scorers) are the public extension points of the system and must declare what data they need, how they initialize, and be loadable from arbitrary modules so users can provide custom implementations without modifying the project.

Rules and how to apply them:
- Declarative requirements: each plugin class must provide classmethods that declare required fields. Example methods: required_response_metadata_fields() -> list[str], required_context_metadata_fields() -> list[str]. The core app will call these before invoking the plugin and instruct the Model to only return requested fields.

- Optional heavy fields: plugins must indicate whether they need the full response text or only a prefix/n tokens. Make this configurable so the model can avoid returning expensive data when unnecessary (e.g., include_text() -> bool or text_token_limit() -> int).

- Settings schema: plugins may declare a pydantic BaseModel subclass as `settings` to validate plugin-specific configuration. The loader should instantiate plugin settings from the global config.

- Lifecycle hooks and validation: enforce a small lifecycle surface. Plugins must not define __init__(); instead provide an init(ctx) -> None hook for initialization and an optional start(ctx) for runtime setup. Provide a validate_contract() classmethod that the loader calls to enforce these rules and raise clear errors.

- Loader API: implement a loader that accepts both built-in names and arbitrary module paths (e.g., "heretic.taggers.builtin", "~/my_plugins/custom_tagger.py:MyTagger", or "package.module:ClassName"). The loader must:
  - resolve either a package-qualified plugin or a file/module path
  - import and locate the plugin class
  - call plugin.validate_contract()
  - read plugin.required_* methods and configure the Model/Context accordingly (e.g., model.set_requested_response_fields(...))
  - instantiate the plugin with the canonical constructor arguments (settings, model/context, etc.)

- Keep APIs minimal and consistent: plugin methods should accept explicit typed objects, not ad-hoc arg lists. Use small domain objects like Response and Context rather than multiple parallel arguments. Example Response: Response(text: str | None, metadata: dict[str, Any], tokens: Optional[list[int]]). Make fields optional and typed so callers know what's available.

Example usage (illustrative):

# Plugin class (sketch)
class MyTagger(TaggerBase):
    @classmethod
    def required_response_metadata_fields(cls) -> list[str]:
        return ["logprobs", "finish_reason"]

    @classmethod
    def include_text(cls) -> bool:
        return False  # avoids returning full text when not needed

    @classmethod
    def validate_contract(cls) -> None:
        # ensure no __init__ and required methods exist
        ...

    def init(self, ctx: Context) -> None:
        # optional initialization using provided Context
        ...

    def tag_batch(self, responses: list[Response]) -> list[dict[str, float]]:
        ...

# Loader usage (sketch)
plugin_cls = load_plugin(name=settings.tagger)  # accepts package name or module:path
plugin_cls.validate_contract()
model.set_requested_response_fields(plugin_cls.required_response_metadata_fields())
model.set_requested_context_fields(plugin_cls.required_context_metadata_fields())
plugin = plugin_cls(settings=settings, model=model, context_metadata=model.get_context_metadata())
plugin.init(Context(settings=settings, model=model))

Rationale: This rule prevents fragile implicit contracts, avoids unnecessary data transfers (performance), enables third-party plugin distribution without altering core code, and makes plugin initialization predictable and testable. Following it reduces bugs from mismatched expectations (missing fields, incorrect init semantics, hardcoded package names) and simplifies upgrading third-party libraries by keeping argument names and responsibilities explicit.