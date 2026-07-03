# Offshore Wind Knowledge Wiki - Current Status

**Last Updated**: 2026-07-03
**Current Phase**: v2 - Live, persistent, and genuinely unattended (cron + OAuth token, validated against 15 real articles — 10 manual + 5 fully automated)
**Target**: Review gate before pipeline commits land unattended

---

## Current Focus

**Tracking model**: `.claude/tasks/*.md` files cover work already done (v1/v2 history below). Going forward, new discrete work items are tracked as **GitHub Issues** instead of new task files — better fit for Archon delegation (`archon-fix-github-issue` and friends expect an issue number) and for tracking outside a Claude Code session. STATUS.md stays as the "what's the current focus" snapshot.

### Priority Order

1. **[Issue #2](https://github.com/BluegReeno/OW-KWiki-llm/issues/2)** - Add a review gate (likely PR + verification agent, per the pattern from PR #1) before pipeline-authored wiki changes commit unattended. Currently: pipeline writes to the working tree, commit is manual.
2. **Nice to have** - AO1–AO10 overview page, wider `companies/`/`projects/` coverage, LinkedIn demo post, BlueWind Companion integration story.

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

### Phase 3: AgentMail → RSS pivot, real go-live — 2026-07-02
- [x] AgentMail newsletter signup's confirmation email never arrived after two attempts — pivoted to polling offshoreWIND.biz's public RSS feed instead (no account, no confirmation step)
- [x] `pipeline/poll_rss.py` written (stdlib only), `pipeline/run.py` (AgentMail) removed
- [x] Dry-run tested with an RSS-shaped fictitious article — correctly digest-only, no fabricated pages
- [x] Launched for real against the actual bundle; baselined the 10 articles already in the feed, now waiting on genuinely new ones
- [x] AgentMail MCP server connected (local scope) for ad-hoc inbox inspection — account/key kept, unused by the pipeline itself

### Phase 4: Persistent scheduling (cron) — 2026-07-02
- [x] Refactored `poll_rss.py` from a `while True` daemon into a single check-and-exit invocation (fcntl-locked against overlapping runs)
- [x] Scheduled via cron every 30 min — survives session end, Mac restarts (as long as the machine is on)
- [x] `CLAUDE_BIN` pinned to `claude`'s absolute path in `.env` since cron's minimal `PATH` doesn't include it

### Phase 5: Validated against real articles — 2026-07-03
- [x] Manually ran the curator agent against all 10 articles present in the feed at launch (previously skipped as baseline) — one by one, real content, not synthetic tests
- [x] Result: ~14 new concept pages, 8 cross-link updates, 10 digests, 0 broken links, frontmatter valid throughout
- [x] Confirmed cron is executing on schedule (poll.log) and correctly reports "no new articles" when the feed genuinely hasn't changed (verified by diffing live feed guids against stored state)
- [x] Committed as content-only (no pipeline code changed) — decided going forward: pipeline should NOT auto-commit unattended; review gate needed first ([Issue #2](https://github.com/BluegReeno/OW-KWiki-llm/issues/2))

### Phase 6: Real unattended auth fix — 2026-07-03
- [x] Diagnosed the actual root cause of unattended failures: `claude -p` has no access to the interactive session's login under cron **or** launchd (tested both — same `"Not logged in · Please run /login"` either way, so it was never a cron-vs-launchd issue)
- [x] Fix: `claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN` in `.env` (long-lived, ~1 year) — confirmed working under a minimal `env -i` shell matching cron/launchd's environment
- [x] Fixed a real bug this surfaced: `poll_rss.py` was marking failed items as "seen" — meaning a curation failure silently and permanently dropped that article. Now failed items retry on the next run.
- [x] Reverted the brief launchd detour back to cron (both work now that auth is the actual fix; cron is simpler and was the original preference)
- [x] First fully unattended, automated ingestions: 5 real articles processed with zero manual intervention (ESB/Inch Cape, JERA Nex BP/Northwester 2/Nobelwind, Bernhard Schulte Offshore, Curonian Nord/Lithuania)
- [x] Documented both failure signatures (`Not logged in` vs `401 Invalid bearer token`) in `pipeline/README.md` so a future expiry is recognizable at a glance

### Recent Commits
| Feature | Commit | Date |
|---------|--------|------|
| OKF bundle + ingestion pipeline | `0a18a76` | 2026-07-02 |
| Brief v2 (STATUS + task file) | `89f3ffd` | 2026-07-02 |
| Tender AO numbering fix + AO1 page (PR #1, via Archon) | `5364dab` | 2026-07-02 |
| AgentMail → RSS pivot | `ca311d0` | 2026-07-02 |
| One-shot refactor + cron scheduling | `a847cdb` | 2026-07-02 |
| Real README | `8922037` | 2026-07-02 |
| Ingest 10 real articles (manual validation) | `c3c4eb2` | 2026-07-03 |
| GitHub Issues tracking model, close v2 task | `b48fa27` | 2026-07-03 |
| Fix silent-drop bug + OAuth token docs | `b436828` | 2026-07-03 |
| Ingest 5 real articles (first automated runs) | `0ac4428` | 2026-07-03 |

---

## Architecture

```
https://www.offshorewind.biz/feed/ → pipeline/poll_rss.py polls every 30 min
   → pipeline/wiki_agent.py shells out to `claude -p`
     (Read/Write/Edit/Glob/Grep only, cwd = bundle root)
   → updates companies/projects/tenders/technology/policy pages,
     writes digests/YYYY-MM-DD-*.md, logs to log.md

Consumption: any AI agent (or Obsidian, as a vault) reads
bundles/offshore-wind/ directly (plain markdown) or via
bundles/offshore-wind/okf-cli.py (index/find/read).
```

---

## Quick Commands

```bash
# Navigate/search the bundle
cd bundles/offshore-wind
python3 okf-cli.py index
python3 okf-cli.py find "<query>"
python3 okf-cli.py read <path>

# Run the ingestion pipeline manually (also runs via cron every 30 min, see crontab -l)
cd bundles/offshore-wind/pipeline
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# .env needs CLAUDE_CODE_OAUTH_TOKEN (from `claude setup-token`) for unattended runs
python poll_rss.py   # single check-and-exit pass; first run baselines existing articles
```

---

## Key Files

```
bundles/offshore-wind/
├── index.md, log.md, README.md, okf-cli.py
├── companies/ projects/ tenders/ technology/ policy/ digests/   # OKF concept pages
└── pipeline/
    ├── poll_rss.py     # RSS polling loop (stdlib only)
    ├── wiki_agent.py   # shells out to `claude -p`, scoped system prompt
    ├── README.md        # setup instructions
    └── .env.example
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Knowledge format | Open Knowledge Format (OKF) — markdown + YAML frontmatter |
| Ingestion transport | Public RSS feed (`urllib` + `xml.etree`, stdlib only) |
| Curator agent | Claude Code CLI headless (`claude -p`), Max/Pro subscription auth via `CLAUDE_CODE_OAUTH_TOKEN` |
| Navigation | `okf-cli.py` (Python stdlib only, no deps) or Obsidian (open the folder as a vault) |

---

**Next Action**: See [Issue #2](https://github.com/BluegReeno/OW-KWiki-llm/issues/2) (review gate) — `gh issue list --repo BluegReeno/OW-KWiki-llm` for the full backlog.
