# LLM Wiki Query

Use this skill when answering questions from the compiled Wiki.

## Instructions

1. Start with `Wiki/index.md` when it exists.
2. Search `Wiki/catalog.jsonl` for the user's topic before opening broad Raw context.
3. Open the most relevant compiled notes under `Wiki/`.
4. Use Raw sources only when the compiled notes are insufficient or the user requests source-level verification.
5. Cite the compiled note and Raw source when an answer depends on source material.
6. Say when the Wiki does not contain enough information.

Do not invent missing facts, citations, or source coverage.
