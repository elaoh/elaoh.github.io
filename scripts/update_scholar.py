#!/usr/bin/env python3
"""Synchronize Enrico Laoh's Google Scholar publications via SerpAPI.

Requires only Python's standard library and SERPAPI_API_KEY in the environment.
An API failure never overwrites previously saved publication data.
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SCHOLAR_ID = "DoJQbfoAAAAJ"
PAGE_SIZE = 100
MAX_PAGES = 10  # Up to 1000 publications; increase if needed.
OUTFILE = Path(__file__).resolve().parents[1] / "_data" / "scholar_publications.json"
PROFILE_URL = "https://scholar.google.com/citations?" + urlencode({"user": SCHOLAR_ID, "hl": "en"})


def fetch_page(api_key, start):
    params = {
        "engine": "google_scholar_author",
        "author_id": SCHOLAR_ID,
        "hl": "en",
        "sort": "pubdate",
        "num": PAGE_SIZE,
        "start": start,
        "api_key": api_key,
    }
    url = "https://serpapi.com/search.json?" + urlencode(params)
    req = Request(url, headers={"User-Agent": "AcademicPages-Scholar-Sync/1.0"})
    for attempt in range(3):
        try:
            with urlopen(req, timeout=60) as response:
                payload = json.load(response)
            if not isinstance(payload, dict):
                raise RuntimeError("Unexpected JSON response from SerpAPI")
            if payload.get("error"):
                raise RuntimeError("SerpAPI error: " + str(payload["error"]))
            if "articles" not in payload:
                raise RuntimeError("SerpAPI returned no 'articles' key; original data retained")
            return payload["articles"]
        except HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise RuntimeError(f"SerpAPI request failed (HTTP {exc.code})") from exc
        except (TimeoutError, URLError) as exc:
            if attempt == 2:
                raise RuntimeError("Cannot reach SerpAPI") from exc
        time.sleep(2 ** attempt)
    raise RuntimeError("SerpAPI retry limit exceeded")


def normalize_year(article):
    raw = str(article.get("year") or "").strip()
    year_match = re.search(r"\b(?:19|20)\d{2}\b", raw)
    if year_match:
        return year_match.group(0)
    venue = str(article.get("publication") or "")
    matches = re.findall(r"\b(?:19|20)\d{2}\b", venue)
    return matches[-1] if matches else "Undated"


def normalize_article(article):
    title = str(article.get("title") or "").strip()
    if not title:
        return None
    citation_id = str(article.get("citation_id") or "").strip()
    link = str(article.get("link") or "").strip()
    if not link and citation_id:
        link = "https://scholar.google.com/citations?" + urlencode({
            "view_op": "view_citation", "hl": "en", "user": SCHOLAR_ID,
            "citation_for_view": citation_id,
        })
    citations_data = article.get("cited_by") or {}
    if not isinstance(citations_data, dict):
        citations_data = {}
    try:
        citations = int(str(citations_data.get("value") or "0").replace(",", ""))
    except ValueError:
        citations = 0
    return {
        "title": title,
        "authors": str(article.get("authors") or "").strip(),
        "venue": str(article.get("publication") or "").strip(),
        "year": normalize_year(article),
        "url": link if link.startswith("https://") else PROFILE_URL,
        "citation_id": citation_id,
        "citations": citations,
        "cited_by_url": str(citations_data.get("link") or ""),
    }


def main():
    key = os.environ.get("SERPAPI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing SERPAPI_API_KEY environment variable / GitHub Actions secret")

    results = []
    ids = set()
    for page in range(MAX_PAGES):
        articles = fetch_page(key, page * PAGE_SIZE)
        if not isinstance(articles, list):
            raise RuntimeError("Unexpected SerpAPI 'articles' data; original data retained")
        for article in articles:
            if not isinstance(article, dict):
                continue
            parsed = normalize_article(article)
            if parsed is None:
                continue
            identity = parsed["citation_id"] or (parsed["title"].casefold(), parsed["year"])
            if identity not in ids:
                ids.add(identity)
                results.append(parsed)
        print(f"Page {page + 1}: {len(articles)} article(s); {len(results)} unique total")
        if len(articles) < PAGE_SIZE:
            break

    if not results:
        raise RuntimeError("No publications retrieved; refusing to replace previous data")

    # Stable sort: descending year while keeping Google's newest-first order within years.
    results.sort(
        key=lambda paper: int(paper["year"]) if paper["year"].isdigit() else -1,
        reverse=True,
    )

    record = {
        "scholar_id": SCHOLAR_ID,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "publications": results,
    }
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    staged = OUTFILE.with_suffix(".json.tmp")
    staged.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    staged.replace(OUTFILE)
    print(f"Saved {len(results)} publications to {OUTFILE}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("Scholar sync failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
