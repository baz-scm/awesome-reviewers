---
title: Environment-specific database configuration
description: Configure database connections differently based on the environment.
  Use lightweight file-based databases like SQLite for development and testing, but
  deploy robust server-based databases like PostgreSQL in production. This approach
  simplifies local development while ensuring your application has appropriate scalability
  and reliability in production.
repository: fastapi/fastapi
label: Database
language: Markdown
comments_count: 2
repository_stars: 86871
---

Configure database connections differently based on the environment. Use lightweight file-based databases like SQLite for development and testing, but deploy robust server-based databases like PostgreSQL in production. This approach simplifies local development while ensuring your application has appropriate scalability and reliability in production.

```python
import os
from sqlalchemy import create_engine

# Get environment from configuration
environment = os.getenv('APP_ENV', 'development')

# Configure database based on environment
if environment == 'development':
    # SQLite for local development
    DATABASE_URL = "sqlite:///./app.db"
elif environment == 'testing':
    # In-memory SQLite for testing
    DATABASE_URL = "sqlite:///./test.db"
else:
    # PostgreSQL for production
    DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db_name}"

# Create engine with appropriate configurations
engine = create_engine(
    DATABASE_URL,
    # Add production-specific settings like connection pooling
    pool_size=5 if environment == 'production' else 0,
    max_overflow=10 if environment == 'production' else 0
)
```

This pattern ensures developers can work efficiently with lightweight database setups while maintaining robust configurations for production environments. Remember to properly manage the `engine` object throughout your application as it maintains database connections. For production applications, consider additional settings like connection pooling, timeouts, and SSL configurations appropriate for your specific database provider.