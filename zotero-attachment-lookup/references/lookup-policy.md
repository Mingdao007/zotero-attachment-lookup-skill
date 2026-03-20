# Lookup policy

## Purpose

This skill resolves a paper query to the most credible local Zotero PDF path.

It is local-first:
- quick reference first
- direct attachment folder next
- storage scan after that
- Zotero MCP only as the next manual step when local lookup is insufficient

## Inputs

Supported query inputs:
- DOI
- paper title
- author keyword
- attachment key
- item key
- filename

## Search order

1. `attachment key`
2. `item key` with quick-reference mapping
3. DOI or exact title in quick reference
4. filename scan under `~/Zotero/storage`
5. title-token scan under `~/Zotero/storage`
6. author-token scan under `~/Zotero/storage`

## Output fields

- `match_status`: `matched` or `not_found`
- `match_type`: direct lookup method used
- `local_pdf_path`: absolute path to the PDF when matched
- `ft_cache_path`: absolute path to `.zotero-ft-cache` when present
- `attachment_key`: best known attachment key
- `item_key`: best known Zotero item key
- `filename`: matched PDF filename
- `title_candidate`: best title candidate from quick reference or filename
- `doi_candidate`: DOI if supplied or locally inferred
- `confidence`: 0.0 to 1.0
- `source_tier`: `direct_storage`, `quick_reference`, `storage_scan`, or `not_found`

## Routing boundary

Do not extend this skill to:
- Zotero library organization
- Zotero MCP debugging
- PDF explanation
- literature review synthesis

Those remain owned by other skills.
