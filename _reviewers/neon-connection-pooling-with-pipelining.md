---
title: Connection pooling with pipelining
description: 'Implement connection pooling with request pipelining for network services
  to optimize resource usage and improve throughput. Pool should manage three resource
  levels:'
repository: neondatabase/neon
label: Networking
language: Rust
comments_count: 4
repository_stars: 19015
---

Implement connection pooling with request pipelining for network services to optimize resource usage and improve throughput. Pool should manage three resource levels:

1. Channels (TCP connections): Share between multiple clients with HTTP/2 multiplexing
2. Clients: Acquire from channel pool, return when done
3. Streams: Reuse for multiple requests with controlled queue depth

Example implementation:
```rust
const CLIENTS_PER_CHANNEL: usize = 16;
const STREAM_QUEUE_DEPTH: usize = 2;

pub struct ChannelPool {
    channels: Mutex<BTreeMap<ChannelID, ChannelEntry>>,
}

pub struct ClientPool {
    channel_pool: Arc<ChannelPool>,
    idle: Mutex<BTreeMap<ClientID, ClientEntry>>,
}

pub struct StreamPool {
    client_pool: Arc<ClientPool>,
    streams: Arc<Mutex<HashMap<StreamID, StreamEntry>>>,
}
```

Key principles:
- Use HTTP/2 stream multiplexing to share TCP connections
- Pipeline multiple requests (queue depth 2-3) to mask network latency
- Return resources to pool promptly to enable reuse
- Implement proper backpressure through queue depth limits
- Consider cleanup of idle resources after timeout period