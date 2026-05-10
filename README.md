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

## CLI: Export Reviewers to Claude Skills

This repository ships with a Python CLI (`tools/awesome2claude.py`) that converts prompts in `_reviewers/` into [Anthropic Claude Skills](https://github.com/anthropics/claude-skills) folders. The tool can clone/update the Awesome Reviewers repository, parse each prompt’s YAML front matter, and generate a Claude-compatible `SKILL.md` for every reviewer.

### Installation

```bash
pip install click pyyaml
```

### Usage

```bash
python tools/awesome2claude.py --output-dir ./claude_skills
```

Key options:

- `--overwrite` – replace any existing skill directories in the output folder.
- `--group-by-category` – nest skills under category subdirectories.
- `--single <filename>` – convert only a specific prompt (useful for testing).
- `--limit N` – process only the first *N* prompts (after sorting), handy for generating a sample set.
- `--dry-run` – preview the conversion without writing files.
- `--project-dir <path>` – scan a local project for package manager manifests and emit a combined skill that stitches together every Awesome Reviewer matching a detected dependency.
- `--combined-skill-slug`, `--combined-skill-title`, `--combined-skill-description` – customize directory name, title, and description for the combined skill.

Run `python tools/awesome2claude.py --help` for the full list of options.

### Skill-oriented export behavior

Generated `SKILL.md` files include a standardized wrapper to improve agent execution consistency:

- `When to apply`
- `Review checklist` (derived from bullets/numbered steps in the source prompt when available)
- `Expected output`
- `Source guidance` (the original reviewer text)

### Audit reviewer readiness for skill use

Use the audit helper to quantify how skill-ready the `_reviewers/` corpus is:

```bash
python tools/reviewer_skill_audit.py --write-report docs/reviewer-skill-readiness.md
```

### Generate a project-specific combined skill

When you supply `--project-dir`, the CLI walks the directory tree looking for popular package manager lockfiles (npm, pnpm, Yarn, Poetry, Pipenv, RubyGems, Cargo, Go modules, Composer, Pub, NuGet, etc.). Discovered dependencies are normalized and matched with the Awesome Reviewers catalog, then merged into a **single Claude skill**.

Example:

```bash
python tools/awesome2claude.py \
  --output-dir ./claude_skills \
  --overwrite \
  --project-dir ~/code/my-service
```

After the run, check `./claude_skills/project-dependencies/SKILL.md` (or your configured slug) for the generated combined skill.

## Acknowledgments

This project is maintained by the team at [**Baz**](https://baz.co) as part of a mission to make agentic code reviews more accessible. The prompt library is inspired by patterns found in open-source review conversations across many repositories.

## Disclaimer

Awesome Reviewers is community-contributed. While we aim for high quality, we cannot guarantee complete accuracy, completeness, or security for every prompt. Prompts are inspired by repository maintainer feedback and are not official guidance from those projects. If you encounter suspicious or harmful content, please open an issue in this repository.
