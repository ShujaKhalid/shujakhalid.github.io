#!/usr/bin/env python3
"""Fetch citation metrics from Google Scholar and write data/scholar.json.

Run daily by .github/workflows/update-citations.yml. If scraping fails
(Scholar frequently blocks automated requests), the existing JSON is left
untouched and the script exits 0 so the workflow does not fail.
"""
import json
import os
import sys
from datetime import datetime, timezone

AUTHOR_ID = "1Fa69AYAAAAJ"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "scholar.json")


def main() -> int:
    try:
        from scholarly import scholarly
    except ImportError:
        print("scholarly not installed", file=sys.stderr)
        return 0

    try:
        author = scholarly.search_author_id(AUTHOR_ID)
        author = scholarly.fill(author, sections=["indices", "counts", "publications"])
    except Exception as exc:  # network / blocked / parse errors
        print(f"scholar fetch failed, keeping existing data: {exc}", file=sys.stderr)
        return 0

    papers = {}
    for pub in author.get("publications", []):
        title = (pub.get("bib", {}) or {}).get("title", "").strip()
        if title:
            papers[title] = int(pub.get("num_citations", 0) or 0)

    data = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "citations": author.get("citedby"),
        "hindex": author.get("hindex"),
        "i10index": author.get("i10index"),
        "papers": papers,
    }

    # Sanity: don't overwrite good data with an empty/blocked scrape.
    if not data["citations"] or not papers:
        print("scrape returned empty metrics, keeping existing data", file=sys.stderr)
        return 0

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {OUT}: {data['citations']} citations, h-index {data['hindex']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
