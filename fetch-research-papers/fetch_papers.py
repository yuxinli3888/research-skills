#!/usr/bin/env python3
"""
Fetch latest research papers from Scopus API.
Usage:
  python3 fetch_papers.py --query "machine learning" --count 10
  python3 fetch_papers.py --query "TITLE-ABS-KEY(deep learning)" --count 5 --sort "citedby-count"
  python3 fetch_papers.py --doi "10.1016/j.neunet.2022.01.001"

Requires: SCOPUS_API_KEY environment variable set.
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
from datetime import datetime


def _load_env_file():
    """Load a .env file from the script directory or CWD, if present."""
    search_dirs = [os.path.dirname(os.path.abspath(__file__)), os.getcwd()]
    for directory in search_dirs:
        env_path = os.path.join(directory, ".env")
        if os.path.isfile(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Strip optional leading "export "
                    if line.startswith("export "):
                        line = line[len("export "):]
                    if "=" in line:
                        key, _, value = line.partition("=")
                        value = value.strip().strip('"').strip("'")
                        os.environ.setdefault(key.strip(), value)
            break


_load_env_file()
API_KEY = os.environ.get("SCOPUS_API_KEY", "")
BASE_URL = "https://api.elsevier.com/content/search/scopus"
ABSTRACT_URL = "https://api.elsevier.com/content/abstract/doi/"

SORT_OPTIONS = {
    "newest": "date-desc",
    "oldest": "date-asc",
    "cited": "citedby-count",
    "relevance": "relevancy",
}

def search_papers(query: str, count: int = 10, sort: str = "date-desc", year_from: str = None) -> dict:
    if not API_KEY:
        print("ERROR: SCOPUS_API_KEY is not set.", file=sys.stderr)
        print("Add it to a .env file in this directory or set it as an environment variable.", file=sys.stderr)
        print("Get a free key at https://dev.elsevier.com/", file=sys.stderr)
        sys.exit(1)

    # Add date filter if specified
    if year_from:
        query = f"({query}) AND PUBYEAR > {int(year_from) - 1}"

    params = {
        "query": query,
        "count": str(count),
        "sort": sort,
        "field": "dc:title,dc:creator,prism:publicationName,prism:coverDate,prism:doi,citedby-count,dc:description,authkeywords,prism:aggregationType",
    }
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "X-ELS-APIKey": API_KEY,
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"ERROR {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

def fetch_by_doi(doi: str) -> dict:
    if not API_KEY:
        print("ERROR: SCOPUS_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    url = ABSTRACT_URL + urllib.parse.quote(doi, safe="")
    req = urllib.request.Request(url, headers={
        "X-ELS-APIKey": API_KEY,
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

def format_paper(entry: dict, index: int = None) -> str:
    title = entry.get("dc:title", "No title")
    authors = entry.get("dc:creator", "Unknown author")
    journal = entry.get("prism:publicationName", "")
    date = entry.get("prism:coverDate", "")
    doi = entry.get("prism:doi", "")
    citations = entry.get("citedby-count", "0")
    abstract = entry.get("dc:description", "")
    keywords = entry.get("authkeywords", "")
    year = date[:4] if date else ""

    prefix = f"[{index}] " if index is not None else ""
    lines = [
        f"{prefix}**{title}**",
        f"   Authors: {authors}",
    ]
    if journal:
        lines.append(f"   Journal: {journal}")
    if year:
        lines.append(f"   Year: {year}  |  Citations: {citations}")
    if doi:
        lines.append(f"   DOI: {doi}  |  URL: https://doi.org/{doi}")
    if keywords:
        lines.append(f"   Keywords: {keywords}")
    if abstract:
        lines.append(f"   Abstract: {abstract[:300]}{'...' if len(abstract) > 300 else ''}")
    return "\n".join(lines)

def format_as_obsidian(entry: dict) -> str:
    title = entry.get("dc:title", "Untitled")
    authors_raw = entry.get("dc:creator", "")
    authors = [a.strip() for a in authors_raw.split(";")] if authors_raw else []
    journal = entry.get("prism:publicationName", "")
    date = entry.get("prism:coverDate", "")
    doi = entry.get("prism:doi", "")
    citations = entry.get("citedby-count", "0")
    abstract = entry.get("dc:description", "")
    keywords_raw = entry.get("authkeywords", "")
    keywords = [k.strip().replace(" ", "-").lower() for k in keywords_raw.split("|")] if keywords_raw else []
    year = date[:4] if date else str(datetime.now().year)
    today = datetime.now().strftime("%Y-%m-%d")

    frontmatter_authors = json.dumps(authors)
    tags = ["research"] + keywords[:5]
    tags_str = json.dumps(tags)

    note = f"""---
title: "{title}"
authors: {frontmatter_authors}
year: {year}
doi: "{doi}"
source: "{journal}"
citations: {citations}
tags: {tags_str}
date-added: {today}
status: "unread"
---

# {title}

## Summary
{abstract or "_Add summary here._"}

## Key Contributions
- 

## Methods
- 

## Results
- 

## My Notes
- 

## Links
"""
    if doi:
        note += f"- [Full paper](https://doi.org/{doi})\n"
    return note

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from Scopus.")
    parser.add_argument("--query", "-q", help="Search query (Scopus query syntax or plain keywords)")
    parser.add_argument("--doi", help="Fetch a specific paper by DOI")
    parser.add_argument("--count", "-n", type=int, default=10, help="Number of results (default: 10)")
    parser.add_argument("--sort", "-s", default="newest",
                        choices=list(SORT_OPTIONS.keys()), help="Sort order (default: newest)")
    parser.add_argument("--year-from", help="Filter papers published from this year onwards")
    parser.add_argument("--obsidian", action="store_true",
                        help="Output in Obsidian note format (for the first result or with --doi)")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if args.doi:
        data = fetch_by_doi(args.doi)
        if args.as_json:
            print(json.dumps(data, indent=2))
            return
        entry = data.get("abstracts-retrieval-response", {}).get("coredata", {})
        if args.obsidian:
            entry_mapped = {
                "dc:title": entry.get("dc:title", ""),
                "dc:creator": entry.get("dc:creator", {}).get("$", "") if isinstance(entry.get("dc:creator"), dict) else entry.get("dc:creator", ""),
                "prism:publicationName": entry.get("prism:publicationName", ""),
                "prism:coverDate": entry.get("prism:coverDate", ""),
                "prism:doi": entry.get("prism:doi", ""),
                "citedby-count": entry.get("citedby-count", "0"),
                "dc:description": entry.get("dc:description", ""),
            }
            print(format_as_obsidian(entry_mapped))
        else:
            print(format_paper(entry))
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    sort_key = SORT_OPTIONS.get(args.sort, "date-desc")
    data = search_papers(args.query, args.count, sort_key, args.year_from)

    if args.as_json:
        print(json.dumps(data, indent=2))
        return

    entries = data.get("search-results", {}).get("entry", [])
    total = data.get("search-results", {}).get("opensearch:totalResults", "?")

    if not entries:
        print("No results found.")
        return

    print(f"\n📚 Scopus Search Results for: '{args.query}'")
    print(f"   Total available: {total}  |  Showing: {len(entries)}  |  Sort: {args.sort}\n")
    print("=" * 70)

    if args.obsidian and len(entries) >= 1:
        print(format_as_obsidian(entries[0]))
        return

    for i, entry in enumerate(entries, 1):
        print(format_paper(entry, i))
        print("-" * 70)

if __name__ == "__main__":
    main()
