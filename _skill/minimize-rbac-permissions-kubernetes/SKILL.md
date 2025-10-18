---
name: minimize-rbac-permissions-kubernetes
description: "Apply the principle of least privilege to Kubernetes RBAC rules by only granting the minimal permissions each component needs."
---

# Minimize RBAC Permissions (Kubernetes)

Kubernetes clusters use RBAC (Role-Based Access Control) to govern what actions components can perform. From a security perspective, each role should have only the permissions absolutely required and nothing more[30]. Reviewers should inspect Kubernetes configuration or code for RBAC definitions and flag overly broad access:

- **Least privilege for each role.** For every API group, resource, and verb in a Role/ClusterRole, ask “does this component truly need this permission?” If not, remove it[30].
- **Avoid broad verbs.** Instead of granting a role all possible actions (`get`, `list`, `watch`, `create`, `update`, `patch`, `delete`) on a resource, give it only what it uses. For example, if a controller only needs to update a resource’s status, it likely doesn’t need `delete` or `list` on that resource[31].
- **Review cluster-scoped rights.** Especially scrutinize permissions on `""` (core API) and cluster-wide resources. Namespaced components often do not need cluster-wide access.
- **Justify each rule.** Treat each rule line in the YAML as suspect unless there is a clear justification from the code/docs that the component uses that capability.

For instance, Kubernetes maintainers often catch PRs where a role was given `['get', 'list', 'patch', 'update', 'watch']` on a resource, and trim it down to just `['update']` because only updates were necessary[31]. Tightening permissions reduces the attack surface and potential impact if a component is compromised. This makes the cluster more secure by default[30].
