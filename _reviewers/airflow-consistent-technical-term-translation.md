---
title: Consistent technical term translation
description: 'When localizing an application, maintain consistent conventions for
  technical terms while respecting language-specific rules:


  1. For acronyms, follow the target language''s capitalization conventions:'
repository: apache/airflow
label: Naming Conventions
language: Json
comments_count: 4
repository_stars: 40858
---

When localizing an application, maintain consistent conventions for technical terms while respecting language-specific rules:

1. For acronyms, follow the target language's capitalization conventions:
   - In English: Use "Dag" with capitalized first letter only (not "DAG")
   - In Spanish: Use full capitalization for acronyms ("DAG") as per RAE guidelines

2. For technical terms, prioritize what's familiar to developers in that language:
   - Keep universally recognized technical terms in English when they're commonly used by developers in the target language (e.g., "heartbeat", "token", "backend")
   - Use localized versions when they're more recognized by developers in that language (e.g., "커넥션" instead of "연결" for "connections" in Korean)

3. Be consistent within each language across the entire application:
   ```json
   // English
   "dag_one": "Dag",
   "dagRun_one": "Dag Run",
   
   // Spanish
   "dag_one": "DAG",
   "dagRun_one": "Ejecución del DAG"
   ```

This approach ensures that the UI remains intuitive for developers working in different languages while respecting established conventions in each target language.