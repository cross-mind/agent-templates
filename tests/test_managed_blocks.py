from __future__ import annotations

import pytest

from template_sync.managed_blocks import ManagedBlockError, replace_managed_block


def test_replace_managed_block_updates_only_inner_content():
    text = "before\n<general_rules>\nold\n</general_rules>\nafter\n"
    canonical = "# Title\n- rule\n"

    res = replace_managed_block(text=text, block_name="general_rules", canonical_content=canonical, strict=True)
    assert res.changed is True
    assert "<general_rules>\n# Title\n- rule\n</general_rules>" in res.updated_text
    assert res.updated_text.startswith("before\n")
    assert res.updated_text.endswith("after\n")


def test_replace_managed_block_missing_is_non_strict_skip():
    text = "no tags here\n"
    res = replace_managed_block(text=text, block_name="general_rules", canonical_content="x\n", strict=False)
    assert res.changed is False
    assert res.updated_text == text


def test_replace_managed_block_missing_is_strict_error():
    with pytest.raises(ManagedBlockError):
        replace_managed_block(text="no tags here\n", block_name="general_rules", canonical_content="x\n", strict=True)


def test_replace_managed_block_multiple_is_error():
    text = "<general_rules>a</general_rules>\n<general_rules>b</general_rules>\n"
    with pytest.raises(ManagedBlockError):
        replace_managed_block(text=text, block_name="general_rules", canonical_content="x\n", strict=True)
