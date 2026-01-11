from __future__ import annotations

from dataclasses import dataclass


class ManagedBlockError(ValueError):
    pass


@dataclass(frozen=True)
class ManagedBlockResult:
    updated_text: str
    changed: bool
    reason: str


def replace_managed_block(
    *,
    text: str,
    block_name: str,
    canonical_content: str,
    strict: bool,
) -> ManagedBlockResult:
    open_tag = f"<{block_name}>"
    close_tag = f"</{block_name}>"

    newline = "\r\n" if "\r\n" in text else "\n"
    canonical_body = canonical_content.replace("\r\n", "\n").rstrip("\n")
    canonical_lines = [line + newline for line in canonical_body.split("\n")] if canonical_body else []

    lines = text.splitlines(keepends=True)

    open_line_indices: list[int] = []
    close_line_indices: list[int] = []
    single_line_indices: list[int] = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == open_tag:
            open_line_indices.append(i)
        elif stripped == close_tag:
            close_line_indices.append(i)
        elif stripped.startswith(open_tag) and stripped.endswith(close_tag):
            single_line_indices.append(i)

    if open_line_indices:
        if len(open_line_indices) != 1:
            raise ManagedBlockError(f"Multiple {open_tag} blocks found")
        if len(close_line_indices) != 1:
            raise ManagedBlockError(f"Expected exactly one {close_tag}, found {len(close_line_indices)}")

        open_idx = open_line_indices[0]
        close_idx = close_line_indices[0]
        if close_idx <= open_idx:
            raise ManagedBlockError(f"{close_tag} appears before {open_tag}")

        current_inner_lines = lines[open_idx + 1 : close_idx]
        if current_inner_lines == canonical_lines:
            return ManagedBlockResult(updated_text=text, changed=False, reason="unchanged")

        updated_lines = lines[: open_idx + 1] + canonical_lines + lines[close_idx:]
        updated_text = "".join(updated_lines)
        return ManagedBlockResult(updated_text=updated_text, changed=True, reason="updated")

    if single_line_indices:
        if len(single_line_indices) != 1:
            raise ManagedBlockError(f"Multiple {open_tag} blocks found")
        if close_line_indices:
            raise ManagedBlockError(f"Invalid mixed single-line and multi-line {open_tag} markers")

        idx = single_line_indices[0]
        original_line = lines[idx]
        indent_len = len(original_line) - len(original_line.lstrip(" \t"))
        indent = original_line[:indent_len]
        line_newline = "\r\n" if original_line.endswith("\r\n") else "\n" if original_line.endswith("\n") else newline

        replacement = [f"{indent}{open_tag}{line_newline}"]
        replacement.extend([line.replace("\n", line_newline) for line in canonical_lines])
        replacement.append(f"{indent}{close_tag}{line_newline}")

        updated_lines = lines[:idx] + replacement + lines[idx + 1 :]
        updated_text = "".join(updated_lines)

        if updated_text == text:
            return ManagedBlockResult(updated_text=text, changed=False, reason="unchanged")
        return ManagedBlockResult(updated_text=updated_text, changed=True, reason="updated")

    msg = f"Missing managed block {open_tag}...{close_tag}"
    if strict:
        raise ManagedBlockError(msg)
    return ManagedBlockResult(updated_text=text, changed=False, reason=msg)
