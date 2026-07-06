---
name: zotero-attachment-lookup
description: Locate the most credible local Zotero PDF by checking local attachment paths first and using Zotero MCP only as a fallback for unresolved metadata or missing files. Use when the user asks to find a paper's local PDF, resolve a Zotero attachment path, or read a paper body from local Zotero storage before falling back to Zotero MCP.
---

# Zotero attachment lookup

## Mission

Resolve a paper or attachment to the best local Zotero PDF path with a deterministic local-first workflow.

This skill owns lookup only.
It does not reorganize the Zotero library, explain paper contents, or write review deliverables.

## Trigger boundary

Use this skill when the user asks things like:
- `帮我在 Zotero 里找这篇 paper 的本地 PDF`
- `先本地后 MCP 找 Zotero 附件`
- `这个 DOI 对应的本地 PDF 在哪里`
- `帮我定位 attachment path`

Do not use this skill for:
- cleaning or reorganizing the Zotero library
- fixing Zotero MCP transport or startup
- explaining a paper section after the PDF is already known
- literature review synthesis or deck writing

Route nearby tasks as follows:
- library maintenance: `zotero-library-organizer`
- MCP transport/startup failure: use active Zotero integration diagnostics;
  recover dormant repair playbooks only by exact slash/name request
- explanation or paper reading: `explain`
- literature review workflow: `literature-review-workflow`

## Default workflow

1. Read the local helper reference first:

```bash
python3 "$CODEX_HOME/skills/zotero-attachment-lookup/scripts/zotero_attachment_lookup.py" --title "<paper title>"
```

The script checks these defaults:
- `$ZOTERO_QUICK_REFERENCE_PATH` when set, otherwise `$HOME/.zotero-quick-reference.md`
- `$ZOTERO_STORAGE_ROOT` when set, otherwise `$HOME/Zotero/storage`

2. Prefer direct local keys when available:
- if the user gives `attachment key`, try `~/Zotero/storage/<key>/` first
- if the user gives `item key`, check quick reference mappings and then try the mapped local path

3. If no direct key works, search local storage in this order:
- DOI
- exact or near-exact title
- filename
- author keyword

4. When a local PDF is found:
- return the local PDF path
- return sibling `.zotero-ft-cache` path when present
- include the best available attachment key, item key, filename, title candidate, and confidence

5. Only fall back conceptually to Zotero MCP when:
- local storage did not produce a credible hit
- or the user explicitly needs collection, note, annotation, or parent-child metadata

This v1 skill does not call Zotero MCP directly.
It reports when MCP is the next step.

## CLI interface

Use the bundled script:

```bash
python3 "$CODEX_HOME/skills/zotero-attachment-lookup/scripts/zotero_attachment_lookup.py" \
  [--doi "<doi>"] \
  [--title "<title>"] \
  [--author "<author>"] \
  [--attachment-key "<key>"] \
  [--item-key "<key>"] \
  [--filename "<filename>"]
```

The script returns JSON with these fixed fields:
- `match_status`
- `match_type`
- `local_pdf_path`
- `ft_cache_path`
- `attachment_key`
- `item_key`
- `filename`
- `title_candidate`
- `doi_candidate`
- `confidence`
- `source_tier`

## Output contract

Interpret output tiers as:
- `direct_storage`: direct key or direct path style hit from local Zotero storage
- `quick_reference`: match driven by the local quick reference file
- `storage_scan`: match found by scanning local PDF filenames under Zotero storage
- `not_found`: no credible local match

Return `match_status` as:
- `matched`
- `not_found`

## Failure handling

- If quick reference is missing, continue with storage scan.
- If storage root is missing, return `not_found` without guessing.
- If multiple local hits are too close to distinguish, return the top local hit only when confidence is still credible; otherwise return `not_found`.
- If local lookup fails but the user clearly needs metadata, say that Zotero MCP is the next step rather than fabricating metadata.

## Resources

- `scripts/zotero_attachment_lookup.py`: deterministic local-first lookup entrypoint
- `references/lookup-policy.md`: lookup order, examples, and routing boundaries


## Validation And Checkpoints

- Before final handoff, validate the requested artifact or decision against this skill's output contract and report the verification result explicitly.
- Before any local mutation, pass the recoverability gate: create a rollback point when the change is reversible, and request confirmation when backup cannot cover the risk.
- Use an explicit checkpoint when required input is missing, tool evidence conflicts, or repeated attempts fail; wait for approval or route to the named owner instead of guessing.
- For multi-session work, update a progress or HANDOFF artifact with current state, verified result, and next executable step.
