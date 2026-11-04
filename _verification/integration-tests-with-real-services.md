---
title: "Integration tests with real services"
code: "V1019.002"
slug: "integration-tests-with-real-services"
technique: "Unit and integration tests"
technique_id: "V1019"
technique_slug: "unit-and-integration-tests"
tactic: "Testing"
tactic_id: "VA04"
description: "Run against real databases and queues in containers instead of mocks."
repos: 0
craft:
  - "Start the real database or queue in a container from the test setup."
  - "Run storage and messaging tests against that container, not a mock."
  - "Tear down the containers after each test run."
reverse:
  - "Testcontainers imports or container definitions in the test suite."
  - "A docker-compose file that the test job or a test fixture uses."
  - "CI jobs that enable a container runtime for the test step."
packages:
  - id: "testcontainers"
    name: "Testcontainers (Python)"
    url: "https://github.com/testcontainers/testcontainers-python"
tools: []
examples: []
---
