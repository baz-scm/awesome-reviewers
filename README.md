<div align="center">
   <img align="center" width="128px" src="https://avatars.githubusercontent.com/u/140384842?s=200&v=4" />
   <h1 align="center"><b>Awesome Reviewers ✨ </b></h1>
   <p align="center">
      A skills library of reusable prompts for AI-assisted code review.
      <br />
      <a href="https://awesomereviewers.com"><strong>AwesomeReviewers.com »</strong></a>
      <br />
   </p>
</div>

**Awesome Reviewers** is an open-source skills library of reusable prompts for agentic code review. Each skill is distilled from real code review feedback in leading open-source repositories, then packaged into copy-ready guidance you can apply in your AI workflows. You can browse, filter, and open any skill on the website, then use it in your editor, chat assistant, or automated review pipeline.

<div align="center">

🧠 **Skills-first UX** &nbsp;&nbsp;•&nbsp;&nbsp; 🔎 Search + filters &nbsp;&nbsp;•&nbsp;&nbsp; 🚀 Deployable review agents

</div>

## What the project is today

Awesome Reviewers is positioned as a **Skills Library**:

- **Skills-centric browsing:** The homepage is focused on discovering reusable review skills with search, language filters, and tag filters.
- **Practical guidance:** Every skill page provides copy-ready, actionable review instructions.
- **Source-backed prompts:** Skills are derived from recurring patterns in real maintainer feedback.
- **Automation-ready:** Selected skills can be deployed as reviewer agents through Baz.

## Core Features

- **🧩 Reusable review skills:** A large catalog of prompts covering quality, security, readability, testing, infrastructure, and more.
- **🔎 Fast discovery:** Search and filter by tag/language to find the right reviewer quickly.
- **📄 Skill detail pages:** Inspect the full guidance, associated metadata, and shareable links.
- **🚀 One-click Baz deployment:** Launch skills as PR review agents via **Deploy to baz**.
- **🏢 Organizations explorer:** Explore contributor and repository activity by organization.
- **🧠 Methodology transparency:** Learn how patterns are extracted and turned into practical review guidance.

## Getting Started

1. **Browse skills** at [awesomereviewers.com](https://awesomereviewers.com).
2. **Open a skill** and copy its guidance.
3. **Apply it in your AI workflow** as a system/agent instruction in tools like VS Code, Cursor, ChatGPT, or Claude.
4. **Iterate on feedback** and combine skills as needed.
5. **(Optional) Deploy with Baz** to run the skill automatically on pull requests.

No installation is required for website usage. You can also inspect prompt sources directly in this repository under `_reviewers/`.

## Deprecated: Export Reviewers to Claude Skills CLI

The `tools/awesome2claude.py` exporter has been **deprecated** and is no longer supported.

- The command is intentionally disabled and will exit with a deprecation message.
- Please consume skills directly from this repository (`_reviewers/`) and the website instead.

## Acknowledgments

This project is maintained by the team at [**Baz**](https://baz.co) as part of a mission to make agentic code reviews more accessible. The prompt library is inspired by patterns found in open-source review conversations across many repositories.

## Disclaimer

Awesome Reviewers is community-contributed. While we aim for high quality, we cannot guarantee complete accuracy, completeness, or security for every prompt. Prompts are inspired by repository maintainer feedback and are not official guidance from those projects. If you encounter suspicious or harmful content, please open an issue in this repository.
