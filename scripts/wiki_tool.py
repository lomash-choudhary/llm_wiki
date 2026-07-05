#!/usr/bin/env python3
"""Deterministic maintenance tool for the LLM Wiki core."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = [
    "Raw/Sources",
    "Raw/Files",
    "Wiki/Topics",
    "Wiki/Concepts",
    "Wiki/Entities",
    "Wiki/Projects",
    "Wiki/Logs",
    "Schema",
    "_templates",
    ".agents/skills",
    "scripts",
    "tutorial",
]

WIKI_FOLDERS = {
    "Wiki/Topics": "topic",
    "Wiki/Concepts": "concept",
    "Wiki/Entities": "entity",
    "Wiki/Projects": "project",
    "Wiki/Logs": "log",
}

ALLOWED_TAGS = {"topic", "concept", "entity", "project", "log"}
CATALOG_PATH = ROOT / "Wiki/catalog.jsonl"
SOURCE_MANIFEST_PATH = ROOT / "Schema/source-manifest.jsonl"


def today() -> str:
    return _dt.date.today().isoformat()


def relpath(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def print_ok(message: str) -> None:
    print(f"OK: {message}")


def print_warn(message: str) -> None:
    print(f"WARN: {message}")


def print_fail(message: str) -> None:
    print(f"FAIL: {message}")


def split_frontmatter(text: str) -> tuple[dict[str, object], str, bool]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, False

    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break

    if end is None:
        return {}, text, False

    frontmatter = parse_frontmatter_lines(lines[1:end])
    body = "\n".join(lines[end + 1 :])
    return frontmatter, body, True


def parse_frontmatter_lines(lines: list[str]) -> dict[str, object]:
    data: dict[str, object] = {}
    current_key: str | None = None

    for raw_line in lines:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        if raw_line.startswith("  - ") and current_key:
            item = raw_line[4:].strip()
            value = data.setdefault(current_key, [])
            if not isinstance(value, list):
                value = [value]
                data[current_key] = value
            value.append(parse_scalar(item))
            continue

        current_key = None
        if ":" not in raw_line:
            continue

        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            continue

        if raw_value == "":
            data[key] = []
            current_key = key
        else:
            data[key] = parse_scalar(raw_value)

    return data


def parse_scalar(value: str) -> object:
    value = value.strip()
    if value in {"[]", "[ ]"}:
        return []
    if value in {"{}", "{ }"}:
        return {}

    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None

    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]

    if re.fullmatch(r"-?\d+", value):
        try:
            return int(value)
        except ValueError:
            pass

    return value


def ensure_list(value: object) -> list[object]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def string_list(value: object) -> list[str]:
    return [str(item) for item in ensure_list(value) if item is not None]


def read_note(path: Path) -> tuple[dict[str, object], str, bool]:
    text = path.read_text(encoding="utf-8")
    return split_frontmatter(text)


def h1_title(body: str) -> str | None:
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if title:
                return title
    return None


def title_from_path(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()


def note_title(path: Path, frontmatter: dict[str, object], body: str) -> str:
    for key in ("title", "Title"):
        value = frontmatter.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return h1_title(body) or title_from_path(path)


def compiled_note_paths() -> list[Path]:
    paths: list[Path] = []
    for folder in WIKI_FOLDERS:
        base = ROOT / folder
        if not base.exists():
            continue
        paths.extend(
            path
            for path in base.rglob("*.md")
            if path.name != "index.md" and path.is_file()
        )
    return sorted(paths, key=relpath)


def source_note_paths() -> list[Path]:
    base = ROOT / "Raw/Sources"
    if not base.exists():
        return []
    return sorted((path for path in base.rglob("*.md") if path.is_file()), key=relpath)


def expected_tag_for_path(path: Path) -> str | None:
    rel = relpath(path)
    for folder, tag in WIKI_FOLDERS.items():
        if rel.startswith(f"{folder}/"):
            return tag
    return None


def primary_tag(frontmatter: dict[str, object], fallback: str | None = None) -> str:
    tags = string_list(frontmatter.get("tags"))
    allowed = [tag for tag in tags if tag in ALLOWED_TAGS]
    if allowed:
        return allowed[0]
    return fallback or "concept"


def updated_value(frontmatter: dict[str, object]) -> str:
    for key in ("updated", "Updated", "Created", "created"):
        value = frontmatter.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return today()


def catalog_entries() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for path in compiled_note_paths():
        frontmatter, body, _ = read_note(path)
        fallback_tag = expected_tag_for_path(path)
        entries.append(
            {
                "path": relpath(path),
                "title": note_title(path, frontmatter, body),
                "tag": primary_tag(frontmatter, fallback_tag),
                "topics": string_list(frontmatter.get("topics")),
                "sources": string_list(frontmatter.get("sources")),
                "updated": updated_value(frontmatter),
            }
        )
    return sorted(entries, key=lambda item: str(item["path"]))


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    if not path.exists():
        return records
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{relpath(path)}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{relpath(path)}:{line_number}: record is not an object")
        records.append(record)
    return records


def section_title(folder: str) -> str:
    return Path(folder).name


def write_index_files(entries: list[dict[str, object]]) -> None:
    counts = {tag: 0 for tag in ALLOWED_TAGS}
    for entry in entries:
        tag = str(entry.get("tag", ""))
        if tag in counts:
            counts[tag] += 1

    summary_lines = [
        "# Wiki Index",
        "",
        "Generated by `python3 scripts/wiki_tool.py build`.",
        "",
        "## Summary",
        "",
        f"- Topics: {counts['topic']}",
        f"- Concepts: {counts['concept']}",
        f"- Entities: {counts['entity']}",
        f"- Projects: {counts['project']}",
        f"- Logs: {counts['log']}",
        "",
        "## Sections",
        "",
    ]
    for folder in WIKI_FOLDERS:
        name = section_title(folder)
        summary_lines.append(f"- [{name}]({name}/index.md)")
    summary_lines.append("")
    (ROOT / "Wiki/index.md").write_text("\n".join(summary_lines), encoding="utf-8")

    by_folder: dict[str, list[dict[str, object]]] = {folder: [] for folder in WIKI_FOLDERS}
    for entry in entries:
        path = str(entry["path"])
        for folder in WIKI_FOLDERS:
            if path.startswith(f"{folder}/"):
                by_folder[folder].append(entry)
                break

    for folder, folder_entries in by_folder.items():
        folder_path = ROOT / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        title = section_title(folder)
        lines = [
            f"# {title} Index",
            "",
            "Generated by `python3 scripts/wiki_tool.py build`.",
            "",
        ]
        if not folder_entries:
            lines.append("No notes yet.")
        else:
            for entry in folder_entries:
                note_name = Path(str(entry["path"])).name
                lines.append(f"- [{entry['title']}]({note_name})")
        lines.append("")
        (folder_path / "index.md").write_text("\n".join(lines), encoding="utf-8")


def source_coverage_map() -> dict[str, list[str]]:
    coverage: dict[str, list[str]] = {}
    for entry in catalog_entries():
        compiled_path = str(entry["path"])
        for source in string_list(entry.get("sources")):
            coverage.setdefault(source, []).append(compiled_path)
    return {key: sorted(value) for key, value in sorted(coverage.items())}


def raw_processed(frontmatter: dict[str, object]) -> bool:
    return bool(frontmatter.get("Processed", False))


def source_records(accept_covered: bool = False) -> list[dict[str, object]]:
    coverage = source_coverage_map()
    records: list[dict[str, object]] = []
    for path in source_note_paths():
        frontmatter, body, _ = read_note(path)
        source_path = relpath(path)
        covered_by = coverage.get(source_path, [])
        processed = raw_processed(frontmatter) or (accept_covered and bool(covered_by))
        records.append(
            {
                "path": source_path,
                "title": note_title(path, frontmatter, body),
                "processed": processed,
                "covered_by": covered_by,
                "updated": updated_value(frontmatter),
            }
        )
    return sorted(records, key=lambda item: str(item["path"]))


def is_valid_source_path(value: str) -> bool:
    source_path = Path(value)
    if source_path.is_absolute():
        return False
    parts = source_path.parts
    if ".." in parts:
        return False
    return value.startswith("Raw/Sources/") and (ROOT / value).is_file()


def check_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        _dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def cmd_doctor(_args: argparse.Namespace) -> int:
    failures = 0
    print("LLM Wiki doctor")

    if sys.version_info >= (3, 9):
        print_ok(f"Python {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print_fail("Python 3.9 or newer is recommended")
        failures += 1

    for folder in REQUIRED_DIRS:
        if (ROOT / folder).is_dir():
            print_ok(f"{folder}/ exists")
        else:
            print_fail(f"{folder}/ is missing")
            failures += 1

    for path, label in ((CATALOG_PATH, "catalog"), (SOURCE_MANIFEST_PATH, "source manifest")):
        if path.exists():
            try:
                count = len(read_jsonl(path))
            except ValueError as exc:
                print_fail(str(exc))
                failures += 1
            else:
                print_ok(f"{label} has {count} record(s)")
        else:
            print_warn(f"{label} is missing; run the matching build or source-scan command")

    print_ok(f"Raw source notes: {len(source_note_paths())}")
    print_ok(f"Compiled Wiki notes: {len(compiled_note_paths())}")
    return 1 if failures else 0


def cmd_build(_args: argparse.Namespace) -> int:
    entries = catalog_entries()
    write_jsonl(CATALOG_PATH, entries)
    write_index_files(entries)
    print_ok(f"wrote {relpath(CATALOG_PATH)} with {len(entries)} record(s)")
    print_ok("wrote Wiki index files")
    return 0


def cmd_lint(_args: argparse.Namespace) -> int:
    errors: list[str] = []

    for path in compiled_note_paths():
        frontmatter, _body, has_frontmatter = read_note(path)
        location = relpath(path)
        if not has_frontmatter:
            errors.append(f"{location}: missing YAML frontmatter")
            continue

        tags = string_list(frontmatter.get("tags"))
        allowed_tags = [tag for tag in tags if tag in ALLOWED_TAGS]
        if len(tags) != 1 or len(allowed_tags) != 1:
            errors.append(
                f"{location}: tags must contain exactly one allowed tag "
                f"({', '.join(sorted(ALLOWED_TAGS))})"
            )

        sources = string_list(frontmatter.get("sources"))
        source_count = frontmatter.get("source_count")
        if not isinstance(source_count, int):
            errors.append(f"{location}: source_count must be an integer")
        elif source_count != len(sources):
            errors.append(
                f"{location}: source_count is {source_count}, but sources has {len(sources)} item(s)"
            )

        for source in sources:
            if not is_valid_source_path(source):
                errors.append(f"{location}: source does not exist under Raw/Sources/: {source}")

    if errors:
        for error in errors:
            print_fail(error)
        return 1

    print_ok(f"lint passed for {len(compiled_note_paths())} compiled note(s)")
    return 0


def cmd_source_scan(args: argparse.Namespace) -> int:
    records = source_records(accept_covered=args.accept_covered)
    for record in records:
        print(json.dumps(record, sort_keys=True))

    if args.update:
        write_jsonl(SOURCE_MANIFEST_PATH, records)
        print_ok(f"wrote {relpath(SOURCE_MANIFEST_PATH)} with {len(records)} record(s)")

    if not records:
        print_ok("no Raw source notes found")
    return 0


def cmd_source_lint(_args: argparse.Namespace) -> int:
    errors: list[str] = []
    coverage = source_coverage_map()
    manifest_by_path: dict[str, dict[str, object]] = {}

    if SOURCE_MANIFEST_PATH.exists():
        try:
            manifest_by_path = {
                str(record.get("path")): record for record in read_jsonl(SOURCE_MANIFEST_PATH)
            }
        except ValueError as exc:
            errors.append(str(exc))

    current_sources = {relpath(path) for path in source_note_paths()}
    for source_path, record in manifest_by_path.items():
        if source_path and source_path not in current_sources:
            errors.append(f"{relpath(SOURCE_MANIFEST_PATH)}: stale source path {source_path}")
        if bool(record.get("processed", False)) and not record.get("covered_by"):
            errors.append(f"{source_path}: manifest says processed but has no Wiki coverage")

    for path in source_note_paths():
        frontmatter, _body, has_frontmatter = read_note(path)
        location = relpath(path)
        if not has_frontmatter:
            errors.append(f"{location}: missing YAML frontmatter")
            continue

        for key in ("Title", "Reference", "Created", "Processed", "tags"):
            if key not in frontmatter:
                errors.append(f"{location}: missing required field {key}")

        if "Created" in frontmatter and not check_date(frontmatter.get("Created")):
            errors.append(f"{location}: Created must use YYYY-MM-DD")

        tags = string_list(frontmatter.get("tags"))
        if "source" not in tags:
            errors.append(f"{location}: tags must include source")

        processed = raw_processed(frontmatter)
        if processed and not coverage.get(location):
            errors.append(f"{location}: Processed is true but no compiled Wiki note covers it")

    if errors:
        for error in errors:
            print_fail(error)
        return 1

    print_ok(f"source-lint passed for {len(source_note_paths())} Raw source note(s)")
    return 0


def cmd_source_delta(_args: argparse.Namespace) -> int:
    current = {relpath(path) for path in source_note_paths()}
    manifest = set()
    if SOURCE_MANIFEST_PATH.exists():
        manifest = {str(record.get("path")) for record in read_jsonl(SOURCE_MANIFEST_PATH)}

    missing = sorted(current - manifest)
    stale = sorted(manifest - current)

    if not missing and not stale:
        print_ok("source manifest matches Raw/Sources")
    for path in missing:
        print(f"MISSING_FROM_MANIFEST: {path}")
    for path in stale:
        print(f"STALE_IN_MANIFEST: {path}")
    return 0


def cmd_source_coverage(_args: argparse.Namespace) -> int:
    coverage = source_coverage_map()
    sources = source_note_paths()
    if not sources:
        print_ok("no Raw source notes found")
        return 0

    for path in sources:
        source_path = relpath(path)
        covered_by = coverage.get(source_path, [])
        if covered_by:
            print(f"COVERED: {source_path} -> {', '.join(covered_by)}")
        else:
            print(f"UNCOVERED: {source_path}")
    return 0


def cmd_search_catalog(args: argparse.Namespace) -> int:
    query = args.query.lower().strip()
    if not CATALOG_PATH.exists():
        print_fail("Wiki/catalog.jsonl is missing; run `python3 scripts/wiki_tool.py build`")
        return 1

    matches = []
    for record in read_jsonl(CATALOG_PATH):
        haystack = " ".join(
            [
                str(record.get("path", "")),
                str(record.get("title", "")),
                str(record.get("tag", "")),
                " ".join(string_list(record.get("topics"))),
                " ".join(string_list(record.get("sources"))),
            ]
        ).lower()
        if query in haystack:
            matches.append(record)

    for record in matches:
        print(json.dumps(record, sort_keys=True))
    if not matches:
        print_ok("no catalog matches")
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    log_path = ROOT / "Wiki/log.md"
    entry = [
        f"## {today()} - {args.title}",
        "",
        args.details.strip(),
        "",
    ]
    if not log_path.exists():
        log_path.write_text("# Wiki Log\n\n", encoding="utf-8")
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(entry))
    print_ok(f"appended log entry to {relpath(log_path)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain the LLM Wiki core")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="run non-mutating health checks")
    doctor.set_defaults(func=cmd_doctor)

    build = subparsers.add_parser("build", help="build catalog and index files")
    build.set_defaults(func=cmd_build)

    lint = subparsers.add_parser("lint", help="lint compiled Wiki notes")
    lint.set_defaults(func=cmd_lint)

    source_scan = subparsers.add_parser("source-scan", help="scan Raw source notes")
    source_scan.add_argument("--update", action="store_true", help="write source manifest")
    source_scan.add_argument(
        "--accept-covered",
        action="store_true",
        help="mark covered sources processed in the manifest",
    )
    source_scan.set_defaults(func=cmd_source_scan)

    source_lint = subparsers.add_parser("source-lint", help="lint Raw source notes")
    source_lint.set_defaults(func=cmd_source_lint)

    source_delta = subparsers.add_parser("source-delta", help="show source manifest deltas")
    source_delta.set_defaults(func=cmd_source_delta)

    source_coverage = subparsers.add_parser("source-coverage", help="show source coverage")
    source_coverage.set_defaults(func=cmd_source_coverage)

    search_catalog = subparsers.add_parser("search-catalog", help="search Wiki/catalog.jsonl")
    search_catalog.add_argument("--query", required=True, help="search text")
    search_catalog.set_defaults(func=cmd_search_catalog)

    log = subparsers.add_parser("log", help="append a short entry to Wiki/log.md")
    log.add_argument("--title", required=True, help="log entry title")
    log.add_argument("--details", required=True, help="log entry details")
    log.set_defaults(func=cmd_log)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
