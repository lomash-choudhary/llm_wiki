# LLM Wiki Lint

Use this skill when checking Wiki quality before a commit.

## Instructions

1. Check notes against `Schema/frontmatter-schema.md`.
2. Use `Schema/lint-checklist.md` as the human-readable checklist.
3. Confirm compiled notes use one allowed tag: `topic`, `concept`, `entity`, `project`, or `log`.
4. Confirm each compiled note has valid `sources` paths under `Raw/Sources/`.
5. Confirm `source_count` equals the number of source links.
6. Confirm processed Raw sources have Wiki coverage.
7. Run the deterministic lint and source checks when `scripts/wiki_tool.py` exists.

Report failures clearly and fix them before committing unless the user asks for a review only.
