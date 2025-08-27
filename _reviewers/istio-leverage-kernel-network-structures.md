---
title: leverage kernel network structures
description: When implementing eBPF networking programs, prefer using kernel-native
  data structures and BPF helpers over maintaining custom eBPF maps that duplicate
  network routing information. The kernel already tracks IP-to-MAC mappings, interface
  information, and routing data through its networking stack.
repository: istio/istio
label: Networking
language: C
comments_count: 3
repository_stars: 37192
---

When implementing eBPF networking programs, prefer using kernel-native data structures and BPF helpers over maintaining custom eBPF maps that duplicate network routing information. The kernel already tracks IP-to-MAC mappings, interface information, and routing data through its networking stack.

Instead of creating and maintaining parallel eBPF maps with pod IP addresses, interface indices, and MAC addresses, use BPF helpers like `bpf_fib_lookup()` to dynamically query the kernel's existing network state. This approach offers several advantages:

1. **Reduces complexity**: Eliminates the need for userspace programs to constantly update eBPF maps with network state changes
2. **Avoids state synchronization**: No risk of eBPF maps becoming out of sync with actual kernel network state  
3. **Improves maintainability**: Less custom state tracking code in both kernel and userspace components
4. **Handles scale better**: No need to pre-allocate map sizes or worry about map size limits

Example of the preferred approach:
```c
// Instead of maintaining custom pod routing maps:
// struct { ... } app_info SEC(".maps");

// Use kernel helpers for dynamic lookup:
SEC("tc")
int network_redirect(struct __sk_buff *skb) {
    // Use bpf_fib_lookup to get device/MAC from dest IP
    struct bpf_fib_lookup fib_params = {};
    // ... populate fib_params from packet data
    int ret = bpf_fib_lookup(skb, &fib_params, sizeof(fib_params), 0);
    if (ret == BPF_FIB_LKUP_RET_SUCCESS) {
        // Use fib_params.ifindex and fib_params.dmac
        return bpf_redirect(fib_params.ifindex, 0);
    }
}
```

This principle applies especially when the custom eBPF map would contain information that's already available through kernel networking APIs and BPF helpers.