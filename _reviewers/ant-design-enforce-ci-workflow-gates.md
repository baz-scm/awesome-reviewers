---
title: Enforce CI workflow gates
description: Establish and enforce proper CI/CD workflow gates to maintain code quality
  and release safety. This includes preventing direct commits to protected branches
  and validating CI status before releases.
repository: ant-design/ant-design
label: CI/CD
language: TypeScript
comments_count: 2
repository_stars: 95882
---

Establish and enforce proper CI/CD workflow gates to maintain code quality and release safety. This includes preventing direct commits to protected branches and validating CI status before releases.

Key practices:
1. **Branch Protection**: Avoid direct commits to master/main branches. Use feature branches and pull requests instead: `git checkout -b feature-branch` rather than committing directly to master.

2. **Release Gating**: Implement proper CI validation before releases. When CI is pending, either wait for completion or implement fallback validation (like running local CI checks) rather than bypassing all checks.

3. **Risk Assessment**: When considering CI bypasses, evaluate alternatives such as checking only critical CI jobs (e.g., artifact builds) or requiring local validation as a safety net.

Example from release script:
```typescript
if (data.state === 'pending') {
  const shouldSkip = await confirm({
    message: '是否要跳过 CI 检查继续发布？',
    default: false,
  });
  
  if (!shouldSkip) {
    showMessage('已取消发布，请等待 CI 完成后再试', 'fail');
    process.exit(1);
  }
  // Consider running local CI as fallback validation
}
```

This approach balances development velocity with code quality by ensuring proper workflow gates are respected while providing escape hatches for legitimate edge cases.