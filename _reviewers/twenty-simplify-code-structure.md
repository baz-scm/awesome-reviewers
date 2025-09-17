---
title: simplify code structure
description: 'Write code that is easy to read and understand by avoiding unnecessary
  complexity in structure and logic. This includes several key practices:


  **Avoid complex nesting and nested ternaries:**'
repository: twentyhq/twenty
label: Code Style
language: TSX
comments_count: 8
repository_stars: 35477
---

Write code that is easy to read and understand by avoiding unnecessary complexity in structure and logic. This includes several key practices:

**Avoid complex nesting and nested ternaries:**
```javascript
// ❌ Hard to read with nesting
const result = isStandardizedFormat ? (
  toolOutput && typeof toolOutput === 'object' && 'success' in toolOutput ? 
    Boolean(toolOutput.result) : 
    Boolean(toolResult?.result)
) : false;

// ✅ Split into clear, explicit steps
const isStandardizedFormat = toolOutput && typeof toolOutput === 'object' && 'success' in toolOutput;
const hasResult = isStandardizedFormat 
  ? Boolean(toolOutput.result)
  : Boolean(toolResult?.result);
```

**Simplify boolean comparisons:**
```javascript
// ❌ Unnecessary explicit comparison
if (hasAnySoftDeleteFilter === true) {

// ✅ Direct boolean usage
if (hasAnySoftDeleteFilter) {
```

**Prefer switch statements over if-else chains:**
```javascript
// ❌ Long if-else chain
if (activeTabId === ROLES_LIST_TABS.TABS_IDS.USER_ROLES) {
  matchesTab = role.canBeAssignedToUsers;
} else if (activeTabId === ROLES_LIST_TABS.TABS_IDS.AGENT_ROLES) {
  matchesTab = role.canBeAssignedToAgents;
} else if (activeTabId === ROLES_LIST_TABS.TABS_IDS.API_KEY_ROLES) {
  matchesTab = role.canBeAssignedToApiKeys;
}

// ✅ Clear switch statement
switch (activeTabId) {
  case ROLES_LIST_TABS.TABS_IDS.USER_ROLES:
    return role.canBeAssignedToUsers;
  case ROLES_LIST_TABS.TABS_IDS.AGENT_ROLES:
    return role.canBeAssignedToAgents;
  case ROLES_LIST_TABS.TABS_IDS.API_KEY_ROLES:
    return role.canBeAssignedToApiKeys;
  default:
    return role.canBeAssignedToUsers;
}
```

**Use early returns to reduce nesting:**
```javascript
// ❌ Nested conditions
const rolesOptions = rolesData?.getRoles?.reduce((acc, role) => {
  if (role.canBeAssignedToAgents) {
    acc.push({ label: role.label, value: role.id });
  }
  return acc;
}, []);

// ✅ Early return pattern
const rolesOptions = rolesData?.getRoles?.reduce((acc, role) => {
  if (!role.canBeAssignedToAgents) return acc;
  
  acc.push({ label: role.label, value: role.id });
  return acc;
}, []);
```

**Prefer functional methods for better readability:**
```javascript
// ❌ Nested forEach loops
data.forEach((dataPoint, dataIndex) => {
  keys.forEach((key, keyIndex) => {
    configs.push(createConfig(dataPoint, key, keyIndex));
  });
});

// ✅ Functional approach with flatMap
const configs = data.flatMap((dataPoint, dataIndex) =>
  keys.map((key, keyIndex) => createConfig(dataPoint, key, keyIndex))
);
```

The goal is to make code self-documenting and reduce cognitive load for other developers. When code structure is simple and clear, it's easier to understand, debug, and maintain.