---
title: Document CI/CD workflows clearly
description: When documenting CI/CD processes, build pipelines, or deployment workflows,
  use clear and precise language that helps developers understand the sequence of
  operations. Write in present tense to describe what tools do, and provide explicit
  references when explaining examples.
repository: docker/compose
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 35858
---

When documenting CI/CD processes, build pipelines, or deployment workflows, use clear and precise language that helps developers understand the sequence of operations. Write in present tense to describe what tools do, and provide explicit references when explaining examples.

Key practices:
- Use present tense when describing tool behavior (e.g., "Dry run mode shows..." instead of "will show...")
- Provide clear references to examples (e.g., "From the example above, you can see..." instead of "You could see...")
- Explain workflow steps in logical order with clear transitions

Example of clear CI/CD documentation:
```
### Use Dry Run mode to test your command

Use `--dry-run` flag to test a command without changing your application stack state.
Dry Run mode shows you all the steps Compose applies when executing a command, for example:

```console
$ docker compose --dry-run up --build -d
[+] Running 10/8
 ✔ DRY-RUN MODE -  Container nginx-golang-mysql-db-1     Created
 ✔ DRY-RUN MODE -  Container nginx-golang-mysql-backend-1 Created
```

From the example above, you can see that the first step is to pull the image defined by `db` service, then build the `backend` service.
```

This approach ensures that team members can easily follow and understand CI/CD processes, reducing confusion during deployment and build operations.