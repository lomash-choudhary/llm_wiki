# Naming Conventions

Use names that are readable in Obsidian and stable in Git.

## Files

- Prefer short, descriptive Markdown file names.
- Use lowercase kebab-case for new files, such as `retrieval-augmented-generation.md`.
- Keep the `.md` extension for notes.
- Avoid dates in file names unless the note is a log or source where the date matters.
- Avoid vague names like `notes.md`, `misc.md`, or `new-file.md`.

## Raw Sources

- Store source notes in `Raw/Sources/`.
- Name source files after the source title or topic.
- Keep original evidence in the Raw note body.
- Put binary attachments in `Raw/Files/`, not directly in `Wiki/`.

## Wiki Notes

- Put topic notes in `Wiki/Topics/`.
- Put concept notes in `Wiki/Concepts/`.
- Put entity notes in `Wiki/Entities/`.
- Put project notes in `Wiki/Projects/`.
- Put log notes in `Wiki/Logs/`.
- One compiled note should focus on one reusable idea, entity, topic, project, or log entry.

## Links

- Use Obsidian links when connecting notes inside the vault.
- Use source paths in frontmatter for machine-readable source tracking.
- Keep aliases in frontmatter when a concept has common alternate names.
