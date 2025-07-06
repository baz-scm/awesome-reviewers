---
title: Share documentation configs
description: Documentation tooling and configuration files should leverage shared/centralized
  resources rather than maintaining duplicate copies across repositories. This reduces
  maintenance burden, ensures consistency, and simplifies updates.
repository: apache/airflow
label: Documentation
language: Txt
comments_count: 2
repository_stars: 40858
---

Documentation tooling and configuration files should leverage shared/centralized resources rather than maintaining duplicate copies across repositories. This reduces maintenance burden, ensures consistency, and simplifies updates.

Examples:
1. For dependencies, prefer pyproject.toml over separate requirements files:
   ```python
   # Instead of separate requirements.txt files:
   # sphinx>=5.0
   # sphinx-autoapi>=1.8
   # sphinx-airflow-theme>=0.2.2
   
   # Use pyproject.toml with direct references when needed:
   [project.optional-dependencies]
   docs = [
       "sphinx>=5.0",
       "sphinx-autoapi>=1.8",
       "sphinx_airflow_theme @ https://github.com/apache/airflow-site/releases/download/0.2.3/sphinx_airflow_theme-0.2.3-py3-none-any.whl",
   ]
   ```

2. For configuration files like spelling wordlists, reference common resources:
   ```python
   # Use shared mechanism instead of duplicating large wordlists
   # uv run --group docs build-docs 
   # (will automatically use common spelling exclusion file from `airflow/docs`)
   ```

This approach ensures documentation tools stay consistent across projects and simplifies maintenance when standards change.