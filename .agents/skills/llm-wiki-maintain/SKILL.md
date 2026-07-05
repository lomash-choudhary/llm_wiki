# LLM Wiki Maintain

Use this skill when keeping indexes, catalogs, manifests, and logs up to date.

## Instructions

1. Rebuild generated indexes and `Wiki/catalog.jsonl` after compiled notes change.
2. Update `Schema/source-manifest.jsonl` after Raw source coverage changes.
3. Keep `Wiki/index.md` and per-folder indexes consistent with current notes.
4. Add a short log entry when a maintenance change meaningfully changes the Wiki.
5. Run build, lint, source lint, and public audit checks when the tooling exists.
6. Keep commits small and limited to the current requested step or maintenance task.

Do not commit ignored Obsidian state, plugin caches, drafts, or binary Raw files by default.
