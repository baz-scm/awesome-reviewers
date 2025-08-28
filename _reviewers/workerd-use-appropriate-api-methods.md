---
title: Use appropriate API methods
description: When integrating with external APIs or implementing interface methods,
  ensure you're using the correct API calls for your intended functionality. Consult
  the official documentation and examples to understand the purpose and proper usage
  of different methods.
repository: cloudflare/workerd
label: API
language: Rust
comments_count: 2
repository_stars: 6989
---

When integrating with external APIs or implementing interface methods, ensure you're using the correct API calls for your intended functionality. Consult the official documentation and examples to understand the purpose and proper usage of different methods.

Common issues include:
- Using low-level execution APIs when high-level container management APIs are more appropriate
- Implementing incomplete interface methods without returning required object types
- Not following the documented API patterns and object models

For example, when working with Docker APIs, use `create_container()` and `start_container()` for container lifecycle management rather than `start_exec()` for command execution:

```rust
// Correct approach for container management
let config = ContainerCreateBody {
    image: Some(container_name.clone()),
    cmd: Some(entrypoint),
    env: Some(env),
    ..Default::default()
};

docker.create_container(Some(options), config).await?;
docker.start_container(&container_name, None::<StartContainerOptions>).await?;
```

When implementing RPC interfaces, ensure you return the correct object types as specified in the interface definition:

```rust
// Implement required server interface and return proper object type
fn get_tcp_port(&mut self, params: container::GetTcpPortParams, results: container::GetTcpPortResults) -> Promise<(), capnp::Error> {
    // Must implement rpc::Container::Port::Server and return that object
}
```

Always reference the official documentation, API specifications, and existing examples to verify you're using the intended methods for your use case.