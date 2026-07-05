#!/usr/bin/env python3
"""Fail on obvious private or machine-local material before publishing."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PATH_PARTS = {
    ".obsidian/plugins",
    ".obsidian/cache",
    ".obsidian/logs",
}

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"
    ),
]

LOCAL_PATH_PATTERNS = [
    re.compile("/" + "Users" + r"/[^/\s]+/"),
    re.compile("/" + "home" + r"/[^/\s]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
]


def listed_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return [
            path
            for path in ROOT.rglob("*")
            if path.is_file() and ".git" not in path.relative_to(ROOT).parts
        ]

    return [ROOT / line for line in result.stdout.splitlines() if line.strip()]


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith(".git/"):
        return True
    if rel.endswith(".DS_Store"):
        return True
    return False


def audit_path(path: Path) -> list[str]:
    rel = path.relative_to(ROOT).as_posix()
    issues: list[str] = []

    for forbidden in FORBIDDEN_PATH_PARTS:
        if rel.startswith(f"{forbidden}/"):
            issues.append(f"{rel}: forbidden Obsidian plugin/cache/log state")

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return issues

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            issues.append(f"{rel}: possible secret or private key")
            break

    for pattern in LOCAL_PATH_PATTERNS:
        if pattern.search(text):
            issues.append(f"{rel}: machine-local path")
            break

    return issues


def main() -> int:
    issues: list[str] = []
    for path in listed_files():
        if path.exists() and not should_skip(path):
            issues.extend(audit_path(path))

    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        return 1

    print("OK: public audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
