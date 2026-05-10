#!/usr/bin/env python3
"""Deprecated CLI stub for exporting Awesome Reviewers to Claude Skills."""

from __future__ import annotations

import click


DEPRECATION_MESSAGE = (
    "Deprecated: tools/awesome2claude.py has been retired and is no longer supported.\n"
    "Please use the Awesome Reviewers skills directly from _reviewers/ or awesomereviewers.com."
)


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None:
    """Emit a deprecation notice and exit."""
    click.echo(DEPRECATION_MESSAGE, err=True)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
