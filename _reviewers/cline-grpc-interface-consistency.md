---
title: gRPC interface consistency
description: Ensure gRPC/RPC interfaces follow consistent patterns for return types,
  error handling, and method design. Avoid creating duplicate RPC methods when existing
  ones can be reused, use proper gRPC clients instead of direct imports, and maintain
  type safety with specific parameter types rather than generic objects.
repository: cline/cline
label: API
language: TypeScript
comments_count: 6
repository_stars: 48299
---

Ensure gRPC/RPC interfaces follow consistent patterns for return types, error handling, and method design. Avoid creating duplicate RPC methods when existing ones can be reused, use proper gRPC clients instead of direct imports, and maintain type safety with specific parameter types rather than generic objects.

Key principles:
- Return proper protobuf types (e.g., `Promise<Empty>` not `Promise<void>`) to ensure compatibility across different platforms
- Use native gRPC error mechanisms instead of custom error response fields
- Avoid duplicate RPC methods - check if existing host bridge methods can fulfill the requirement before creating new ones
- Use gRPC clients for cross-platform calls instead of direct platform-specific imports
- Define specific typed fields instead of generic `values: Record<string, any>` objects

Example of proper gRPC handler:
```typescript
// Good - proper return type and error handling
export async function addRemoteMcpServer(
  controller: Controller, 
  request: AddRemoteMcpServerRequest
): Promise<McpServers> {
  if (!request.serverName) {
    throw new Error("Server name is required") // Native gRPC error
  }
  
  const servers = await controller.mcpHub?.addRemoteServer(request.serverName, request.serverUrl)
  return { mcpServers: convertMcpServersToProtoMcpServers(servers) }
}

// Bad - generic response with custom error handling
interface CustomResponse {
  success: boolean
  error?: string
  values?: Record<string, any>
}
```

This ensures API interfaces are predictable, type-safe, and work consistently across different client implementations.