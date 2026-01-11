from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal

from .config import TemplateSyncConfig
from .managed_blocks import ManagedBlockError, replace_managed_block
from .util import matches_any, sha256_file


ChangeKind = Literal["create", "update", "skip", "error"]


@dataclass(frozen=True)
class Change:
    kind: ChangeKind
    target: str
    path: str
    detail: str = ""


def discover_targets(repo_root: Path, *, exclude: Iterable[str]) -> list[str]:
    exclude_set = {str(x) for x in exclude}
    targets: list[str] = []
    for child in repo_root.iterdir():
        if not child.is_dir():
            continue
        name = child.name
        if name.startswith("."):
            continue
        if name in exclude_set:
            continue
        if (child / "CLAUDE.md").exists():
            targets.append(name)
    return sorted(targets)


def iter_source_files(source_root: Path, pattern: str) -> Iterable[Path]:
    has_glob = any(ch in pattern for ch in ["*", "?", "["])
    if not has_glob:
        literal = source_root / pattern
        if literal.is_file():
            yield literal
        elif literal.is_dir():
            for nested in literal.rglob("*"):
                if nested.is_file():
                    yield nested
        return

    for path in source_root.glob(pattern):
        if path.is_file():
            yield path


def sync_file(
    *,
    src: Path,
    dst: Path,
    rel_posix: str,
    target_name: str,
    dry_run: bool,
) -> Change:
    if dst.exists():
        if dst.is_dir():
            return Change(kind="error", target=target_name, path=rel_posix, detail="destination is a directory")
        if sha256_file(src) == sha256_file(dst):
            return Change(kind="skip", target=target_name, path=rel_posix, detail="unchanged")
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        return Change(kind="update", target=target_name, path=rel_posix)

    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return Change(kind="create", target=target_name, path=rel_posix)


def sync_keep_updated(
    *,
    cfg: TemplateSyncConfig,
    repo_root: Path,
    target_name: str,
    dry_run: bool,
) -> list[Change]:
    source_root = cfg.source_dir
    target_root = repo_root / target_name

    changes: list[Change] = []
    for pattern in cfg.keep_updated:
        for src_file in iter_source_files(source_root, pattern):
            rel = src_file.relative_to(source_root).as_posix()
            if matches_any(rel, cfg.ignore_patterns):
                continue
            if matches_any(rel, cfg.never_update):
                changes.append(Change(kind="skip", target=target_name, path=rel, detail="never_update"))
                continue

            dst_file = target_root / rel
            changes.append(sync_file(src=src_file, dst=dst_file, rel_posix=rel, target_name=target_name, dry_run=dry_run))

    return changes


def sync_managed_blocks(
    *,
    cfg: TemplateSyncConfig,
    repo_root: Path,
    target_name: str,
    dry_run: bool,
    strict: bool,
) -> list[Change]:
    changes: list[Change] = []
    target_root = repo_root / target_name

    for rel in cfg.managed_files:
        if matches_any(rel, cfg.ignore_patterns):
            continue
        if matches_any(rel, cfg.never_update):
            changes.append(Change(kind="skip", target=target_name, path=rel, detail="never_update"))
            continue

        target_path = target_root / rel
        if not target_path.exists():
            changes.append(Change(kind="error", target=target_name, path=rel, detail="missing file"))
            continue

        try:
            text = target_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            changes.append(Change(kind="error", target=target_name, path=rel, detail=f"utf-8 decode failed: {e}"))
            continue

        changed_blocks: list[str] = []
        updated_text = text
        file_error: str | None = None
        for block in cfg.managed_blocks:
            canonical_path = repo_root / block.source
            canonical = canonical_path.read_text(encoding="utf-8")
            try:
                res = replace_managed_block(
                    text=updated_text,
                    block_name=block.name,
                    canonical_content=canonical,
                    strict=strict,
                )
            except ManagedBlockError as e:
                file_error = str(e)
                break

            updated_text = res.updated_text
            if res.changed:
                changed_blocks.append(block.name)

        if file_error:
            changes.append(Change(kind="error", target=target_name, path=rel, detail=file_error))
            continue

        if not changed_blocks:
            changes.append(Change(kind="skip", target=target_name, path=rel, detail="managed blocks unchanged"))
            continue

        if not dry_run:
            target_path.write_text(updated_text, encoding="utf-8")
        changes.append(Change(kind="update", target=target_name, path=rel, detail=f"managed blocks: {', '.join(changed_blocks)}"))

    return changes


def sync_skills(
    *,
    cfg: TemplateSyncConfig,
    repo_root: Path,
    target_name: str,
    dry_run: bool,
) -> list[Change]:
    if cfg.skills_mode == "disabled":
        return []

    source_skills_root = cfg.source_dir / cfg.skills_root
    if not source_skills_root.exists():
        return []

    target_skills_root = repo_root / target_name / cfg.skills_root
    changes: list[Change] = []

    for skill_dir in sorted(p for p in source_skills_root.iterdir() if p.is_dir()):
        skill_name = skill_dir.name
        target_skill_dir = target_skills_root / skill_name
        if not target_skill_dir.exists():
            continue

        for src_file in skill_dir.rglob("*"):
            if not src_file.is_file():
                continue
            rel = src_file.relative_to(cfg.source_dir).as_posix()
            if matches_any(rel, cfg.ignore_patterns):
                continue
            dst_file = repo_root / target_name / rel
            changes.append(sync_file(src=src_file, dst=dst_file, rel_posix=rel, target_name=target_name, dry_run=dry_run))

    return changes


def sync_target(
    *,
    cfg: TemplateSyncConfig,
    repo_root: Path,
    target_name: str,
    dry_run: bool,
    strict: bool,
    with_skills: bool,
) -> list[Change]:
    changes: list[Change] = []
    changes.extend(sync_keep_updated(cfg=cfg, repo_root=repo_root, target_name=target_name, dry_run=dry_run))
    changes.extend(sync_managed_blocks(cfg=cfg, repo_root=repo_root, target_name=target_name, dry_run=dry_run, strict=strict))
    if with_skills:
        changes.extend(sync_skills(cfg=cfg, repo_root=repo_root, target_name=target_name, dry_run=dry_run))
    return changes
