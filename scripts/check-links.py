#!/usr/bin/env python3
"""Check local Markdown links and SUMMARY membership without dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
SUMMARY = SOURCE / "SUMMARY.md"
LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")


def local_target(source: Path, raw: str) -> Path | None:
    destination = raw.strip().split()[0].strip("<>")
    if not destination or destination.startswith(("#", "http://", "https://", "mailto:")):
        return None
    destination = unquote(destination.split("#", 1)[0])
    return (source.parent / destination).resolve()


def main() -> int:
    problems: list[str] = []
    pages = sorted(SOURCE.rglob("*.md"))
    summary_text = SUMMARY.read_text(encoding="utf-8")
    listed = {
        target
        for raw in LINK.findall(summary_text)
        if (target := local_target(SUMMARY, raw)) is not None
    }

    for page in pages:
        text = page.read_text(encoding="utf-8")
        for line, content in enumerate(text.splitlines(), 1):
            if content.endswith((" ", "\t")):
                problems.append(f"{page.relative_to(ROOT)}:{line}: trailing whitespace")
            for raw in LINK.findall(content):
                target = local_target(page, raw)
                if target is not None and not target.exists():
                    problems.append(
                        f"{page.relative_to(ROOT)}:{line}: missing link target {raw}"
                    )

    for page in pages:
        if page != SUMMARY and page.resolve() not in listed:
            problems.append(f"{page.relative_to(ROOT)}: not listed in SUMMARY.md")

    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"checked {len(pages) - 1} book pages and their local links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

