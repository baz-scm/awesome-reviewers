from .base import BaseWriter
from .cursor import CursorWriter
from .claude import ClaudeWriter
from .cline import ClineWriter
from .codex import CodexWriter
from .amp import AmpWriter
from .windsurf import WindsurfWriter
from .augment import AugmentWriter

writers = {
    'cursor': CursorWriter,
    'claude': ClaudeWriter,
    'windsurf': WindsurfWriter,
    'codex': CodexWriter,
    'cline': ClineWriter,
    'augment': AugmentWriter,
    'amp': AmpWriter,
}

__all__ = ['BaseWriter', 'CursorWriter', 'ClaudeWriter', 'ClineWriter',
           'CodexWriter', 'WindsurfWriter', 'AugmentWriter', 'AmpWriter', 'writers']
