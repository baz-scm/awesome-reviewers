---
title: "Strict docs build"
code: "V1010.001"
slug: "strict-docs-build"
technique: "Documentation build"
technique_id: "V1010"
technique_slug: "documentation-build"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Treat warnings as errors (sphinx -W, mkdocs --strict)."
repos: 19
craft:
  - "Run sphinx-build with -W or mkdocs build with --strict in CI."
  - "Fix existing warnings before turning the flag on."
  - "Fail the docs job on broken references, missing navigation entries and bad markup."
reverse:
  - "A docs job in CI running sphinx-build -W or mkdocs build --strict."
  - "A docs/conf.py or mkdocs.yml file in the repository."
packages:
  - id: "sphinx"
    name: "Sphinx"
    url: "https://github.com/sphinx-doc/sphinx"
  - id: "mkdocs"
    name: "MkDocs"
    url: "https://github.com/mkdocs/mkdocs"
tools:
  - name: "sphinx"
    repos: 9
  - name: "mkdocs"
    repos: 11
examples:
  - repo: "TheAlgorithms/Python"
    tool: "sphinx"
    command: "sphinx-build -c docs . docs/_build/html"
  - repo: "pallets/flask"
    tool: "sphinx"
    command: "sphinx-build -E -W -b dirhtml docs docs/_build/dirhtml"
  - repo: "traefik/traefik"
    tool: "mkdocs"
    command: "mkdocs build --strict"
  - repo: "astral-sh/ruff"
    tool: "mkdocs"
    command: "mkdocs build --strict -f mkdocs.yml"
  - repo: "celery/celery"
    tool: "sphinx"
    command: "sphinx-build -j2 -b apicheck -d {envtmpdir}/doctrees docs docs/_build/apicheck"
---
