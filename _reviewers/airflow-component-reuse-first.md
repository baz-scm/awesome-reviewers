---
title: Component reuse first
description: 'Always prioritize reusing existing components before creating new ones.
  This practice improves codebase consistency, reduces maintenance burden, and prevents
  duplication. When implementing new UI elements:'
repository: apache/airflow
label: React
language: TSX
comments_count: 4
repository_stars: 40858
---

Always prioritize reusing existing components before creating new ones. This practice improves codebase consistency, reduces maintenance burden, and prevents duplication. When implementing new UI elements:

1. First search your codebase for similar functionality (e.g., search bars, filters, icons)
2. Use components from your UI library consistently rather than mixing with HTML elements
3. Choose the simplest component that satisfies requirements

**Example - Bad:**
```jsx
// Creating a new input component when a SearchBar already exists
<InputGroup startElement={<FiHash size={14} />}>
  <Input
    maxW="200px"
    onChange={handleRunIdChange}
    placeholder={translate("dags:filters.runIdFilter")}
    value={filteredRunId ?? ""}
  />
</InputGroup>
```

**Example - Good:**
```jsx
// Reusing the existing SearchBar component
<SearchBar
  onChange={handleRunIdChange}
  placeholder={translate("dags:filters.runIdFilter")}
  value={filteredRunId ?? ""}
/>
```

**Example - Bad:**
```jsx
// Custom SVG implementation
const ChevronDownIcon = () => (
  <svg fill="currentColor" height="1em" viewBox="0 0 20 20" width="1em">
    <path
      clipRule="evenodd"
      d="M5.23 7.21a.75.75 0 011.06.02L10 11.085l3.71-3.855a.75.75 0 111.08 1.04l-4.24 4.4a.75.75 0 01-1.08 0l-4.24-4.4a.75.75 0 01.02-1.06z"
      fillRule="evenodd"
    />
  </svg>
);
```

**Example - Good:**
```jsx
// Using existing icon library
import { FiChevronDown } from "react-icons/fi";

// Then in your component
<FiChevronDown />
```

Additionally, maintain framework consistency by using framework-specific patterns (like Chakra UI factories) rather than mixing with HTML elements:

```jsx
// Instead of <details>...</details>
<chakra.details open={open} w="100%">
  {/* content */}
</chakra.details>
```

This approach ensures better styling consistency, accessibility support, and reduces the need to reinvent existing functionality.