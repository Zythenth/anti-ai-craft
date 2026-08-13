from __future__ import annotations

from typing import Any, Protocol

from .evidence import Finding


class Rule(Protocol):
    id: str
    category: str
    description: str
    deterministic: bool

    def evaluate(self, context: Any) -> tuple[Finding, ...]: ...
