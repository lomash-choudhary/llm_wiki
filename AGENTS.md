# LLM Wiki Agent Rules

These rules apply to this whole vault.

## Core Boundaries

- Treat `Raw/Sources/` as source material, not as compiled notes.
- Keep binary files and attachments under `Raw/Files/`.
- Write reusable knowledge only under `Wiki/`.
- Keep schema, workflow, and linting rules under `Schema/`.
- Keep reusable note templates under `_templates/`.

## Source And Citation Rules

- Keep every compiled Wiki note linked to one or more Raw sources.
- Put source paths in the compiled note frontmatter `sources` list.
- Keep `source_count` equal to the number of entries in `sources`.
- Do not invent citations.
- Do not create unsupported claims.
- If a claim cannot be traced to a Raw source, mark it as a question or leave it out.

## Query Rules

- Search `Wiki/catalog.jsonl` before opening broad Raw context.
- Prefer compiled notes in `Wiki/` when answering ordinary questions.
- Open Raw sources only when the compiled note is missing detail, unclear, or the user asks for source-level verification.

## Commit Rules

- Run `build`, `lint`, and source checks before commits.
- After source ingestion, update source coverage before committing.
- Do not commit Obsidian workspace churn, plugin state, caches, drafts, or binary Raw files unless the user explicitly asks.
- Keep each tutorial commit limited to the current setup step.

## Expected Maintenance Commands

When the tooling exists, use:

```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
```

After ingesting or changing Raw sources, also use:

```bash
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
```
