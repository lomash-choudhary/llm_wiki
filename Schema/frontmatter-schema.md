# Frontmatter Schema

This vault uses simple YAML frontmatter so agents can check notes reliably.

## Raw Source Notes

Raw source notes live in `Raw/Sources/`.

Required fields:

```yaml
---
Title: ""
Author: ""
Reference: ""
ContentType:
  - "markdown"
Created: YYYY-MM-DD
Processed: false
tags:
  - "source"
---
```

Field meanings:

- `Title`: human-readable source title.
- `Author`: source author or owner, if known.
- `Reference`: URL, citation, file reference, or stable local reference.
- `ContentType`: one or more content types, such as `markdown`, `transcript`, `article`, or `notes`.
- `Created`: date the source note was created, using `YYYY-MM-DD`.
- `Processed`: `false` until the source has been compiled into Wiki notes.
- `tags`: must include `source`.

## Compiled Wiki Notes

Compiled notes live under `Wiki/`.

Required fields:

```yaml
---
tags:
  - "concept"
topics: []
status: seed
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
source_count: 0
aliases: []
---
```

Allowed compiled note tags:

- `topic`
- `concept`
- `entity`
- `project`
- `log`

Rules:

- Use exactly one main compiled note tag.
- Every path in `sources` must point to an existing file under `Raw/Sources/`.
- `source_count` must equal the number of paths in `sources`.
- `created` and `updated` must use `YYYY-MM-DD`.
- `status` should start as `seed` for early notes.
