# Command Reference

Run these commands from the vault root.

## Health

```bash
python3 scripts/wiki_tool.py doctor
```

Checks required folders, Python version, catalog state, source manifest state, and basic note counts. This command does not change files.

## Build

```bash
python3 scripts/wiki_tool.py build
```

Generates:

- `Wiki/catalog.jsonl`
- `Wiki/index.md`
- `Wiki/Topics/index.md`
- `Wiki/Concepts/index.md`
- `Wiki/Entities/index.md`
- `Wiki/Projects/index.md`
- `Wiki/Logs/index.md`

## Lint

```bash
python3 scripts/wiki_tool.py lint
```

Checks compiled Wiki note frontmatter, allowed tags, source links, and `source_count`.

## Source Commands

```bash
python3 scripts/wiki_tool.py source-scan
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
python3 scripts/wiki_tool.py source-delta
python3 scripts/wiki_tool.py source-coverage
```

- `source-scan` lists Raw sources.
- `source-scan --update --accept-covered` writes `Schema/source-manifest.jsonl`.
- `source-lint` checks Raw source frontmatter and coverage.
- `source-delta` compares `Raw/Sources/` with the manifest.
- `source-coverage` shows which Raw sources are covered by compiled Wiki notes.

## Search

```bash
python3 scripts/wiki_tool.py search-catalog --query "text"
```

Searches `Wiki/catalog.jsonl`.

## Log

```bash
python3 scripts/wiki_tool.py log --title "title" --details "details"
```

Appends a short entry to `Wiki/log.md`.

## Hooks And Audit

```bash
sh scripts/install_hooks.sh
python3 scripts/audit_public.py
```

`install_hooks.sh` points Git at `.githooks/`. The pre-commit hook runs build, lint, and source lint. `audit_public.py` fails on obvious secrets, machine-local paths, private keys, and Obsidian plugin or cache state.
