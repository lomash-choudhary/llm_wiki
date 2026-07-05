# Lint Checklist

Use this checklist before committing Wiki changes.

## Folder Checks

- Raw source notes are under `Raw/Sources/`.
- Compiled reusable notes are under `Wiki/`.
- Schema and workflow docs are under `Schema/`.
- Templates are under `_templates/`.
- Scripts are under `scripts/`.

## Source Checks

- Raw source notes include `Title`, `Reference`, `Created`, `Processed`, and `tags`.
- Raw source notes include the `source` tag.
- Processed Raw sources are covered by at least one compiled Wiki note.

## Wiki Note Checks

- Compiled Wiki notes use one allowed tag: `topic`, `concept`, `entity`, `project`, or `log`.
- Compiled Wiki notes include a `sources` list.
- Each source path points to an existing file under `Raw/Sources/`.
- `source_count` equals the number of source paths.
- Claims are supported by the listed sources.
- Unsupported ideas are written as questions or omitted.

## Commit Checks

- Build generated indexes and catalog when the tooling exists.
- Run `lint` and source checks when the tooling exists.
- Do not commit Obsidian workspace churn, plugin files, caches, drafts, or ignored binary Raw files.
- Keep the commit limited to the requested tutorial step.
