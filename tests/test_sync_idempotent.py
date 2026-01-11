from __future__ import annotations

from pathlib import Path

import yaml

from template_sync.config import load_config
from template_sync.sync import sync_target


def test_sync_is_idempotent(tmp_path: Path):
    repo = tmp_path

    # Minimal default source
    (repo / "default" / "managed_blocks" / "claude").mkdir(parents=True)
    (repo / "default" / "managed_blocks" / "claude" / "general_rules.md").write_text("RULES\n", encoding="utf-8")
    (repo / "default" / ".gitignore").write_text("*.tmp\n", encoding="utf-8")

    # Target template
    (repo / "t1").mkdir()
    (repo / "t1" / "CLAUDE.md").write_text("<general_rules>old</general_rules>\n", encoding="utf-8")

    # Config
    cfg_path = repo / "default" / "template-sync.yaml"
    cfg_path.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "source": {"dir": "default"},
                "targets": {"mode": "explicit", "list": ["t1"]},
                "sync": {"keep_updated": [".gitignore"], "never_update": []},
                "managed_blocks": {
                    "files": ["CLAUDE.md"],
                    "blocks": {"general_rules": {"source": "default/managed_blocks/claude/general_rules.md"}},
                },
                "skills": {"root": ".claude/skills", "mode": "disabled"},
                "ignore": {"patterns": []},
            }
        ),
        encoding="utf-8",
    )

    cfg = load_config(cfg_path, repo_root=repo)

    # First run applies changes
    changes_1 = sync_target(cfg=cfg, repo_root=repo, target_name="t1", dry_run=False, strict=True, with_skills=False)
    assert any(c.kind in ("create", "update") for c in changes_1)

    # Second run should be clean (all skips)
    changes_2 = sync_target(cfg=cfg, repo_root=repo, target_name="t1", dry_run=False, strict=True, with_skills=False)
    assert all(c.kind == "skip" for c in changes_2)
