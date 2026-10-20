from __future__ import annotations

import dataclasses


ROW_STRUCTURE = "row_structure"
NAME = "name"
STREAM_FORMAT = "stream_format"
WEB_FORMAT = "web_format"
LOGO_FORMAT = "logo_format"
EPG_ID = "epg_id"
INFO_TAGS = "info_tags"
DUPLICATE_NAMES = "duplicate_names"
DUPLICATE_STREAM_URLS = "duplicate_stream_urls"
DUPLICATE_EPG_IDS = "duplicate_epg_ids"
STREAM_AVAILABILITY = "stream_availability"

CHECKS = (
    (ROW_STRUCTURE, "Table row structure", True),
    (NAME, "Channel/station name present", True),
    (STREAM_FORMAT, "Stream link format and type", True),
    (WEB_FORMAT, "Web link format", True),
    (LOGO_FORMAT, "Logo link format", True),
    (EPG_ID, "EPG ID presence", True),
    (INFO_TAGS, "Info tags format", True),
    (DUPLICATE_NAMES, "Duplicate names", True),
    (DUPLICATE_STREAM_URLS, "Duplicate stream URLs", True),
    (DUPLICATE_EPG_IDS, "Duplicate EPG IDs", True),
)

ENTRY_CHECKS = {NAME, STREAM_FORMAT, WEB_FORMAT, LOGO_FORMAT, EPG_ID, INFO_TAGS}
DUPLICATE_CHECKS = {DUPLICATE_NAMES, DUPLICATE_STREAM_URLS, DUPLICATE_EPG_IDS}


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
    check: str
    message: str

    def render(self, level: str = "error") -> str:
        return f"::{level} file={self.catalog},line={self.line}::{self.message}"
