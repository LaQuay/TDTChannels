from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Entry:
    catalog: str
    line: int
    section: str
    name: str
    stream: str
    web: str
    logo: str
    epg_id: str
    info: str


@dataclasses.dataclass(frozen=True)
class Problem:
    catalog: str
    line: int
    message: str

    def render(self, level: str = "error") -> str:
        return f"::{level} file={self.catalog},line={self.line}::{self.message}"
