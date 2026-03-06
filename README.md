# 🔬 Research Skills

A collection of [GitHub Copilot CLI agent skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-skills) that supercharge your research workflow — fetching papers from Scopus, saving notes to Obsidian, and generating mind maps automatically.

---

## Skills

### 1. `fetch-research-papers`

Searches the **Scopus API** for the latest research papers and returns structured results. Can output notes ready to paste directly into Obsidian.

**Usage examples:**
```bash
# Search by topic (newest first)
python3 fetch-research-papers/fetch_papers.py --query "prescribed-time control" --count 10 --sort newest

# Filter by year
python3 fetch-research-papers/fetch_papers.py --query "robotic arm tracking" --count 5 --year-from 2023

# Advanced Scopus query syntax
python3 fetch-research-papers/fetch_papers.py --query "TITLE-ABS-KEY(sliding mode) AND PUBYEAR > 2023"

# Fetch a specific paper by DOI
python3 fetch-research-papers/fetch_papers.py --doi "10.1109/CAC59555.2023.10451655"

# Output as an Obsidian-ready note
python3 fetch-research-papers/fetch_papers.py --doi "10.1080/00207721.2024.2444683" --obsidian
```

**Sort options:** `newest` · `oldest` · `cited` · `relevance`

**Requires:** `SCOPUS_API_KEY` environment variable. Get a free key at [dev.elsevier.com](https://dev.elsevier.com/).

---

### 2. `obsidian-vault`

Reads, creates, and organizes notes in your Obsidian vault at the path set in `OBSIDIAN_VAULT_PATH`. Copilot uses this skill to save paper notes with YAML frontmatter, search existing notes, and maintain a consistent folder structure.

**Vault folder structure:**
```
${OBSIDIAN_VAULT_PATH}/
├── Papers/       # Individual research paper notes
├── Topics/       # Topic overviews and Maps of Content
├── Daily/        # Daily reading logs (YYYY-MM-DD.md)
└── Inbox/        # Quick captures to organize later
```

**Example prompts in Copilot:**
```
Save this paper to my Obsidian vault
Search my vault for notes about sliding mode control
Create a new paper note for DOI 10.xxxx/xxxxx
```

---

### 3. `obsidian-mindmap`

Generates **Mermaid mindmap diagrams** embedded in Obsidian notes — rendered natively in Obsidian's Reading View (no plugins needed).

**Usage examples:**
```bash
# Topic overview mindmap
python3 obsidian-mindmap/mindmap_gen.py \
  --topic "Prescribed-Time Control" \
  --keywords "Sliding Mode,Fuzzy Control,Adaptive,Robustness,Multi-Agent"

# Paper analysis mindmap
python3 obsidian-mindmap/mindmap_gen.py \
  --paper "Attention Is All You Need" \
  --authors "Vaswani et al." --year 2017 \
  --keywords "Self-Attention,Encoder,Decoder,Positional Encoding" \
  --contributions "Eliminates recurrence,Parallelizable training"

# Save directly to the vault
python3 obsidian-mindmap/mindmap_gen.py \
  --topic "Federated Learning" \
  --keywords "Privacy,Aggregation,Non-IID,Security" \
  --save
```

**Example prompt in Copilot:**
```
Create a mind map for my papers on robotic arm control and save it to Obsidian
```

---

## Setup

**1. Clone or open this folder in Copilot CLI:**
```bash
cd "Research Skills"
copilot
```

**2. Set your Scopus API key:**
```bash
export SCOPUS_API_KEY="your-key-here"
# or source the .env file:
source .env
```

**3. Set your Obsidian vault path:**
```powershell
$env:OBSIDIAN_VAULT_PATH = "C:\Users\<user>\Documents\Obsidian\Research"
```

```bash
export OBSIDIAN_VAULT_PATH="$HOME/Documents/Vault/Research"
```

**4. Register the skills folder (once per Copilot session):**
```
/skills add "<path-to-this-repo>"
/skills reload
```

**5. Verify skills are loaded:**
```
/skills list
```

---

## Typical Workflow

```
1. Ask Copilot: "Find me the 10 latest papers on prescribed-time control from 2024"
   → fetch-research-papers fetches from Scopus

2. Ask Copilot: "Save these papers to my Obsidian vault"
   → obsidian-vault creates structured notes in Papers/

3. Ask Copilot: "Create a mind map connecting these papers"
   → obsidian-mindmap generates a Mermaid diagram in Topics/
```
