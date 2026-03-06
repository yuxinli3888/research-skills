---
name: obsidian-vault
description: >
  Interact with the user's Obsidian vault stored at /Users/yuxinli/Documents/Vault/Research.
  Use this skill when asked to: save notes, read notes, search the vault, create research summaries,
  add paper notes, organize knowledge, link notes, or anything related to the user's Obsidian vault.
---

## Obsidian Vault Skill

The user's Obsidian vault is located at: `/Users/yuxinli/Documents/Vault/Research`

### Reading Notes

To read an existing note, use the bash tool to `cat` the file:
```bash
cat "/Users/yuxinli/Documents/Vault/Research/<subfolder>/<note-name>.md"
```

To search across all notes:
```bash
grep -r "<keyword>" "/Users/yuxinli/Documents/Vault/Research" --include="*.md" -l
```

To list all notes in the vault:
```bash
find "/Users/yuxinli/Documents/Vault/Research" -name "*.md" | sort
```

### Creating or Updating Notes

Every note should use YAML frontmatter at the top. Use this template for research paper notes:

```markdown
---
title: "<Paper Title>"
authors: ["Author One", "Author Two"]
year: <YYYY>
doi: "<DOI>"
source: "<Journal or Conference>"
tags: [research, <topic>, <subtopic>]
date-added: <YYYY-MM-DD>
status: "unread"  # unread | reading | done
---

# <Paper Title>

## Summary
<1–2 paragraph summary>

## Key Contributions
- 

## Methods
- 

## Results
- 

## My Notes
- 

## Links
- Related: [[<other note>]]
```

### Folder Structure Convention

Organize notes under these subfolders (create them if they don't exist):
- `Papers/` — individual research paper notes
- `Topics/` — topic overviews and MOCs (Maps of Content)
- `Daily/` — daily reading logs (named `YYYY-MM-DD.md`)
- `Inbox/` — quick captures to be organized later

### Saving a Paper Note

To save a new note for a research paper:
1. Determine the appropriate filename: `<Year> - <Short Title>.md` (e.g., `2024 - Attention Is All You Need.md`)
2. Place it under `Papers/`
3. Write the note using the frontmatter template above
4. Use the bash tool to write the file:

```bash
cat > "/Users/yuxinli/Documents/Vault/Research/Papers/<filename>.md" << 'EOF'
<note content>
EOF
```

Or use the file editing tools to create the note directly.

### Appending to the Daily Log

When saving papers in bulk, append a line to today's daily log:
```bash
echo "- [[Papers/<filename>]] — <one-line description>" >> "/Users/yuxinli/Documents/Vault/Research/Daily/$(date +%Y-%m-%d).md"
```

### Wikilinks

Use Obsidian-style `[[Note Name]]` wikilinks (without `.md` extension) to link between notes.

### Important

- Never delete existing files unless explicitly asked.
- Always check if a file already exists before creating it to avoid overwriting.
- Preserve the user's existing formatting and frontmatter style if editing existing notes.
