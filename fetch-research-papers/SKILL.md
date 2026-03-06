---
name: fetch-research-papers
description: >
  Fetch and retrieve the latest research papers from Scopus. Use this skill when asked to:
  find recent papers, search for research, get papers on a topic, fetch paper details by DOI,
  summarize new research, discover what's new in a field, or save papers to Obsidian.
---

## Fetch Research Papers Skill

This skill uses the **Scopus API** (Elsevier) to search for and retrieve research papers.

### Prerequisites

- Environment variable `SCOPUS_API_KEY` must be set.
- Python 3 must be available.
- The helper script is at: `~/.copilot/skills/fetch-research-papers/fetch_papers.py`

If `SCOPUS_API_KEY` is not set, remind the user to run:
```bash
export SCOPUS_API_KEY="your-key-here"
```
Get a free API key at: https://dev.elsevier.com/

---

### Searching for Papers

Use the script to search for papers:

```bash
python3 ~/.copilot/skills/fetch-research-papers/fetch_papers.py \
  --query "<topic or keywords>" \
  --count 10 \
  --sort newest
```

**Sort options:**
- `newest` — most recently published (default)
- `cited` — most cited
- `relevance` — best keyword match
- `oldest` — oldest first

**Filter by year:**
```bash
python3 ~/.copilot/skills/fetch-research-papers/fetch_papers.py \
  --query "<topic>" --count 10 --sort newest --year-from 2023
```

**Advanced Scopus query syntax** (more precise):
```bash
# Search in title, abstract, keywords
python3 ... --query "TITLE-ABS-KEY(transformer architecture)"

# Specific journal
python3 ... --query "SOURCE(Nature) AND TITLE-ABS-KEY(climate change)"

# Specific author
python3 ... --query "AUTH(Hinton, Geoffrey)"

# Publication year range
python3 ... --query "TITLE-ABS-KEY(BERT) AND PUBYEAR > 2022"
```

---

### Fetch a Single Paper by DOI

```bash
python3 ~/.copilot/skills/fetch-research-papers/fetch_papers.py \
  --doi "10.1016/j.neunet.2022.01.001"
```

---

### Saving a Paper to Obsidian

To fetch a paper and get it formatted as an Obsidian note:

```bash
python3 ~/.copilot/skills/fetch-research-papers/fetch_papers.py \
  --doi "<DOI>" --obsidian
```

Then save the output to the vault:
```bash
python3 ~/.copilot/skills/fetch-research-papers/fetch_papers.py \
  --doi "<DOI>" --obsidian > "/Users/yuxinli/Documents/Vault/Research/Papers/<Year> - <Short Title>.md"
```

You can also combine this with the `obsidian-vault` skill to organize and save notes intelligently.

---

### Typical Workflow

When the user asks "find me the latest papers on X":

1. Run the fetch script with relevant keywords
2. Present the results clearly — title, authors, year, journal, DOI, abstract snippet
3. Ask if the user wants any of them saved to their Obsidian vault
4. If yes, use `--obsidian` flag and save to `~/Documents/Vault/Research/Papers/`

When the user asks "find papers and save them to Obsidian":

1. Fetch papers using the script
2. For each selected paper, generate the Obsidian note with `--obsidian`
3. Save to `/Users/yuxinli/Documents/Vault/Research/Papers/<Year> - <Short Title>.md`
4. Optionally append a line to today's daily log in the vault

---

### Rate Limits

The free Scopus API key allows:
- 20,000 requests/week for search
- 5,000 requests/week for abstract retrieval
- Results limited to 25 per query for non-institutional access

Keep `--count` at 10–25 for best results.
