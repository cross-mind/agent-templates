from __future__ import annotations

import hashlib
from collections.abc import Iterable
from pathlib import Path, PurePosixPath


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def posix_relpath(path: Path) -> str:
    return path.as_posix()


def matches_any(rel_posix: str, patterns: Iterable[str]) -> bool:
    p = PurePosixPath(rel_posix)
    for raw_pattern in patterns:
        pattern = str(raw_pattern)
        if "/" in pattern:
            if p.match(pattern):
                return True
        else:
            if p.match(f"**/{pattern}"):
                return True
    return False
