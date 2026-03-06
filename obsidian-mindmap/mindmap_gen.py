#!/usr/bin/env python3
"""
Generate a Mermaid mindmap scaffold for Obsidian notes.
Usage:
  python3 mindmap_gen.py --topic "Transformer Architecture"
  python3 mindmap_gen.py --paper "Attention Is All You Need" --keywords "attention,transformer,NLP,encoder,decoder"
  python3 mindmap_gen.py --topic "Federated Learning" --nodes "Privacy,Communication,Model Aggregation,Security" --save

Outputs a ready-to-paste Obsidian note with an embedded Mermaid mindmap.
"""
import argparse
import sys
import os
import re
from datetime import datetime


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\-]", "-", text.strip().lower()).strip("-")


def clean_node(label: str) -> str:
    """Escape Mermaid special characters in node labels."""
    return label.strip().replace("(", "[").replace(")", "]").replace('"', "'")


def generate_topic_mindmap(topic: str, nodes: list[str]) -> str:
    root = clean_node(topic)
    indent = "    "
    branches = ""
    for node in nodes:
        node_label = clean_node(node)
        branches += f"{indent}{node_label}\n"

    return f"""```mermaid
mindmap
  root(({root}))
{branches}```"""


def generate_paper_mindmap(title: str, authors: str, year: str, keywords: list[str],
                            contributions: list[str] = None, methods: list[str] = None) -> str:
    root = clean_node(title[:40] + ("..." if len(title) > 40 else ""))
    kw_block = "\n".join(f"      {clean_node(k)}" for k in keywords[:8])
    contrib_block = "\n".join(f"      {clean_node(c)}" for c in (contributions or ["To be added"]))
    method_block = "\n".join(f"      {clean_node(m)}" for m in (methods or ["To be added"]))

    author_label = clean_node(authors[:50]) if authors else "Unknown"
    year_label = year or str(datetime.now().year)

    return f"""```mermaid
mindmap
  root(({root}))
    Publication
      {author_label}
      {year_label}
    Key Concepts
{kw_block}
    Contributions
{contrib_block}
    Methodology
{method_block}
    My Thoughts
      Questions
      Applications
      Connections
```"""


def build_note(title: str, mermaid_block: str, note_type: str = "topic") -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    tags = json_list(["mindmap", note_type, "diagram"])

    return f"""---
title: "{title} - Mind Map"
tags: {tags}
date-created: {today}
type: mindmap
---

# 🧠 {title}

## Concept Map

{mermaid_block}

## Notes

_Add your thoughts, connections, and observations here._

## Related Notes

- 

"""


def json_list(items: list[str]) -> str:
    return "[" + ", ".join(f'"{x}"' for x in items) + "]"


def main():
    parser = argparse.ArgumentParser(description="Generate Mermaid mindmap notes for Obsidian.")
    parser.add_argument("--topic", "-t", help="Topic name for a general mindmap")
    parser.add_argument("--paper", "-p", help="Paper title for a paper analysis mindmap")
    parser.add_argument("--authors", default="", help="Paper authors (comma-separated)")
    parser.add_argument("--year", default="", help="Publication year")
    parser.add_argument("--keywords", "-k", default="",
                        help="Comma-separated keywords or subtopics")
    parser.add_argument("--contributions", "-c", default="",
                        help="Comma-separated key contributions (for paper maps)")
    parser.add_argument("--methods", "-m", default="",
                        help="Comma-separated methods (for paper maps)")
    parser.add_argument("--save", "-s", action="store_true",
                        help="Save the note directly to the Obsidian vault")
    parser.add_argument("--vault", default="/Users/yuxinli/Documents/Vault/Research",
                        help="Path to Obsidian vault")

    args = parser.parse_args()

    if not args.topic and not args.paper:
        parser.print_help()
        sys.exit(1)

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    contributions = [c.strip() for c in args.contributions.split(",") if c.strip()]
    methods = [m.strip() for m in args.methods.split(",") if m.strip()]

    if args.paper:
        title = args.paper
        if not keywords:
            keywords = ["Methodology", "Results", "Limitations", "Impact"]
        mermaid = generate_paper_mindmap(title, args.authors, args.year, keywords, contributions, methods)
        note_type = "paper"
    else:
        title = args.topic
        if not keywords:
            keywords = ["Overview", "Applications", "Challenges", "Future Work"]
        mermaid = generate_topic_mindmap(title, keywords)
        note_type = "topic"

    note = build_note(title, mermaid, note_type)

    if args.save:
        folder = os.path.join(args.vault, "Topics" if note_type == "topic" else "Papers")
        os.makedirs(folder, exist_ok=True)
        year_prefix = f"{args.year} - " if args.year else ""
        filename = f"{year_prefix}MindMap - {title[:50]}.md"
        filepath = os.path.join(folder, filename)

        if os.path.exists(filepath):
            print(f"⚠️  File already exists: {filepath}", file=sys.stderr)
            print(note)
            sys.exit(0)

        with open(filepath, "w") as f:
            f.write(note)
        print(f"✅ Saved mindmap to: {filepath}")
    else:
        print(note)


if __name__ == "__main__":
    main()
