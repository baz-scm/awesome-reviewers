---
title: observability documentation structure
description: Use proper heading hierarchy instead of bold text formatting when documenting
  observability features like monitoring, failure points, and telemetry. This improves
  navigation, readability, and maintains consistent documentation structure across
  observability-related content.
repository: langflow-ai/langflow
label: Observability
language: Other
comments_count: 3
repository_stars: 111046
---

Use proper heading hierarchy instead of bold text formatting when documenting observability features like monitoring, failure points, and telemetry. This improves navigation, readability, and maintains consistent documentation structure across observability-related content.

Instead of using bold text for section organization:
```markdown
**Database Failure**:
* **Impact**: Disrupts flow retrieval, saving, user authentication...
* **Mitigation**: Use a replicated PostgreSQL setup...

**File System Issues**:
* **Impact**: Concurrency issues in file caching...
```

Use proper heading hierarchy:
```markdown
### Database failure

* **Impact**: Disrupts flow retrieval, saving, user authentication...
* **Mitigation**: Use a replicated PostgreSQL setup...

### File system issues

* **Impact**: Concurrency issues in file caching...
```

This approach makes observability documentation more scannable, enables proper table of contents generation, and follows standard documentation practices. Apply this consistently across monitoring guides, troubleshooting sections, telemetry documentation, and failure analysis content.