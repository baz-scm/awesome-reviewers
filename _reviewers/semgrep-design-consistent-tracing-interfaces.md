---
title: Design consistent tracing interfaces
description: When implementing observability features like tracing, prioritize consistent
  and extensible API design. Use structured annotations that can accommodate future
  configuration options rather than simple flags. Place tracing instrumentation directly
  on the functions being measured rather than creating wrapper functions. Follow established
  naming conventions...
repository: semgrep/semgrep
label: Observability
language: Other
comments_count: 4
repository_stars: 12598
---

When implementing observability features like tracing, prioritize consistent and extensible API design. Use structured annotations that can accommodate future configuration options rather than simple flags. Place tracing instrumentation directly on the functions being measured rather than creating wrapper functions. Follow established naming conventions that align with other similar tools in your ecosystem.

For tracing annotations, prefer extensible syntax like `[@@trace { level = Debug }]` over simple flags like `[@@trace_debug]`, as this provides a more consistent design with other ppx extensions and allows for future expansion of configuration options.

Place tracing annotations directly on the target functions rather than creating wrapper functions:

```ocaml
(* Preferred: Direct annotation *)
let rules_from_rule_source config = 
  (* implementation *)
[@@trace]

(* Avoid: Wrapper function *)
let get_rules config =
  Common.with_time (fun () -> rules_from_rule_source config)
[@@trace]
```

For API parameters, use direct parameters instead of optional ones when the value is always computed:

```ocaml
(* Preferred: Direct parameter *)
let config = Opentelemetry_client_ocurl.Config.make ~url () in
Opentelemetry_client_ocurl.with_setup ~config () @@ fun () ->

(* Avoid: Unnecessary optional *)
let config = Some (Opentelemetry_client_ocurl.Config.make ~url ()) in
Opentelemetry_client_ocurl.with_setup ?config () @@ fun () ->
```

This approach ensures your observability instrumentation remains maintainable, follows predictable patterns, and can evolve with changing requirements.