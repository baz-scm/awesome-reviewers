"""Pillar 6c — the machine-enforced tier.

Most of the corpus cannot be automated. "Name things for what they do" is real
expertise and no checker will ever decide it. So the harness runs two tiers, and
this module is the small one: checks whose rule a deterministic analysis can decide,
each bound to the corpus instruction it enforces.

Every check declares the slug it came from, and `policy build` refuses to compile a
check whose slug does not resolve to a real instruction file. That binding is the
point — a rule you can trace to the review discussion that produced it is a rule a
team will accept, and a rule nobody can trace is a lint nobody will keep.

Python is analysed with `ast`, not regexes. `subprocess.run(cmd, shell=True)` split
over four lines, a `requests.get` whose `timeout=` sits in a dict splat, a mutable
default on a decorated async method — a regex gets all three wrong, in both
directions. YAML, Dockerfiles and requirements files are matched textually, because
parsing them would mean a dependency.

Findings are scoped to added lines. A gate that reported the whole file would blame
every change for the state of the repository, and would be switched off in a week.

Derived from the corpus:
  aidlc-workflows-check-mode-must-mirror — a check must decide exactly what the
      rule says, or it teaches people that the gate is noise.
  aidlc-workflows-secure-scope-and-input-validation — validate at the boundary.
  aidlc-workflows-fail-loudly-degrade-safely — a file that cannot be parsed is
      reported as unexamined, never silently treated as clean.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

from ..scrub import HIGH_CONFIDENCE, find as find_secrets
from .findings import ERROR, INFO, WARNING, Finding, SUPPRESSION_RE, make_finding

# Engines: how a check consumes a file.
PYTHON = "python"  # ast walk, findings intersected with added lines
TEXT = "text"  # per added line
FILE = "file"  # whole changed file


@dataclass(frozen=True)
class Check:
    id: str
    slug: str
    summary: str
    severity: str
    selector: tuple[str, ...]
    engine: str

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "slug": self.slug,
            "summary": self.summary,
            "severity": self.severity,
            "selector": list(self.selector),
            "engine": self.engine,
        }


# --------------------------------------------------------------------------- #
# Glob matching
# --------------------------------------------------------------------------- #

def _glob_to_regex(pattern: str) -> re.Pattern[str]:
    """Translate a path glob supporting `**`.

    `fnmatch` treats `*` as matching separators, so `*.py` would match
    `vendor/a.py`, and `Path.match` does not implement `**` recursion. Neither is
    close enough for a selector that decides whether a rule applies.
    """
    out = ["^"]
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if pattern.startswith("**/", index):
            out.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("**", index):
            out.append(".*")
            index += 2
        elif char == "*":
            out.append("[^/]*")
            index += 1
        elif char == "?":
            out.append("[^/]")
            index += 1
        elif char == "{":
            end = pattern.find("}", index)
            if end == -1:
                out.append(re.escape(char))
                index += 1
            else:
                alternatives = pattern[index + 1 : end].split(",")
                out.append("(?:" + "|".join(re.escape(a) for a in alternatives) + ")")
                index = end + 1
        else:
            out.append(re.escape(char))
            index += 1
    out.append("$")
    return re.compile("".join(out))


_GLOB_CACHE: dict[str, re.Pattern[str]] = {}


def matches_selector(path: str, selectors: Iterable[str]) -> bool:
    for pattern in selectors:
        compiled = _GLOB_CACHE.get(pattern)
        if compiled is None:
            compiled = _GLOB_CACHE[pattern] = _glob_to_regex(pattern)
        if compiled.match(path):
            return True
    return False


# --------------------------------------------------------------------------- #
# Context
# --------------------------------------------------------------------------- #

# Files above this are not analysed: a 5MB generated bundle produces no useful
# finding and a great deal of wasted hashing.
MAX_FILE_BYTES = 1 << 20

_BINARY_SUFFIXES = frozenset(
    {
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz", ".tar",
        ".whl", ".so", ".dylib", ".dll", ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".pyc",
    }
)


@dataclass
class Context:
    """One evaluation's view of the change under gate."""

    root: Path
    files: tuple[str, ...]
    added: dict[str, list[tuple[int, str]]]
    notes: list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.notes is None:
            self.notes = []
        self._text: dict[str, str | None] = {}
        self._trees: dict[str, ast.Module | None] = {}

    def added_lines(self, path: str) -> list[tuple[int, str]]:
        return self.added.get(path, [])

    def added_line_numbers(self, path: str) -> set[int]:
        return {number for number, _ in self.added.get(path, [])}

    def read(self, path: str) -> str | None:
        """File contents, or None when unreadable. Cached, and reported once."""
        if path in self._text:
            return self._text[path]
        target = self.root / path
        text: str | None = None
        try:
            if target.is_file() and Path(path).suffix.lower() not in _BINARY_SUFFIXES:
                if target.stat().st_size <= MAX_FILE_BYTES:
                    text = target.read_text(encoding="utf-8", errors="strict")
                else:
                    self.notes.append(f"{path}: skipped, larger than {MAX_FILE_BYTES // 1024} KiB")
        except (OSError, UnicodeDecodeError) as exc:
            self.notes.append(f"{path}: not examined ({type(exc).__name__})")
        self._text[path] = text
        return text

    def tree(self, path: str) -> ast.Module | None:
        """Parsed Python module, or None. A syntax error is a recorded note.

        Not a finding: a file that does not parse may be a template or a fixture,
        and inventing a policy violation for it would be a check deciding something
        it was not given a rule for. But it is never silently clean either.
        """
        if path in self._trees:
            return self._trees[path]
        source = self.read(path)
        tree: ast.Module | None = None
        if source is not None:
            try:
                tree = ast.parse(source, filename=path)
            except (SyntaxError, ValueError) as exc:
                self.notes.append(f"{path}: not analysed, does not parse as Python ({exc})")
        self._trees[path] = tree
        return tree

    def suppression(self, path: str, line: int, check_id: str) -> str:
        """Reason string when the check is suppressed at this line, else empty.

        Looks at the offending line and the one above it, which is where a reader
        would naturally put the comment. A suppression without a reason does not
        count: the regex requires one.
        """
        source = self.read(path)
        if not source:
            return ""
        lines = source.splitlines()
        for candidate in (line, line - 1):
            if 1 <= candidate <= len(lines):
                match = SUPPRESSION_RE.search(lines[candidate - 1])
                if match and check_id in {i.strip() for i in match.group("ids").split(",")}:
                    reason = (match.group("reason") or "").strip()
                    if reason:
                        return f"inline: {reason}"
        return ""


# --------------------------------------------------------------------------- #
# The registry
# --------------------------------------------------------------------------- #

CHECKS: dict[str, Check] = {}


def register(check: Check) -> Check:
    if check.id in CHECKS:
        raise ValueError(f"duplicate check id {check.id}")
    CHECKS[check.id] = check
    return check


PY = ("**/*.py",)
WORKFLOWS = (".github/workflows/*.yml", ".github/workflows/*.yaml")
ANY_TEXT = ("**",)

register(Check(
    id="AH001",
    slug="checkov-avoid-hardcoded-secrets",
    summary="No credential literals in source. Read secrets from the environment or a secret manager.",
    severity=ERROR,
    selector=ANY_TEXT,
    engine=TEXT,
))
register(Check(
    id="AH002",
    slug="angular-pin-github-actions-sha",
    summary="Pin third-party GitHub Actions to a full commit SHA; a tag or branch is a mutable pointer.",
    severity=WARNING,
    selector=WORKFLOWS,
    engine=TEXT,
))
register(Check(
    id="AH003",
    slug="grafana-workflow-permission-boundaries",
    summary="Declare least-privilege `permissions:` in every workflow; never `write-all`.",
    severity=WARNING,
    selector=WORKFLOWS,
    engine=FILE,
))
register(Check(
    id="AH004",
    slug="codex-prevent-command-injection",
    summary="Never run a composed string through a shell. Pass argv.",
    severity=ERROR,
    selector=PY,
    engine=PYTHON,
))
register(Check(
    id="AH005",
    slug="aidlc-workflows-secure-path-confinement",
    summary="Confine paths with Path.is_relative_to, not a string prefix check.",
    severity=ERROR,
    selector=PY,
    engine=PYTHON,
))
register(Check(
    id="AH006",
    slug="comfyui-prevent-path-traversal",
    summary="Validate archive members before extraction; extractall writes anywhere its names point.",
    severity=ERROR,
    selector=PY,
    engine=PYTHON,
))
register(Check(
    id="AH007",
    slug="airflow-handle-exceptions-with-specificity",
    summary="Catch the exceptions you can handle; never swallow everything silently.",
    severity=WARNING,
    selector=PY,
    engine=PYTHON,
))
register(Check(
    id="AH008",
    slug="waveterm-use-network-timeouts",
    summary="Every network call needs an explicit timeout, or it hangs forever by default.",
    severity=WARNING,
    selector=PY,
    engine=PYTHON,
))
register(Check(
    id="AH009",
    slug="cline-set-evidence-based-timeouts",
    summary="Bound subprocess calls with a timeout so a wedged child cannot hang the run.",
    severity=WARNING,
    selector=PY,
    engine=PYTHON,
))
register(Check(
    id="AH010",
    slug="cli-validate-environment-variables-early",
    summary="Validate environment variables at startup rather than failing with a KeyError deep in a call.",
    severity=INFO,
    selector=PY,
    engine=PYTHON,
))
register(Check(
    id="AH011",
    slug="azure-sentinel-avoid-logging-sensitive-data",
    summary="Do not log values held in secret-named variables.",
    severity=WARNING,
    selector=PY,
    engine=PYTHON,
))
register(Check(
    id="AH012",
    slug="ant-design-pin-ci-dependencies-securely",
    summary="Pin dependency versions exactly so a build is a function of its lockfile.",
    severity=WARNING,
    selector=("**/requirements*.txt", "**/requirements/*.txt", "**/constraints*.txt"),
    engine=TEXT,
))
register(Check(
    id="AH013",
    slug="compose-avoid-mutable-defaults",
    summary="A mutable default argument is shared across every call.",
    severity=WARNING,
    selector=PY,
    engine=PYTHON,
))
register(Check(
    id="AH014",
    slug="airflow-use-guards-over-assertions",
    summary="Use an explicit guard and a raised error, not assert — assertions vanish under -O.",
    severity=INFO,
    selector=PY,
    engine=PYTHON,
))
register(Check(
    id="AH015",
    slug="comfyui-container-security-best-practices",
    summary="Containers must declare a non-root USER.",
    severity=WARNING,
    selector=("**/Dockerfile", "**/Dockerfile.*", "**/*.dockerfile"),
    engine=FILE,
))
register(Check(
    id="AH016",
    slug="lobe-chat-pin-docker-base-versions",
    summary="Pin base images to a digest or an exact version, never `latest`.",
    severity=WARNING,
    selector=("**/Dockerfile", "**/Dockerfile.*", "**/*.dockerfile"),
    engine=TEXT,
))


# --------------------------------------------------------------------------- #
# Python analysis
# --------------------------------------------------------------------------- #

# Narrow on purpose. `base` and `prefix` were tried and removed: `s.startswith(prefix)`
# on an ordinary string is a legitimate operation, and flagging it made the check
# noisy. `base_dir` still matches, via `dir`.
_PATHISH = re.compile(r"path|dir|root|file|folder|cwd", re.IGNORECASE)

# Calls that consume a value without disclosing it, so a secret passed through one is
# not being logged. `repr` and `str` are deliberately absent — both print the value.
_NON_DISCLOSING = frozenset({"len", "bool", "type", "id", "hash", "isinstance", "any", "all", "sorted"})
_REDACTING = re.compile(r"redact|scrub|mask|sanitiz|fingerprint|digest|hashed|short|obfuscat", re.IGNORECASE)
_SECRET_IDENT = re.compile(
    r"pass(?:word|wd)?|secret|token|api[_-]?key|access[_-]?key|private[_-]?key|"
    r"client[_-]?secret|credential|auth",
    re.IGNORECASE,
)
_LOG_METHODS = frozenset({"debug", "info", "warning", "warn", "error", "critical", "exception", "log"})
_SUBPROCESS_CALLS = frozenset({"run", "call", "check_call", "check_output", "Popen"})
_HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete", "head", "options", "request"})

# Receivers that are unambiguously HTTP clients. `client`, `s` and `sess` are
# deliberately absent: `s.get("name")` on a dict is far more common than an HTTP call,
# and a check that fires on it is a check that gets switched off. Anything outside
# this set needs a URL-shaped first argument to qualify (see `_is_url_like`).
_HTTP_RECEIVERS = frozenset({"requests", "httpx", "aiohttp", "urllib3"})
_URLISH = re.compile(r"url|uri|endpoint|href|address", re.IGNORECASE)


def _root_name(node: ast.AST) -> str:
    """Leftmost identifier of a dotted expression: `a.b.c(...)` -> `a`."""
    while isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else ""


def _has_keyword(call: ast.Call, name: str) -> bool:
    """True when the keyword is passed, including via `**kwargs`.

    The `**` case is deliberately treated as "passed". A call that splats a dict is
    one this check cannot reason about, and guessing "missing" there would produce
    exactly the false positive that gets a gate disabled.
    """
    for keyword in call.keywords:
        if keyword.arg == name:
            return True
        if keyword.arg is None:
            return True
    return False


def _is_true(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is True


def _expression_name(node: ast.AST | None) -> str:
    """Best identifier for an expression: `a.b_dir` -> `b_dir`, `p` -> `p`."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _is_pathish(node: ast.AST | None) -> bool:
    """Is this expression a path, judged by name?

    Sees through `str(...)` and `os.fspath(...)`, which is how a Path reaches a string
    comparison in the first place — and how the antipattern this check exists for
    usually looks: `str(candidate).startswith(str(base_dir))`.
    """
    if node is None:
        return False
    if isinstance(node, ast.Call):
        callee = _expression_name(node.func) or _root_name(node.func)
        if callee in ("str", "fspath", "abspath", "realpath", "normpath") and node.args:
            return _is_pathish(node.args[0])
        return False
    name = _expression_name(node)
    return bool(name and _PATHISH.search(name))


def _is_url_like(node: ast.AST | None) -> bool:
    """Does this argument look like a URL?

    The disambiguator for `x.get(...)`: a call whose first argument is a URL is an
    HTTP call whatever the receiver is called, and one whose first argument is a
    dictionary key is not.
    """
    if node is None:
        return False
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.startswith(("http://", "https://", "ws://", "wss://", "//"))
    if isinstance(node, ast.Name):
        return bool(_URLISH.search(node.id))
    if isinstance(node, ast.Attribute):
        return bool(_URLISH.search(node.attr))
    if isinstance(node, ast.JoinedStr):
        head = next((p for p in node.values if isinstance(p, ast.Constant)), None)
        return bool(head and str(head.value).startswith(("http://", "https://")))
    if isinstance(node, ast.BinOp):
        return _is_url_like(node.left)
    return False


def _is_composed(node: ast.AST) -> bool:
    """Does this expression build a string at runtime?"""
    if isinstance(node, ast.JoinedStr):
        return True
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Mod)):
        return True
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        return node.func.attr in ("format", "join")
    return False


class _Raw:
    __slots__ = ("check", "line", "message", "evidence")

    def __init__(self, check: str, line: int, message: str, evidence: str = "") -> None:
        self.check = check
        self.line = line
        self.message = message
        self.evidence = evidence


class PythonAnalyzer(ast.NodeVisitor):
    """One walk per file, collecting every Python finding the pack might want."""

    def __init__(self, path: str, source: str, *, is_test: bool) -> None:
        self.path = path
        self.lines = source.splitlines()
        self.is_test = is_test
        self.out: list[_Raw] = []

    def line_text(self, line: int) -> str:
        return self.lines[line - 1] if 1 <= line <= len(self.lines) else ""

    def emit(self, check: str, node: ast.AST, message: str) -> None:
        line = getattr(node, "lineno", 1)
        self.out.append(_Raw(check, line, message, self.line_text(line)))

    # ---- calls ----------------------------------------------------------- #

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802 - ast API
        func = node.func
        attr = func.attr if isinstance(func, ast.Attribute) else (func.id if isinstance(func, ast.Name) else "")
        root = _root_name(func)

        # AH004 — a shell plus a composed string is command injection.
        if attr == "system" and root == "os":
            self.emit("AH004", node, "os.system runs its argument through a shell; use subprocess with an argv list")
        elif attr in _SUBPROCESS_CALLS and any(_is_true(k.value) for k in node.keywords if k.arg == "shell"):
            composed = any(_is_composed(arg) for arg in node.args)
            self.emit(
                "AH004",
                node,
                (
                    "shell=True with a runtime-composed command string is command injection; "
                    "pass an argv list instead"
                    if composed
                    else "shell=True invokes a shell; pass an argv list so arguments are not re-parsed"
                ),
            )

        # AH005 — string prefix checks do not confine paths.
        #
        # The rule is about *path* containment, so the check has to establish that a
        # path is what is being compared. Three independent signals, any of which is
        # enough, and none of which fires on `str(x).startswith("https://")`:
        #   the receiver is named like a path            base_dir.startswith(...)
        #   the receiver is str() around a path-named    str(run_folder).startswith(...)
        #   the *prefix* is a path                       str(p).startswith(str(base_dir))
        #   the prefix is an absolute path literal       p.startswith("/srv/")
        if attr == "startswith":
            receiver = func.value if isinstance(func, ast.Attribute) else None
            name = _expression_name(receiver)
            wrapped_path = _is_pathish(receiver)
            first = node.args[0] if node.args else None
            prefix_is_path = _is_pathish(first)
            # A bare "/" is an absoluteness test, which is a different and legitimate
            # operation. Only a prefix naming an actual directory is containment.
            absolute_prefix = (
                isinstance(first, ast.Constant)
                and isinstance(first.value, str)
                and len(first.value) > 1
                and first.value.startswith("/")
                and not first.value.startswith("//")
            )
            if wrapped_path or prefix_is_path or absolute_prefix or (name and _PATHISH.search(name)):
                self.emit(
                    "AH005",
                    node,
                    "prefix check on a path: '/run' is a prefix of '/runner' and '..' survives it — "
                    "use Path.is_relative_to on resolved paths",
                )

        # AH006 — extractall writes wherever its member names point.
        if attr == "extractall" and not (_has_keyword(node, "filter") or _has_keyword(node, "members")):
            self.emit(
                "AH006",
                node,
                "extractall without filter= or validated members can write outside the destination",
            )

        # AH008 / AH009 — unbounded waits.
        if attr in ("urlopen", "urlretrieve") and not _has_keyword(node, "timeout"):
            self.emit("AH008", node, f"{attr} without timeout= blocks indefinitely")
        elif attr in _HTTP_METHODS and not _has_keyword(node, "timeout"):
            first = node.args[0] if node.args else None
            if root.lower() in _HTTP_RECEIVERS or _is_url_like(first):
                self.emit("AH008", node, f"{root}.{attr} without timeout= blocks indefinitely by default")
        if attr in _SUBPROCESS_CALLS - {"Popen"} and root == "subprocess" and not _has_keyword(node, "timeout"):
            self.emit("AH009", node, f"subprocess.{attr} without timeout= can hang the whole run")
        if attr in ("communicate", "wait") and not _has_keyword(node, "timeout"):
            if isinstance(func, ast.Attribute) and _PROC_HINT.search(_root_name(func) or ""):
                self.emit("AH009", node, f".{attr}() without timeout= can hang the whole run")

        # AH011 — logging a secret-named value.
        if attr in _LOG_METHODS or attr == "print" or (isinstance(func, ast.Name) and func.id == "print"):
            for argument in [*node.args, *(k.value for k in node.keywords)]:
                leaked = _secret_identifier(argument)
                if leaked:
                    self.emit("AH011", node, f"{leaked!r} looks like a secret and is being written to output")
                    break

        self.generic_visit(node)

    # ---- subscripts ------------------------------------------------------ #

    def visit_Subscript(self, node: ast.Subscript) -> None:  # noqa: N802
        value = node.value
        # Two narrowings, both from the rule rather than from convenience:
        #   Load only — `os.environ["TZ"] = "UTC"` sets a variable, it does not depend
        #   on one, so there is nothing to validate at startup.
        #   Constant key only — `os.environ[name]` is a dynamic lookup that is almost
        #   always already guarded (`if name in os.environ`), whereas
        #   `os.environ["API_KEY"]` is the hardcoded required-variable read the
        #   instruction is about.
        if (
            isinstance(value, ast.Attribute)
            and value.attr == "environ"
            and _root_name(value) == "os"
            and isinstance(node.ctx, ast.Load)
            and isinstance(node.slice, ast.Constant)
        ):
            self.emit(
                "AH010",
                node,
                f"os.environ[{node.slice.value!r}] raises KeyError at the point of use; "
                f"validate required variables at startup",
            )
        self.generic_visit(node)

    # ---- handlers -------------------------------------------------------- #

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:  # noqa: N802
        swallowed = len(node.body) == 1 and isinstance(node.body[0], (ast.Pass, ast.Continue))
        if node.type is None:
            self.emit(
                "AH007",
                node,
                "a bare except also catches KeyboardInterrupt and SystemExit; name the exceptions you handle",
            )
        elif isinstance(node.type, ast.Name) and node.type.id in ("Exception", "BaseException") and swallowed:
            self.emit(
                "AH007",
                node,
                f"except {node.type.id} with a silent {type(node.body[0]).__name__.lower()} hides every failure",
            )
        self.generic_visit(node)

    # ---- definitions ----------------------------------------------------- #

    def _check_defaults(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        defaults = [*node.args.defaults, *[d for d in node.args.kw_defaults if d is not None]]
        for default in defaults:
            mutable = isinstance(default, (ast.List, ast.Dict, ast.Set)) or (
                isinstance(default, ast.Call)
                and isinstance(default.func, ast.Name)
                and default.func.id in ("list", "dict", "set")
                and not default.args
            )
            if mutable:
                self.emit(
                    "AH013",
                    node,
                    f"{node.name}() has a mutable default argument, which is created once and shared "
                    f"by every call; default to None and build inside",
                )
                break

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        self._check_defaults(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
        self._check_defaults(node)
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:  # noqa: N802
        if not self.is_test:
            self.emit(
                "AH014",
                node,
                "assert is removed by python -O; raise an explicit error for a runtime guard",
            )
        self.generic_visit(node)


_PROC_HINT = re.compile(r"proc|process|child|popen", re.IGNORECASE)


def _secret_identifier(node: ast.AST) -> str:
    """Name of a secret-looking identifier whose *value* would be disclosed.

    Two narrowings, both needed to keep this quiet on correct code:

      identifiers only, never string literals — `log.info("password reset sent")` is a
      perfectly good log line, and flagging it is how a check earns a reputation for
      crying wolf

      do not descend into a call that consumes the value without printing it —
      `log.info("key of %d chars", len(api_key))` discloses a length, and
      `log.info(redact(token))` discloses nothing. Walking blindly would flag both.
    """
    stack: list[ast.AST] = [node]
    while stack:
        current = stack.pop()
        if isinstance(current, ast.Call):
            callee = _expression_name(current.func) or _root_name(current.func)
            if callee in _NON_DISCLOSING or _REDACTING.search(callee or ""):
                continue  # the value is consumed here, not emitted
        if isinstance(current, ast.Name) and _SECRET_IDENT.search(current.id):
            return current.id
        if isinstance(current, ast.Attribute) and _SECRET_IDENT.search(current.attr):
            return current.attr
        stack.extend(ast.iter_child_nodes(current))
    return ""


def _is_test_path(path: str) -> bool:
    parts = Path(path).parts
    name = Path(path).name
    return (
        "tests" in parts
        or "test" in parts
        or name.startswith("test_")
        or name.endswith("_test.py")
        or "conftest" in name
    )


def run_python(ctx: Context, checks: dict[str, Check]) -> Iterator[tuple[Check, _Raw, str]]:
    ids = {check.id for check in checks.values() if check.engine == PYTHON}
    if not ids:
        return
    for path in ctx.files:
        if not path.endswith(".py"):
            continue
        applicable = [c for c in checks.values() if c.engine == PYTHON and matches_selector(path, c.selector)]
        if not applicable:
            continue
        tree = ctx.tree(path)
        source = ctx.read(path)
        if tree is None or source is None:
            continue
        analyzer = PythonAnalyzer(path, source, is_test=_is_test_path(path))
        analyzer.visit(tree)
        added = ctx.added_line_numbers(path)
        by_id = {c.id: c for c in applicable}
        for raw in analyzer.out:
            check = by_id.get(raw.check)
            if check is None or raw.line not in added:
                continue
            yield check, raw, path


# --------------------------------------------------------------------------- #
# Text analysis
# --------------------------------------------------------------------------- #

_USES_RE = re.compile(r"^\s*(?:-\s+)?uses:\s*['\"]?(?P<action>[^'\"\s#]+)")
_SHA_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
_MUTABLE_REFS = frozenset({"main", "master", "head", "latest", "develop", "trunk"})
_FROM_RE = re.compile(r"^\s*FROM\s+(?P<image>\S+)", re.IGNORECASE)
_REQ_PIN_RE = re.compile(r"(==|===|@\s*git\+|@[0-9a-f]{40})")
_REQ_SKIP_RE = re.compile(r"^\s*(?:#|-r|--|-e|\.|/)")


def _check_secret_line(check: Check, path: str, line: int, text: str) -> Finding | None:
    hits = find_secrets(text, HIGH_CONFIDENCE)
    if not hits:
        return None
    return make_finding(
        check=check.id,
        slug=check.slug,
        severity=check.severity,
        path=path,
        line=line,
        message=f"{hits[0].label} literal in source — read it from the environment or a secret manager",
        # Deliberately not the line: `make_finding` scrubs, but the label alone is
        # already enough for a person to find it, and the value must not travel.
        evidence=f"<{hits[0].label} redacted>",
        title=check.summary,
    )


def _check_action_pin(check: Check, path: str, line: int, text: str) -> Finding | None:
    match = _USES_RE.match(text)
    if not match:
        return None
    action = match.group("action")
    if action.startswith(("./", "docker://")):
        return None  # local composite action or an image reference, not a mutable tag
    if "@" not in action:
        return make_finding(
            check=check.id, slug=check.slug, severity=ERROR, path=path, line=line,
            message=f"action {action!r} has no ref at all",
            evidence=text, title=check.summary,
        )
    name, ref = action.rsplit("@", 1)
    if _SHA_RE.match(ref):
        return None
    mutable = ref.lower() in _MUTABLE_REFS
    return make_finding(
        check=check.id,
        slug=check.slug,
        # A branch is rewritten under you; a tag can be moved but usually is not.
        severity=ERROR if mutable else check.severity,
        path=path,
        line=line,
        message=(
            f"{name} is pinned to the mutable ref {ref!r} — anyone who can push that branch "
            f"runs code in your workflow"
            if mutable
            else f"{name} is pinned to tag {ref!r}; pin to a full commit SHA (a tag can be moved)"
        ),
        evidence=text,
        title=check.summary,
    )


def _check_base_image(check: Check, path: str, line: int, text: str) -> Finding | None:
    match = _FROM_RE.match(text)
    if not match:
        return None
    image = match.group("image")
    if image.startswith("$") or "@sha256:" in image:
        return None
    tag = image.rsplit(":", 1)[1] if ":" in image.rsplit("/", 1)[-1] else ""
    if not tag or tag == "latest":
        return make_finding(
            check=check.id, slug=check.slug, severity=check.severity, path=path, line=line,
            message=f"base image {image!r} is unpinned; use an exact version or @sha256 digest",
            evidence=text, title=check.summary,
        )
    return None


def _check_requirement_pin(check: Check, path: str, line: int, text: str) -> Finding | None:
    stripped = text.strip()
    if not stripped or _REQ_SKIP_RE.match(stripped) or _REQ_PIN_RE.search(stripped):
        return None
    return make_finding(
        check=check.id, slug=check.slug, severity=check.severity, path=path, line=line,
        message=f"{stripped.split(';')[0].strip()!r} is not pinned to an exact version",
        evidence=text, title=check.summary,
    )


_TEXT_CHECKS: dict[str, Callable[[Check, str, int, str], Finding | None]] = {
    "AH001": _check_secret_line,
    "AH002": _check_action_pin,
    "AH012": _check_requirement_pin,
    "AH016": _check_base_image,
}


def run_text(ctx: Context, checks: dict[str, Check]) -> Iterator[Finding]:
    for path in ctx.files:
        applicable = [
            c
            for c in checks.values()
            if c.engine == TEXT and c.id in _TEXT_CHECKS and matches_selector(path, c.selector)
        ]
        if not applicable:
            continue
        if Path(path).suffix.lower() in _BINARY_SUFFIXES:
            continue
        for line, text in ctx.added_lines(path):
            for check in applicable:
                finding = _TEXT_CHECKS[check.id](check, path, line, text)
                if finding is not None:
                    yield finding


# --------------------------------------------------------------------------- #
# Whole-file analysis
# --------------------------------------------------------------------------- #

def _check_workflow_permissions(check: Check, ctx: Context, path: str) -> list[Finding]:
    source = ctx.read(path)
    if source is None:
        return []
    findings: list[Finding] = []
    lines = source.splitlines()
    top_level = False
    for number, text in enumerate(lines, start=1):
        if re.match(r"^permissions:", text):
            top_level = True
            if "write-all" in text:
                findings.append(make_finding(
                    check=check.id, slug=check.slug, severity=ERROR, path=path, line=number,
                    message="permissions: write-all grants the workflow token every scope",
                    evidence=text, title=check.summary,
                ))
        elif re.match(r"^\s+permissions:\s*write-all", text):
            findings.append(make_finding(
                check=check.id, slug=check.slug, severity=ERROR, path=path, line=number,
                message="permissions: write-all grants the job token every scope",
                evidence=text, title=check.summary,
            ))
    if not top_level:
        findings.append(make_finding(
            check=check.id, slug=check.slug, severity=check.severity, path=path, line=1,
            message="workflow declares no top-level permissions:, so it inherits the repository default",
            evidence="", title=check.summary,
        ))
    return findings


def _check_dockerfile_user(check: Check, ctx: Context, path: str) -> list[Finding]:
    source = ctx.read(path)
    if source is None:
        return []
    for text in source.splitlines():
        if re.match(r"^\s*USER\s+\S+", text, re.IGNORECASE):
            stated = text.split()[1]
            if stated.lower() in ("root", "0"):
                break
            return []
    return [make_finding(
        check=check.id, slug=check.slug, severity=check.severity, path=path, line=1,
        message="no non-root USER instruction; the container runs as root",
        evidence="", title=check.summary,
    )]


_FILE_CHECKS: dict[str, Callable[[Check, Context, str], list[Finding]]] = {
    "AH003": _check_workflow_permissions,
    "AH015": _check_dockerfile_user,
}


def run_file(ctx: Context, checks: dict[str, Check]) -> Iterator[Finding]:
    for path in ctx.files:
        for check in checks.values():
            if check.engine != FILE or check.id not in _FILE_CHECKS:
                continue
            if not matches_selector(path, check.selector):
                continue
            yield from _FILE_CHECKS[check.id](check, ctx, path)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def evaluate(ctx: Context, checks: dict[str, Check]) -> list[Finding]:
    """Run every enabled check and return findings, deduplicated by fingerprint."""
    collected: list[Finding] = []
    for check, raw, path in run_python(ctx, checks):
        collected.append(make_finding(
            check=check.id, slug=check.slug, severity=check.severity, path=path,
            line=raw.line, message=raw.message, evidence=raw.evidence, title=check.summary,
        ))
    collected.extend(run_text(ctx, checks))
    collected.extend(run_file(ctx, checks))

    seen: set[str] = set()
    unique: list[Finding] = []
    for finding in sorted(collected, key=lambda f: (f.path, f.line, f.check)):
        if finding.fingerprint in seen:
            continue
        seen.add(finding.fingerprint)
        unique.append(finding)
    return unique
