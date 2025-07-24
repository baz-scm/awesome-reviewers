---
title: Network API precision
description: Use the appropriate Docker network API method based on the specific behavior
  you need. NetworkList and NetworkInspect have different matching behaviors that
  can lead to unexpected results if used incorrectly.
repository: docker/compose
label: Networking
language: Go
comments_count: 3
repository_stars: 35858
---

Use the appropriate Docker network API method based on the specific behavior you need. NetworkList and NetworkInspect have different matching behaviors that can lead to unexpected results if used incorrectly.

Key distinctions:
- `NetworkList` with name filter performs reliable exact matching when combined with post-filtering
- `NetworkInspect` performs prefix matching on both name and ID, which can cause ambiguous matches
- When disconnecting containers from networks, prefer `NetworkDisconnect` over container removal to preserve associated resources like anonymous volumes

Example of proper network resolution:
```go
// Use NetworkList for exact name matching
networks, err := s.apiClient().NetworkList(ctx, moby.NetworkListOptions{
    Filters: filters.NewArgs(filters.Arg("name", networkName)),
})
if err != nil {
    return err
}

// Filter for exact match since NetworkList can return partial matches
networks = utils.Filter(networks, func(net moby.NetworkResource) bool {
    return net.Name == networkName
})

// Check for proper labels to ensure it's the expected network
for _, net := range networks {
    if net.Labels[api.ProjectLabel] == expectedProjectLabel &&
       net.Labels[api.NetworkLabel] == expectedNetworkLabel {
        return nil
    }
}
```

This approach prevents issues like matching a network named `db` to a network with ID `db9086999caf` and ensures you're working with the intended network resource.