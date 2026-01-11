from __future__ import annotations

from pathlib import Path

import yaml
from template_sync.config import load_config
from template_sync.sync import sync_target


def _write_config(repo: Path, *, skills_mode: str) -> None:
    cfg_path = repo / "default" / "template-sync.yaml"
    cfg_path.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "source": {"dir": "default"},
                "targets": {"mode": "explicit", "list": ["t1"]},
                "sync": {"keep_updated": [], "never_update": []},
                "managed_blocks": {"files": [], "blocks": {}},
                "skills": {"root": ".claude/skills", "mode": skills_mode},
                "ignore": {"patterns": []},
            }
        ),
        encoding="utf-8",
    )


def test_skills_sync_all_creates_missing_skill_dirs(tmp_path: Path) -> None:
    repo = tmp_path

    (repo / "default" / ".claude" / "skills" / "new-skill").mkdir(parents=True)
    (repo / "default" / ".claude" / "skills" / "new-skill" / "SKILL.md").write_text("hi\n", encoding="utf-8")

    (repo / "t1").mkdir()

    _write_config(repo, skills_mode="sync_all")
    cfg = load_config(repo / "default" / "template-sync.yaml", repo_root=repo)

    changes_1 = sync_target(cfg=cfg, repo_root=repo, target_name="t1", dry_run=False, strict=True, with_skills=True)
    assert any(c.kind == "create" and c.path == ".claude/skills/new-skill/SKILL.md" for c in changes_1)
    assert (repo / "t1" / ".claude" / "skills" / "new-skill" / "SKILL.md").read_text(encoding="utf-8") == "hi\n"

    changes_2 = sync_target(cfg=cfg, repo_root=repo, target_name="t1", dry_run=False, strict=True, with_skills=True)
    assert any(c.kind == "skip" and c.path == ".claude/skills/new-skill/SKILL.md" for c in changes_2)


def test_skills_update_if_exists_does_not_create_new_skill_dirs(tmp_path: Path) -> None:
    repo = tmp_path

    (repo / "default" / ".claude" / "skills" / "new-skill").mkdir(parents=True)
    (repo / "default" / ".claude" / "skills" / "new-skill" / "SKILL.md").write_text("hi\n", encoding="utf-8")

    (repo / "t1").mkdir()

    _write_config(repo, skills_mode="update_if_exists")
    cfg = load_config(repo / "default" / "template-sync.yaml", repo_root=repo)

    changes = sync_target(cfg=cfg, repo_root=repo, target_name="t1", dry_run=False, strict=True, with_skills=True)
    assert not any(c.path == ".claude/skills/new-skill/SKILL.md" and c.kind == "create" for c in changes)
    assert not (repo / "t1" / ".claude" / "skills" / "new-skill" / "SKILL.md").exists()


def test_skills_update_if_exists_updates_existing_skill_dir(tmp_path: Path) -> None:
    repo = tmp_path

    (repo / "default" / ".claude" / "skills" / "new-skill").mkdir(parents=True)
    (repo / "default" / ".claude" / "skills" / "new-skill" / "SKILL.md").write_text("hi\n", encoding="utf-8")

    (repo / "t1" / ".claude" / "skills" / "new-skill").mkdir(parents=True)

    _write_config(repo, skills_mode="update_if_exists")
    cfg = load_config(repo / "default" / "template-sync.yaml", repo_root=repo)

    changes = sync_target(cfg=cfg, repo_root=repo, target_name="t1", dry_run=False, strict=True, with_skills=True)
    assert any(c.kind == "create" and c.path == ".claude/skills/new-skill/SKILL.md" for c in changes)
    assert (repo / "t1" / ".claude" / "skills" / "new-skill" / "SKILL.md").read_text(encoding="utf-8") == "hi\n"
