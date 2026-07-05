# Workflow Examples

## Ingest A New Source

1. Add a cleaned Markdown source note under `Raw/Sources/`.
2. Fill in the required source frontmatter.
3. Search `Wiki/catalog.jsonl` for related compiled notes before reading broad Raw context.
4. Create or update focused notes under `Wiki/`.
5. Add the Raw source path to each compiled note's `sources` list.
6. Update `source_count` on each compiled note.
7. Mark the Raw source `Processed: true` only after Wiki notes cover it.
8. Run build, lint, source scan, and source lint checks.

## Answer A Question

1. Start with `Wiki/index.md` when it exists.
2. Search `Wiki/catalog.jsonl` for the user's topic.
3. Open the most relevant compiled Wiki notes.
4. Open Raw sources only if more evidence or exact detail is needed.
5. Cite the compiled note and Raw source when the answer depends on source material.

## Maintain The Wiki

1. Keep note frontmatter consistent with `Schema/frontmatter-schema.md`.
2. Keep naming consistent with `Schema/naming-conventions.md`.
3. Rebuild indexes and catalog after compiled notes change.
4. Run the lint checklist before each meaningful commit.
