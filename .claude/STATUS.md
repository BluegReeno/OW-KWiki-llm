# Offshore Wind Knowledge Wiki - Current Status

**Last Updated**: 2026-07-02
**Current Phase**: v2 - Go-live (content gaps closed)
**Target**: Pipeline running continuously against real newsletter issues

---

## Current Focus

**Task File**: `.claude/tasks/offshore-wind-v2.md`

### Priority Order

1. **Go-live** - Run `pipeline/run.py` for real against the AgentMail inbox, subscribe it to the offshoreWIND.biz newsletter, and monitor quality over several real issues.
2. **Nice to have** - AO1–AO10 overview page, wider `companies/`/`projects/` coverage, LinkedIn demo post, BlueWind Companion integration story, AgentMail webhooks instead of polling.

---

## What's DONE

### Phase 1: OKF bundle + pipeline (v1) — 2026-07-02
- [x] Bundle scaffold (`bundles/offshore-wind/`): `index.md`, `log.md`, `README.md`, `okf-cli.py`, 6 sections (companies, projects, tenders, technology, policy, digests)
- [x] Seeded ~36 fact-checked, cross-linked concept pages (5 parallel research agents, web-verified, cited)
- [x] `tenders` established as a first-class cross-cutting tag (ties into BlueWind Companion's origin)
- [x] Ingestion pipeline (`pipeline/`): AgentMail inbox polling + `claude -p` headless as the curator agent (Read/Write/Edit/Glob/Grep only, no Bash/network) — uses Claude Code/Max auth, not a separate Anthropic API key
- [x] Dry-run tested end-to-end against a throwaway bundle — correctly wrote a digest-only entry and declined to fabricate concept pages for fictitious test content
- [x] Zero broken cross-links, all frontmatter valid (`type` field present everywhere)

### Phase 2: v2 content gaps — 2026-07-02
- [x] Fixed AO-numbering slug mismatch (`french-ao5/6-*` → `french-ao3/4-*`, real CRE numbers) — done via Archon (`archon-feature-development`), PR #1
- [x] Added missing `tenders/french-ao1.md`, linked from Saint-Brieuc/Saint-Nazaire
- [x] Independently re-verified post-merge: 0 broken links, 0 stale slug references, frontmatter intact

### Recent Commits
| Feature | Commit | Date |
|---------|--------|------|
| OKF bundle + ingestion pipeline | `0a18a76` | 2026-07-02 |
| Brief v2 (STATUS + task file) | `89f3ffd` | 2026-07-02 |
| Tender AO numbering fix + AO1 page (PR #1, via Archon) | `5364dab` | 2026-07-02 |

---

## Architecture

```
offshoreWIND.biz newsletter → AgentMail inbox → pipeline/run.py polls unread mail
   → pipeline/wiki_agent.py shells out to `claude -p`
     (Read/Write/Edit/Glob/Grep only, cwd = bundle root)
   → updates companies/projects/tenders/technology/policy pages,
     writes digests/YYYY-MM-DD-*.md, logs to log.md

Consumption: any AI agent reads bundles/offshore-wind/ directly (plain
markdown) or via bundles/offshore-wind/okf-cli.py (index/find/read).
```

---

## Quick Commands

```bash
# Navigate/search the bundle
cd bundles/offshore-wind
python3 okf-cli.py index
python3 okf-cli.py find "<query>"
python3 okf-cli.py read <path>

# Run the ingestion pipeline
cd bundles/offshore-wind/pipeline
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in AGENTMAIL_API_KEY
python run.py           # prints inbox address on first run
```

---

## Key Files

```
bundles/offshore-wind/
├── index.md, log.md, README.md, okf-cli.py
├── companies/ projects/ tenders/ technology/ policy/ digests/   # OKF concept pages
└── pipeline/
    ├── run.py          # AgentMail polling loop
    ├── wiki_agent.py   # shells out to `claude -p`, scoped system prompt
    ├── README.md        # setup instructions
    └── .env.example
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Knowledge format | Open Knowledge Format (OKF) — markdown + YAML frontmatter |
| Ingestion transport | AgentMail (inbox API, polling) |
| Curator agent | Claude Code CLI headless (`claude -p`), Max/Pro subscription auth |
| Navigation | `okf-cli.py` (Python stdlib only, no deps) |

---

**Next Action**: Read `.claude/tasks/offshore-wind-v2.md` and start with the first unchecked task.
