#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any


QUICK_REFERENCE_PATH = Path(os.environ.get("ZOTERO_QUICK_REFERENCE_PATH", str(Path.home() / ".zotero-quick-reference.md")))
ZOTERO_STORAGE_ROOT = Path(os.environ.get("ZOTERO_STORAGE_ROOT", str(Path.home() / "Zotero" / "storage")))
ITEM_KEY_RE = re.compile(r"\b[A-Z0-9]{8}\b")
STORAGE_PATH_RE = re.compile(r"storage/([A-Z0-9]{8})/([^|]+?\.pdf)\b", re.IGNORECASE)
ATTACHMENT_HINT_RE = re.compile(r"att:\s*([A-Z0-9]{8})", re.IGNORECASE)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


@dataclass
class QuickReferenceRecord:
    title: str
    item_key: str | None
    attachment_key: str | None
    local_pdf_path: str | None
    filename: str | None
    raw_line: str


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def normalize_tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def safe_json(result: dict[str, Any]) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=2))


def base_result() -> dict[str, Any]:
    return {
        "match_status": "not_found",
        "match_type": None,
        "local_pdf_path": None,
        "ft_cache_path": None,
        "attachment_key": None,
        "item_key": None,
        "filename": None,
        "title_candidate": None,
        "doi_candidate": None,
        "confidence": 0.0,
        "source_tier": "not_found",
    }


def pdf_in_dir(key: str) -> tuple[Path | None, Path | None]:
    directory = ZOTERO_STORAGE_ROOT / key
    if not directory.exists() or not directory.is_dir():
        return None, None
    pdfs = sorted(directory.glob("*.pdf"))
    pdf = pdfs[0] if pdfs else None
    ft_cache = directory / ".zotero-ft-cache"
    return pdf, ft_cache if ft_cache.exists() else None


def load_quick_reference_records() -> list[QuickReferenceRecord]:
    if not QUICK_REFERENCE_PATH.exists():
        return []
    records: list[QuickReferenceRecord] = []
    for line in QUICK_REFERENCE_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0] in {"文件", "itemKey"}:
            continue
        if set("".join(cells)) <= {"-", " "}:
            continue

        title = cells[0]
        item_key_match = ITEM_KEY_RE.search(cells[1])
        detail = " | ".join(cells[2:])
        path_match = STORAGE_PATH_RE.search(detail)
        attachment_hint = ATTACHMENT_HINT_RE.search(detail)
        local_pdf_path = None
        attachment_key = None
        filename = None
        if path_match:
            attachment_key = path_match.group(1)
            filename = path_match.group(2).strip()
            local_pdf_path = str(ZOTERO_STORAGE_ROOT / attachment_key / filename)
        elif attachment_hint:
            attachment_key = attachment_hint.group(1)
            pdf, _ = pdf_in_dir(attachment_key)
            if pdf is not None:
                local_pdf_path = str(pdf)
                filename = pdf.name

        records.append(
            QuickReferenceRecord(
                title=title,
                item_key=item_key_match.group(0) if item_key_match else None,
                attachment_key=attachment_key,
                local_pdf_path=local_pdf_path,
                filename=filename,
                raw_line=stripped,
            )
        )
    return records


def build_matched_result(
    *,
    match_type: str,
    local_pdf_path: Path | str | None,
    attachment_key: str | None = None,
    item_key: str | None = None,
    title_candidate: str | None = None,
    doi_candidate: str | None = None,
    confidence: float = 1.0,
    source_tier: str,
) -> dict[str, Any]:
    result = base_result()
    pdf_path = Path(local_pdf_path) if local_pdf_path else None
    ft_cache_path = None
    if pdf_path is not None:
        ft_cache = pdf_path.parent / ".zotero-ft-cache"
        ft_cache_path = str(ft_cache) if ft_cache.exists() else None
    result.update(
        {
            "match_status": "matched",
            "match_type": match_type,
            "local_pdf_path": str(pdf_path) if pdf_path else None,
            "ft_cache_path": ft_cache_path,
            "attachment_key": attachment_key,
            "item_key": item_key,
            "filename": pdf_path.name if pdf_path else None,
            "title_candidate": title_candidate,
            "doi_candidate": doi_candidate,
            "confidence": round(confidence, 3),
            "source_tier": source_tier,
        }
    )
    return result


def direct_key_lookup(
    *,
    attachment_key: str | None,
    item_key: str | None,
    records: list[QuickReferenceRecord],
) -> dict[str, Any] | None:
    if attachment_key:
        pdf, _ = pdf_in_dir(attachment_key)
        if pdf is not None:
            return build_matched_result(
                match_type="attachment_key_direct",
                local_pdf_path=pdf,
                attachment_key=attachment_key,
                item_key=item_key,
                confidence=1.0,
                source_tier="direct_storage",
            )

    if item_key:
        pdf, _ = pdf_in_dir(item_key)
        if pdf is not None:
            return build_matched_result(
                match_type="item_key_direct",
                local_pdf_path=pdf,
                attachment_key=item_key,
                item_key=item_key,
                confidence=0.98,
                source_tier="direct_storage",
            )
        for record in records:
            if record.item_key != item_key:
                continue
            if record.local_pdf_path:
                return build_matched_result(
                    match_type="item_key_quick_reference",
                    local_pdf_path=record.local_pdf_path,
                    attachment_key=record.attachment_key,
                    item_key=record.item_key,
                    title_candidate=record.title,
                    confidence=0.97,
                    source_tier="quick_reference",
                )
            if record.attachment_key:
                pdf, _ = pdf_in_dir(record.attachment_key)
                if pdf is not None:
                    return build_matched_result(
                        match_type="item_key_attachment_hint",
                        local_pdf_path=pdf,
                        attachment_key=record.attachment_key,
                        item_key=record.item_key,
                        title_candidate=record.title,
                        confidence=0.94,
                        source_tier="quick_reference",
                    )
    return None


def score_record(record: QuickReferenceRecord, title: str | None, author: str | None, filename: str | None) -> float:
    score = 0.0
    corpus = " ".join(filter(None, [record.title, record.filename or ""]))
    corpus_tokens = set(normalize_tokens(corpus))

    if filename:
        normalized_filename = filename.lower()
        if record.filename and normalized_filename in record.filename.lower():
            score += 1.0

    if title:
        title_tokens = [token for token in normalize_tokens(title) if len(token) > 2]
        if title_tokens:
            overlap = len(set(title_tokens) & corpus_tokens)
            score += overlap / len(set(title_tokens))

    if author:
        author_tokens = [token for token in normalize_tokens(author) if len(token) > 2]
        if author_tokens:
            overlap = len(set(author_tokens) & corpus_tokens)
            score += 0.6 * overlap / len(set(author_tokens))

    return score


def quick_reference_lookup(
    *,
    doi: str | None,
    title: str | None,
    author: str | None,
    filename: str | None,
    records: list[QuickReferenceRecord],
) -> dict[str, Any] | None:
    if doi:
        doi_lower = doi.lower()
        for record in records:
            if doi_lower in record.raw_line.lower() and record.local_pdf_path:
                return build_matched_result(
                    match_type="doi_quick_reference",
                    local_pdf_path=record.local_pdf_path,
                    attachment_key=record.attachment_key,
                    item_key=record.item_key,
                    title_candidate=record.title,
                    doi_candidate=doi,
                    confidence=0.95,
                    source_tier="quick_reference",
                )

    best: tuple[float, QuickReferenceRecord] | None = None
    for record in records:
        score = score_record(record, title=title, author=author, filename=filename)
        if score <= 0:
            continue
        if best is None or score > best[0]:
            best = (score, record)

    if best and best[0] >= 0.8 and best[1].local_pdf_path:
        score, record = best
        return build_matched_result(
            match_type="quick_reference_search",
            local_pdf_path=record.local_pdf_path,
            attachment_key=record.attachment_key,
            item_key=record.item_key,
            title_candidate=record.title,
            doi_candidate=doi,
            confidence=min(0.96, 0.7 + 0.2 * score),
            source_tier="quick_reference",
        )
    return None


def score_pdf_path(pdf_path: Path, title: str | None, author: str | None, filename: str | None) -> float:
    stem = pdf_path.stem.lower()
    stem_tokens = set(normalize_tokens(stem))
    score = 0.0

    if filename and filename.lower() in pdf_path.name.lower():
        score += 1.0

    if title:
        title_tokens = [token for token in normalize_tokens(title) if len(token) > 2]
        if title_tokens:
            overlap = len(set(title_tokens) & stem_tokens)
            score += overlap / len(set(title_tokens))

    if author:
        author_tokens = [token for token in normalize_tokens(author) if len(token) > 2]
        if author_tokens:
            overlap = len(set(author_tokens) & stem_tokens)
            score += 0.5 * overlap / len(set(author_tokens))

    return score


def storage_scan_lookup(
    *,
    doi: str | None,
    title: str | None,
    author: str | None,
    filename: str | None,
) -> dict[str, Any] | None:
    if not ZOTERO_STORAGE_ROOT.exists():
        return None
    best: tuple[float, Path] | None = None
    for pdf_path in ZOTERO_STORAGE_ROOT.rglob("*.pdf"):
        score = score_pdf_path(pdf_path, title=title, author=author, filename=filename)
        if score <= 0:
            continue
        if best is None or score > best[0]:
            best = (score, pdf_path)

    if best is None:
        return None
    score, pdf_path = best
    if score < 0.8:
        return None
    attachment_key = pdf_path.parent.name if ITEM_KEY_RE.fullmatch(pdf_path.parent.name) else None
    return build_matched_result(
        match_type="storage_scan",
        local_pdf_path=pdf_path,
        attachment_key=attachment_key,
        item_key=None,
        title_candidate=pdf_path.stem,
        doi_candidate=doi,
        confidence=min(0.93, 0.65 + 0.2 * score),
        source_tier="storage_scan",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local-first Zotero attachment lookup.")
    parser.add_argument("--doi")
    parser.add_argument("--title")
    parser.add_argument("--author")
    parser.add_argument("--attachment-key")
    parser.add_argument("--item-key")
    parser.add_argument("--filename")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records = load_quick_reference_records()

    result = direct_key_lookup(
        attachment_key=args.attachment_key,
        item_key=args.item_key,
        records=records,
    )
    if result is None:
        result = quick_reference_lookup(
            doi=args.doi,
            title=args.title,
            author=args.author,
            filename=args.filename,
            records=records,
        )
    if result is None:
        result = storage_scan_lookup(
            doi=args.doi,
            title=args.title,
            author=args.author,
            filename=args.filename,
        )
    if result is None:
        result = base_result()
        result["doi_candidate"] = args.doi

    safe_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
