---
title: Handle network interrupts safely
description: 'Network code must properly handle interrupts and maintain consistent
  connection state at all potential interruption points. When implementing network
  operations:'
repository: neondatabase/neon
label: Networking
language: C
comments_count: 2
repository_stars: 19015
---

Network code must properly handle interrupts and maintain consistent connection state at all potential interruption points. When implementing network operations:

1. Check for interrupts at all blocking points, including connection attempts, I/O operations, and sleep/delay intervals
2. Reset all connection-specific state when disconnecting due to errors or timeouts
3. Implement robust retry logic that can survive interrupted operations
4. Ensure proper state cleanup even when operations are canceled mid-execution

Example of robust network code with proper interrupt handling:

```c
/* Ensure proper state cleanup during reconnection attempts */
while (us_since_last_attempt < shard->delay_us)
{
    pg_usleep(shard->delay_us - us_since_last_attempt);
    
    /* Handle interrupts during backoff periods */
    CHECK_FOR_INTERRUPTS();
    
    now = GetCurrentTimestamp();
    us_since_last_attempt = (int64) (now - shard->last_reconnect_time);
}

/* For network operations, ensure proper sequencing with error handling */
while (!page_server->send(shard_no, &request.hdr)
        || !page_server->flush(shard_no)
        || !consume_prefetch_responses())
{
    /* Loop until all network operations complete successfully */
    /* Each step should properly handle connection failures */
}

/* When disconnecting, reset all protocol-specific state */
void disconnect(int shard_no)
{
    pageserver_disconnect_shard(shard_no);
    prefetch_on_ps_disconnect(shard_no); /* Reset protocol state */
}
```

Failing to properly handle interrupts in network code can lead to connection leaks, protocol inconsistencies, and hard-to-debug timeout issues.