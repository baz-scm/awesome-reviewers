---
layout: page
title: Privacy
permalink: /privacy/
description: What this site collects, which third-party scripts run on it, what the API endpoints do not collect, and how to opt out.
lead: A static site with no accounts and no login. This page lists exactly what runs in the page, what leaves your browser, and what the endpoints do not see.
---

## What this site is, technically

Every page and endpoint here is a static file served over HTTPS from GitHub Pages. There is no
application server, no database, no session and no login, so there is nothing to sign up for and no
account data to hold. The corpus itself is derived from public code review discussions on GitHub and
contains no personal data beyond the public handles of the reviewers whose comments an instruction
was distilled from, which are credited on the [sources](/sources/) page.

## What the API endpoints collect

Nothing. `/raw/**`, `/v1/**`, `/llms.txt`, `/openapi.json`, `/agents.md` and the rest are plain
files: no key, no `Authorization` header, no cookie, no query parameter that identifies you, and no
request body. Requests do appear in the hosting provider's own server logs, which GitHub operates
under [its privacy statement](https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement).
Fetching an endpoint with `curl` or from an agent runs none of the scripts described below, because
those load only in the HTML pages.

## Scripts that run in the HTML pages

Three third parties are involved when you browse the site in a browser:

- **Google Analytics 4** (`googletagmanager.com`, measurement ID `G-2S2LLCMG7N`) — page views,
  referrers, approximate location derived from IP, device and browser. It sets its own cookies.
- **ZoomInfo WebSights** (`js.zi-scripts.com`) — a visitor-identification script that Baz, the
  maintainer of this site, uses for business analytics: it records the visit and attempts to infer
  the organisation it came from, from network-level information.
- **GitHub avatars** (`github.com`) — instruction pages load reviewer avatar images directly from
  GitHub, so GitHub sees the request for those images.

Blocking third-party scripts and cookies, or sending Do Not Track, removes the first two and does not
affect anything on the site: search, filtering, copying an instruction and every endpoint work with
JavaScript restricted or off.

## Data you send deliberately

The **add a repository** form on the homepage sends the repository URL you typed to
`awesome.baz.co`, a Baz service, so the repository can be queued for extraction. Nothing else in the
form is collected, and the field is meant for a public repository URL — do not put anything
confidential in it. Opening an issue or a pull request instead sends your data to GitHub under
GitHub's own privacy statement, not to this site.

## What is never collected

No accounts, no passwords, no payment details, no email address unless you email one to us, no
tracking of what you copy or which instruction you read at an individual level, and no advertising
profiles sold or shared. The site sets no cookies of its own; the only cookies come from the
analytics scripts above.

## Retention, access and deletion

Analytics data is retained for as long as the respective provider's configured retention allows, and
it is not joined to any account here because there are no accounts. To ask what is held about you, or
to have it deleted, email <privacy@baz.co> — the privacy contact published by Baz — and say the
request concerns awesomereviewers.com. Requests about data held by GitHub (server logs, your issues
and pull requests) go to GitHub.

## Changes

This page describes the site as it is currently deployed. Because the site is built from a public
repository, any change to the scripts listed above is visible in
[its commit history](https://github.com/baz-scm/awesome-reviewers/commits/main), and this page is
updated in the same commit that changes them. Questions about anything on it belong on
[contact](/contact/).
