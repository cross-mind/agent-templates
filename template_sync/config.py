from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml


@dataclass(frozen=True)
class ManagedBlock:
    name: str
    source: Path


@dataclass(frozen=True)
class TemplateSyncConfig:
    version: int
    source_dir: Path

    targets_mode: Literal["explicit", "discover"]
    targets_list: tuple[str, ...]
    targets_exclude: tuple[str, ...]

    keep_updated: tuple[str, ...]
    never_update: tuple[str, ...]

    managed_files: tuple[str, ...]
    managed_blocks: tuple[ManagedBlock, ...]

    skills_root: Path
    skills_mode: Literal["sync_all", "update_if_exists", "disabled"]

    ignore_patterns: tuple[str, ...]


def _require_dict(value: Any, *, path: str) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    raise ValueError(f"Expected mapping at {path}, got {type(value).__name__}")


def _require_list(value: Any, *, path: str) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    raise ValueError(f"Expected list at {path}, got {type(value).__name__}")


def load_config(config_path: Path, *, repo_root: Path) -> TemplateSyncConfig:
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    raw = _require_dict(raw, path="root")

    version = int(raw.get("version", 1))

    source = _require_dict(raw.get("source", {}), path="source")
    source_dir = Path(str(source.get("dir", "default")))

    targets = _require_dict(raw.get("targets", {}), path="targets")
    targets_mode = str(targets.get("mode", "discover"))
    if targets_mode not in ("explicit", "discover"):
        raise ValueError("targets.mode must be 'explicit' or 'discover'")

    targets_list = tuple(str(x) for x in _require_list(targets.get("list"), path="targets.list"))
    targets_exclude = tuple(str(x) for x in _require_list(targets.get("exclude"), path="targets.exclude"))

    sync = _require_dict(raw.get("sync", {}), path="sync")
    keep_updated = tuple(str(x) for x in _require_list(sync.get("keep_updated"), path="sync.keep_updated"))
    never_update = tuple(str(x) for x in _require_list(sync.get("never_update"), path="sync.never_update"))

    managed = _require_dict(raw.get("managed_blocks", {}), path="managed_blocks")
    managed_files = tuple(str(x) for x in _require_list(managed.get("files"), path="managed_blocks.files"))
    managed_blocks_raw = _require_dict(managed.get("blocks", {}), path="managed_blocks.blocks")
    managed_blocks: list[ManagedBlock] = []
    for block_name, block_cfg_raw in managed_blocks_raw.items():
        block_cfg = _require_dict(block_cfg_raw, path=f"managed_blocks.blocks.{block_name}")
        source_rel = block_cfg.get("source")
        if not source_rel:
            raise ValueError(f"managed_blocks.blocks.{block_name}.source is required")
        managed_blocks.append(ManagedBlock(name=str(block_name), source=Path(str(source_rel))))

    skills = _require_dict(raw.get("skills", {}), path="skills")
    skills_root = Path(str(skills.get("root", ".claude/skills")))
    skills_mode = str(skills.get("mode", "update_if_exists"))
    if skills_mode not in ("sync_all", "update_if_exists", "disabled"):
        raise ValueError("skills.mode must be 'sync_all', 'update_if_exists', or 'disabled'")

    ignore = _require_dict(raw.get("ignore", {}), path="ignore")
    ignore_patterns = tuple(str(x) for x in _require_list(ignore.get("patterns"), path="ignore.patterns"))

    return TemplateSyncConfig(
        version=version,
        source_dir=repo_root / source_dir,
        targets_mode=targets_mode,  # type: ignore[arg-type]
        targets_list=targets_list,
        targets_exclude=targets_exclude,
        keep_updated=keep_updated,
        never_update=never_update,
        managed_files=managed_files,
        managed_blocks=tuple(managed_blocks),
        skills_root=skills_root,
        skills_mode=skills_mode,  # type: ignore[arg-type]
        ignore_patterns=ignore_patterns,
    )
