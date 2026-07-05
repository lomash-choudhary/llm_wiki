# LLM Wiki Ingest

Use this skill when adding Raw source material and compiling it into reusable Wiki notes.

## Instructions

1. Put cleaned source Markdown in `Raw/Sources/`.
2. Use the source frontmatter from `Schema/frontmatter-schema.md`.
3. Search `Wiki/catalog.jsonl` before opening broad Raw context, if the catalog exists.
4. Create or update focused notes under `Wiki/`, not under `Raw/`.
5. Link every compiled note back to one or more Raw sources in frontmatter.
6. Keep `source_count` equal to the number of source links.
7. Mark a Raw source `Processed: true` only after compiled Wiki notes cover it.
8. Run build, lint, source scan, and source lint checks before committing.

Never invent citations or create unsupported claims.
