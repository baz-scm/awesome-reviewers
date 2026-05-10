---
title: Use explicit types
description: "在组件/页面代码中保持表达清晰、类型明确，避免冗余与 `any`。\n\n- 布尔表达式：不要写 `flag ? true : false`，可直接传布尔值本身。\n\
  \  - 例如：\n    ```tsx\n    // bad\n    multiple={data.is_list ? true : false}"
repository: eosphoros-ai/DB-GPT
label: Code Style
language: TSX
comments_count: 3
repository_stars: 18703
---

在组件/页面代码中保持表达清晰、类型明确，避免冗余与 `any`。

- 布尔表达式：不要写 `flag ? true : false`，可直接传布尔值本身。
  - 例如：
    ```tsx
    // bad
    multiple={data.is_list ? true : false}

    // good
    multiple={data.is_list}
    ```

- 类型标注：不要使用 `any` 作为 `props` 或关键数据类型；为 `props`、组件内数据（如 `importData`）补充明确的 TypeScript 类型。
  - 例如：
    ```tsx
    type ImportData = {/* 字段按实际补齐 */};

    const Canvas: React.FC<{ importData: ImportData | null }> = ({ importData }) => {
      // ...
      return null;
    };
    ```

- 代码组织：与组件强相关的变量/数据尽量放到组件内部或通过 props 传入，避免“全局/外部裸变量 + any”的写法。

这些规则能提升可读性、减少潜在类型错误，并使代码更易维护。