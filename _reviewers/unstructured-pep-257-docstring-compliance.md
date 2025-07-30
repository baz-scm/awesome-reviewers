---
title: PEP 257 docstring compliance
description: All public modules, classes, methods, and functions must have docstrings
  that follow PEP 257 formatting standards. This ensures consistent, professional
  documentation across the codebase.
repository: Unstructured-IO/unstructured
label: Documentation
language: Python
comments_count: 11
repository_stars: 12116
---

All public modules, classes, methods, and functions must have docstrings that follow PEP 257 formatting standards. This ensures consistent, professional documentation across the codebase.

**Required PEP 257 Format:**
- Use triple double-quotes (`"""`)
- First line must be a complete sentence that fits on one line
- For multi-line docstrings, add a blank line after the summary
- Closing triple-quotes on separate line for multi-line docstrings
- Describe the contract/purpose, not implementation details

**Examples:**

Single-line docstring:
```python
def get_nltk_data_dir() -> str | None:
    """The directory where `nltk` resources are located."""
```

Multi-line docstring:
```python
def clean_pdfminer_inner_elements(document: "DocumentLayout") -> "DocumentLayout":
    """Move pdfminer elements from inside tables to the extra_info dictionary.

    Each element appears in the `extra_info` dictionary using its table id as the key.
    """
```

Module docstring:
```python
"""NDJSON file utilities for document processing.

This module provides functionality for reading and writing newline-delimited JSON files.
Used primarily for batch processing of document elements during partitioning workflows.
"""
```

**Coverage Requirements:**
- All public modules should explain their purpose and usage
- All public classes should document their role and key methods  
- All public methods and functions require docstrings
- Internal functions benefit from docstrings for maintainability

This standard improves code discoverability, reduces onboarding time, and maintains professional documentation quality throughout the codebase.