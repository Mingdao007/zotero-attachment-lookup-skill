# Zotero Attachment Lookup Skill

Portable local-first Zotero PDF lookup skill with optional quick-reference support and deterministic storage scanning.

## What Ships

- installable skill: [`zotero-attachment-lookup`](./zotero-attachment-lookup)
- bundled public references: [`zotero-attachment-lookup/references/`](./zotero-attachment-lookup/references)
- bundled helper scripts: [`zotero-attachment-lookup/scripts/`](./zotero-attachment-lookup/scripts)

## Install / Use

- `Codex App`: install the skill from this repo path `zotero-attachment-lookup`
- GitHub install target:
  - repo: `<owner>/zotero-attachment-lookup-skill`
  - path: `zotero-attachment-lookup`
- Restart `Codex App` after installation so the new skill is discovered.

## Coverage

- attachment-key, item-key, DOI, title, filename, and author lookup inputs
- local-storage-first search with optional quick-reference hints
- structured JSON output describing match type, confidence, and source tier

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

- `zotero-attachment-lookup/`: installable `Codex App` skill
- `zotero-attachment-lookup/references/`: bundled public references
- `zotero-attachment-lookup/scripts/`: bundled public scripts
- `CHANGELOG.md`: release history
- `LICENSE`: `MIT`

Chinese:

- [README.zh-CN.md](./README.zh-CN.md)
