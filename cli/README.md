# Awesome Reviewers CLI

This tool converts reviewer descriptions from the `_reviewers/` directory into various output formats for different LLM assistants.

## Installation

1. Install Python 3.8 or newer.
2. Install dependencies:
   ```bash
   pip install python-frontmatter
   ```

## Usage

Run the CLI from the repository root.

### Generate files for a single reviewer

```bash
python cli/cli.py add axios-complete-error-handling-chain --target cursor
```

### Export a reviewer for multiple targets

```bash
python cli/cli.py add axios-complete-error-handling-chain \
  --target cursor claude codex
```

### Batch process all reviewers with matching `tools` labels

```bash
python cli/cli.py add --all --target cursor claude --output-dir ./out
```

This command writes the converted prompts into the `./out` folder. Each writer
creates files in its own format:

- **cursor** → `.cursor/rules.json` (merged JSON)
- **claude**, **cline**, **amp** → one `.md` file per reviewer
- **codex** → `reviewers.ts` exporting a map of prompts
- **windsurf**, **augment** → JSON files listing prompts

### List reviewers

```bash
python cli/cli.py list --language TypeScript
```

Filters are available for `--language`, `--repo`, and `--category`.

### Add reviewers by language, repo, or category

```bash
python cli/cli.py add --target cursor --language TypeScript
```

### Tips

- Reviewers missing the `## System Prompt` section are skipped with a warning.
- When filtering or using `--all`, only reviewers containing the target name in
  their `tools` frontmatter field are included.

