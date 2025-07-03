---
title: Isolate configuration concerns
description: Keep configuration settings separate from application code by using environment
  variables or dedicated configuration files. This promotes better maintainability,
  security, and flexibility across different deployment environments.
repository: fastapi/fastapi
label: Configurations
language: Markdown
comments_count: 8
repository_stars: 86871
---

Keep configuration settings separate from application code by using environment variables or dedicated configuration files. This promotes better maintainability, security, and flexibility across different deployment environments.

### Key practices:

1. **Use environment variables for sensitive or environment-specific configuration**
   ```python
   import os
   
   # Read configuration from environment variables with defaults
   database_url = os.getenv("DATABASE_URL", "sqlite:///default.db")
   debug_mode = os.getenv("DEBUG_MODE", "False") == "True"
   ```

2. **Isolate project dependencies with virtual environments**
   Create virtual environments for each project to manage dependencies independently and avoid conflicts:
   ```console
   $ python -m venv .venv
   $ source .venv/bin/activate  # Linux/macOS
   $ .venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. **Document configuration options clearly**
   Provide comprehensive documentation of all configuration options, including:
   - Expected variable types
   - Default values
   - Example usage
   - Possible values and their impact

4. **Consider using a centralized configuration manager**
   For more complex applications, implement a dedicated configuration class:
   ```python
   from pydantic_settings import BaseSettings
   
   class Settings(BaseSettings):
       database_url: str = "sqlite:///default.db"
       api_key: str
       debug_mode: bool = False
       
       class Config:
           env_file = ".env"
   
   settings = Settings()
   ```

By separating configuration from code, you can adapt your application to different environments without changing the codebase, simplify testing, and enhance security by keeping sensitive information out of your repository.