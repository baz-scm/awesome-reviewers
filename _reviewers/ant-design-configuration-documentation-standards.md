---
title: Configuration documentation standards
description: Ensure configuration properties and settings are documented with consistent
  formatting and precise specifications. Configuration property names should be wrapped
  in backticks for proper formatting in documentation and changelogs. Version dependencies
  must specify exact version ranges rather than vague references like "latest version".
  Documentation should...
repository: ant-design/ant-design
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 95882
---

Ensure configuration properties and settings are documented with consistent formatting and precise specifications. Configuration property names should be wrapped in backticks for proper formatting in documentation and changelogs. Version dependencies must specify exact version ranges rather than vague references like "latest version". Documentation should clearly describe what each configuration controls and its impact.

Examples of proper formatting:
- ✅ `Button 组件支持 `shape` 全局配置` (property name in backticks)
- ✅ `使用 @ant-design/icons@5.x 配合 antd@5.x` (specific version ranges)
- ✅ `Tooltip 的渲染节点，默认渲染到 body 上` (clear description of what the configuration controls)

This standard helps maintain consistency across documentation, prevents version compatibility issues, and ensures developers understand exactly what each configuration option does and how to use it properly.