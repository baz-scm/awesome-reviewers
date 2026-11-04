# Awesome Reviewers

Review and verification techniques for code, in one place.

- **Reviewers** — instructions distilled from real code review discussions in production repositories.
- **Verification** — techniques for building a check and recognising it in a repository, grouped by tactic.

Browse at [awesomereviewers.com](https://awesomereviewers.com). Search with `/`, filter by type,
category or language, and copy an instruction from its page.

## Contributing

Add a reviewer as `_reviewers/<slug>.md` with the front matter described in [CLAUDE.md](CLAUDE.md).
Add a verification technique as `_verification/<slug>.md`. Then run:

```bash
python -m unittest discover -s tests -t .
bundle exec jekyll build
```

## License

Apache-2.0. See [LICENSE](LICENSE).
