from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .config import load_config
from .sync import Change, discover_targets, sync_target


app = typer.Typer(add_completion=False, no_args_is_help=True)


def _summarize(changes: list[Change]) -> dict[str, int]:
    summary = {"create": 0, "update": 0, "skip": 0, "error": 0}
    for c in changes:
        summary[c.kind] += 1
    return summary


def _print_changes(changes: list[Change]) -> None:
    for c in changes:
        if c.kind == "skip":
            continue
        detail = f" ({c.detail})" if c.detail else ""
        typer.echo(f"[{c.target}] {c.kind.upper():6} {c.path}{detail}")


def _load(repo_root: Path, config_path: Path):
    resolved = config_path if config_path.is_absolute() else repo_root / config_path
    if not resolved.exists():
        raise typer.BadParameter(f"Config not found: {resolved}")
    return load_config(resolved, repo_root=repo_root)


@app.command()
def status(
    repo_root: Annotated[Path, typer.Option("--repo-root", exists=True, file_okay=False, dir_okay=True)] = Path("."),
    config: Annotated[Path, typer.Option("--config")] = Path("default/template-sync.yaml"),
    target: Annotated[list[str], typer.Option("--target")] = [],
    strict: Annotated[bool, typer.Option("--strict")] = False,
    with_skills: Annotated[bool, typer.Option("--with-skills/--no-skills")] = True,
    check: Annotated[bool, typer.Option("--check")] = False,
) -> None:
    """Show planned changes without writing."""
    repo_root = repo_root.resolve()
    cfg = _load(repo_root, config)

    targets = list(cfg.targets_list) if cfg.targets_mode == "explicit" else discover_targets(repo_root, exclude=cfg.targets_exclude)
    if target:
        allowed = set(targets)
        targets = [t for t in target if t in allowed]

    all_changes: list[Change] = []
    for t in targets:
        all_changes.extend(sync_target(cfg=cfg, repo_root=repo_root, target_name=t, dry_run=True, strict=strict, with_skills=with_skills))

    _print_changes(all_changes)
    summary = _summarize(all_changes)
    typer.echo(f"create={summary['create']} update={summary['update']} error={summary['error']}")

    if check and (summary["create"] or summary["update"] or summary["error"]):
        raise typer.Exit(code=1)


@app.command()
def sync(
    repo_root: Annotated[Path, typer.Option("--repo-root", exists=True, file_okay=False, dir_okay=True)] = Path("."),
    config: Annotated[Path, typer.Option("--config")] = Path("default/template-sync.yaml"),
    target: Annotated[list[str], typer.Option("--target")] = [],
    strict: Annotated[bool, typer.Option("--strict")] = False,
    with_skills: Annotated[bool, typer.Option("--with-skills/--no-skills")] = True,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
) -> None:
    """Sync templates from default to targets (idempotent)."""
    repo_root = repo_root.resolve()
    cfg = _load(repo_root, config)

    targets = list(cfg.targets_list) if cfg.targets_mode == "explicit" else discover_targets(repo_root, exclude=cfg.targets_exclude)
    if target:
        allowed = set(targets)
        targets = [t for t in target if t in allowed]

    all_changes: list[Change] = []
    for t in targets:
        all_changes.extend(sync_target(cfg=cfg, repo_root=repo_root, target_name=t, dry_run=dry_run, strict=strict, with_skills=with_skills))

    _print_changes(all_changes)
    summary = _summarize(all_changes)
    typer.echo(f"create={summary['create']} update={summary['update']} error={summary['error']}")

    if summary["error"]:
        raise typer.Exit(code=1)


def main() -> None:
    app()
