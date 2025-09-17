---
title: Effect-based API clients
description: Use Effect-based HTTP clients with specific error types instead of throwing
  generic exceptions or relying on third-party HTTP libraries like axios. API functions
  should return Effects with proper error types rather than throwing errors, enabling
  better error handling and composability.
repository: unionlabs/union
label: API
language: TypeScript
comments_count: 4
repository_stars: 74800
---

Use Effect-based HTTP clients with specific error types instead of throwing generic exceptions or relying on third-party HTTP libraries like axios. API functions should return Effects with proper error types rather than throwing errors, enabling better error handling and composability.

Instead of extending third-party clients or using axios directly:
```typescript
// ❌ Avoid - throws errors, uses axios
async queryContractSmartAtHeight(contract: string, queryMsg: Record<string, unknown>, height: number) {
  const resp = await axios.get(url, { headers: { "x-cosmos-block-height": height.toString() } })
  if (resp.status < 200 || resp.status >= 300) {
    throw new Error(`HTTP ${resp.status}: ${JSON.stringify(resp.data)}`)
  }
  return resp.data
}
```

Use effectful wrappers with specific error types:
```typescript
// ✅ Preferred - Effect-based with specific errors
export type FetchDecodeGraphqlError = GraphQLError | Persistence.PersistenceError | ParseError

export const fetchDecodeGraphql = <S, E, D, V extends Variables = Variables>(
  schema: Schema.Schema<S, E>,
  document: TadaDocumentNode<D, V>,
  variables?: V,
): Effect.Effect<S, FetchDecodeGraphqlError, GraphQL> =>
  Effect.andThen(GraphQL, ({ fetch }) =>
    pipe(
      fetch(new GraphQLRequest({ document, variables })),
      Effect.flatMap(Schema.decodeUnknown(schema))
    )
  )
```

This approach provides meaningful error information, enables proper error composition, and maintains consistency with the Effect-based architecture throughout the codebase.