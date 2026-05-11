# Zotero Attachment Lookup Skill

Portable local-first Zotero PDF lookup skill with optional quick-reference support and deterministic storage scanning.

## Who This Is For

| Use this when you... | Use something else when you... |
| --- | --- |
| need to locate one paper PDF in local Zotero storage | need to reorganize the whole Zotero library |
| have a DOI, title, item key, attachment key, filename, or author hint | need to debug Zotero MCP startup |
| want local files checked before metadata tooling | already know the PDF path and want paper explanation |

## Why This Exists

- Local files are the highest-confidence source for actual PDF access.
- Lookup is separated from library organization and paper reading.
- Structured match output makes confidence and source tier visible.

## What Ships

| Component | Role |
| --- | --- |
| [`zotero-attachment-lookup`](./zotero-attachment-lookup) | installable Codex App skill package |
| [`zotero-attachment-lookup/references`](./zotero-attachment-lookup/references) | bundled public reference material |
| [`zotero-attachment-lookup/scripts`](./zotero-attachment-lookup/scripts) | bundled helper scripts |
| [`zotero-attachment-lookup/test-prompts.json`](./zotero-attachment-lookup/test-prompts.json) | trigger and non-trigger examples |
| [`CHANGELOG.md`](./CHANGELOG.md) | release history |
| [`LICENSE`](./LICENSE) | license |

## Install / Use

### Codex App

- Install the skill from this repo path: `zotero-attachment-lookup`
- GitHub install target:
  - repo: `Mingdao007/zotero-attachment-lookup-skill`
  - path: `zotero-attachment-lookup`
- Restart `Codex App` after installation so the new skill is discovered.

## Workflow

```mermaid
flowchart LR
    A["Paper hint"] --> B["Local Zotero scan"]
    B --> C["Candidate scoring"]
    C --> D["Best PDF path"]
    D --> E["Structured result"]
```

## Coverage

- attachment-key, item-key, DOI, title, filename, and author lookup inputs
- local-storage-first search with optional quick-reference hints
- structured JSON output describing match type, confidence, and source tier

## Expected Result / Verification

| Check | Expected result |
| --- | --- |
| Install target | `zotero-attachment-lookup` |
| GitHub target | `Mingdao007/zotero-attachment-lookup-skill` with path `zotero-attachment-lookup` |
| Skill entrypoint | `zotero-attachment-lookup/SKILL.md` exists |
| Trigger examples | `zotero-attachment-lookup/test-prompts.json` |
| Privacy check | public package contains no private local paths or live user state |

## Trigger Examples

- `Find the local PDF for this Zotero item.`
- `Resolve this DOI to the best local Zotero attachment.`
- `Locate the attachment path before using metadata tooling.`

## Non-Trigger Examples

- `Reorganize the whole Zotero library.`
- `Debug a Zotero transport startup failure.`
- `Explain the paper after the PDF is already known.`

## Privacy Boundary

This public repository keeps the workflow generic and reusable.

- Local paths are rewritten to use host-relative defaults or environment overrides.
- The public package keeps the lookup logic but removes private companion-path assumptions.

## Repository Layout

| Path | Purpose |
| --- | --- |
| [`zotero-attachment-lookup`](./zotero-attachment-lookup) | installable Codex App skill package |
| [`zotero-attachment-lookup/references`](./zotero-attachment-lookup/references) | bundled public reference material |
| [`zotero-attachment-lookup/scripts`](./zotero-attachment-lookup/scripts) | bundled helper scripts |
| [`zotero-attachment-lookup/test-prompts.json`](./zotero-attachment-lookup/test-prompts.json) | trigger and non-trigger examples |
| [`CHANGELOG.md`](./CHANGELOG.md) | release history |
| [`LICENSE`](./LICENSE) | license |

Chinese:

- [README.zh-CN.md](./README.zh-CN.md)
