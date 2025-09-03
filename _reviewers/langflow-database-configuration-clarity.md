---
title: Database configuration clarity
description: When documenting database configuration or setup procedures, provide
  specific, actionable instructions with clear verification steps. Always specify
  which database backend is being used and include concrete examples for verification.
repository: langflow-ai/langflow
label: Database
language: Other
comments_count: 4
repository_stars: 111046
---

When documenting database configuration or setup procedures, provide specific, actionable instructions with clear verification steps. Always specify which database backend is being used and include concrete examples for verification.

Key practices:
- Use actionable language in prerequisites (e.g., "Create a PostgreSQL database" instead of "A PostgreSQL database")
- Break down verification steps into clear, executable commands
- Specify the exact database being referenced (e.g., "your Langflow .env file" instead of "your .env file")
- Include specific SQL queries or commands for verification
- Clarify when different database backends (SQLite vs PostgreSQL) affect component behavior

Example of good database verification documentation:
```
5. To verify the configuration, create any flow using the Langflow UI or API, and then query your database to confirm new tables and activity.
    
    * Query the database container:
    
        ```
        docker exec -it <postgres-container> psql -U langflow -d langflow
        ```
    
    * Use SQL:
    
        ```
        SELECT * FROM pg_stat_activity WHERE datname = 'langflow';
        ```
```

This approach ensures users can successfully configure and verify their database setup, reducing support issues and improving the development experience.