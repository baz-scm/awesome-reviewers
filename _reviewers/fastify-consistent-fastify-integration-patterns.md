---
title: "Consistent Fastify Integration Patterns"
description: "When implementing integrations and plugins using the Fastify framework, maintain consistent coding patterns and conventions: follow Fastify's recommended package naming conventions, ensure integrations provide clear and comprehensive documentation, use Fastify's built-in type definitions and decorators consistently, and include full RFC references when referencing external protocol standards."
repository: "fastify/fastify"
label: "Fastify"
language: "TypeScript"
comments_count: 3
repository_stars: 34000
---

When implementing integrations and plugins using the Fastify framework, maintain consistent coding patterns and conventions:

1. Follow Fastify's recommended package naming conventions, using the `@fastify` scope for all Fastify-specific packages (e.g. `@fastify/kafka` instead of `fastify-kafka`).
2. Ensure integrations provide clear and comprehensive documentation of the specific protocol, system or service being integrated (e.g. "Plugin to interact with Apache Kafka message broker").
3. Use Fastify's built-in type definitions and decorators consistently across all plugins and integrations.
4. When referencing external protocol standards, include the full RFC reference with a period at the end of the description (e.g. "Plugin to add HTTP 103 Early Hints based on [RFC 8297](https://httpwg.org/specs/rfc8297.html).").

Example Fastify integration:

```typescript
import fastify, { FastifyInstance } from 'fastify';
import { FastifyKafka } from '@fastify/kafka';

const server: FastifyInstance = fastify();

server.register(FastifyKafka, {
  brokers: ['kafka1:9092', 'kafka2:9092'],
  topic: 'my-topic'
});

server.get('/messages', async (request, reply) => {
  const messages = await server.kafka.consume();
  return messages;
});
```

Consistent implementation of Fastify integrations and plugins improves maintainability, makes resources easier to discover, and ensures developers can quickly understand the purpose and usage of network-related features in Fastify applications.