---
layout: page
title: Contact
permalink: /contact/
description: Where to report a wrong instruction, request a repository, raise a security or privacy issue, or reach the maintainers at Baz.
lead: Every channel below is public except the privacy and security ones. Pick the one that matches what you have.
---

## Something in the corpus is wrong

Open an [issue](https://github.com/baz-scm/awesome-reviewers/issues) with the instruction's slug or
URL and what it gets wrong. Instructions are distilled from review threads, so the useful correction
usually names the thread or the behaviour that contradicts it. If you would rather fix it directly,
the file lives at `_reviewers/<slug>.md` in
[baz-scm/awesome-reviewers](https://github.com/baz-scm/awesome-reviewers) and a pull request against
it is the fastest route — the site rebuilds from that file.

Wrong domain, topic or language on an entry is the same channel. Domain assignment is an explicit
repository-to-domain map in `build_data.py`, so a one-line pull request fixes it for every instruction
from that repository at once.

## Add a repository

Submit a public repository from the [homepage](/) form and it is queued for extraction, or open an
issue if you want to explain why it is a good source. Private repositories are handled through
[Baz](https://baz.co/agents) rather than here, because the corpus only publishes material derived
from public review discussions.

## Something about the API

The [developer portal](/developers/) covers the endpoints, the versioning and deprecation policy, the
quota and the error format, and the [API page](/api/) has the full endpoint table. If an endpoint
disagrees with its description in [/openapi.json](/openapi.json), that is a bug worth an issue — the
description is generated from the same script that writes the endpoints, so a mismatch means the
generator is wrong.

## Security

Report a vulnerability in the site or the build pipeline privately, through
[GitHub's security advisories](https://github.com/baz-scm/awesome-reviewers/security/advisories/new)
for this repository. Please do not open a public issue for it. There is no authentication, no user
data and no server-side code here, so the realistic surface is the static site, the GitHub Actions
workflow that builds it and the optional edge worker.

## Privacy

For anything about the analytics described on the [privacy](/privacy/) page — including a request to
access or delete data held about you — email <privacy@baz.co>, which is the privacy contact published
by Baz, the maintainer of this site. Say that the request concerns awesomereviewers.com so it reaches
the right place.

## The maintainers

The corpus is maintained by the team at [Baz](https://baz.co), based in Boston, Massachusetts, United
States. For commercial questions about Baz itself — as opposed to this corpus — use
[baz.co/contact](https://baz.co/contact). For anything about the corpus, GitHub is faster and the
answer stays public where the next person can read it.
