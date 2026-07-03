# Feature: Offshore Wind Wiki v2 — go-live + content gaps

## Goal
Get the ingestion pipeline running against real offshoreWIND.biz newsletter issues, and close the content gaps the seed-content agents flagged, so the bundle is a trustworthy day-to-day reference.

## Context
- **Related Files**: `bundles/offshore-wind/**`, especially `pipeline/run.py`, `pipeline/wiki_agent.py`, `tenders/*.md`
- v1 (bundle scaffold + seed content + pipeline) shipped in commit `0a18a76` — see `.claude/STATUS.md` for what's already done.
- User has an AgentMail account and API key already (stored in `bundles/offshore-wind/pipeline/.env`, gitignored).

## Tasks

### Go-live
- [x] `pip install -r requirements.txt` in a venv under `pipeline/` ✓ 2026-07-02
- [x] Confirm `claude` CLI is logged in ✓ 2026-07-02
- [x] ~~Run `python run.py` once; capture the printed AgentMail inbox address~~ — **pivoted**: the offshoreWIND.biz newsletter confirmation email never arrived after two signup attempts. Switched ingestion to the public RSS feed (`https://www.offshorewind.biz/feed/`) instead — no account, no confirmation step. `run.py` (AgentMail) removed, replaced by `pipeline/poll_rss.py` (stdlib only). See `pipeline/README.md` § "Why not AgentMail / the newsletter?". ✓ 2026-07-02
- [x] `python poll_rss.py` launched for real against the actual bundle — first run baselined the 10 articles currently in the feed as already-seen (not processed), so it starts clean and only ingests genuinely new articles going forward. ✓ 2026-07-02
- [x] Refactored `poll_rss.py` from a long-running daemon (`while True` + internal `sleep`) into a single check-and-exit script, and scheduled it via **cron** every 30 minutes instead of a supervised background process (tmux/launchd) — simpler, no process to babysit, `.rss_poll.lock` (fcntl flock) guards against overlapping runs. `CLAUDE_BIN` set to `claude`'s absolute path in `.env` since cron's `PATH` doesn't include it. See `pipeline/README.md` § "Running it periodically (cron)". ✓ 2026-07-02
- [ ] After each new article gets digested, `git diff` the bundle and read the new/changed pages — check for hallucinated facts, wrong cross-links, or duplicate concepts before trusting the page long-term
- [ ] Tune `wiki_agent.SYSTEM_PROMPT` if a recurring quality problem shows up (e.g. over-eager page creation, missed cross-links)

### Content gaps
- [x] **Fix the AO-numbering slug mismatch** — renamed to `french-ao3-dunkerque.md` / `french-ao4-centre-manche.md`, all incoming links fixed across the bundle. Done via Archon (`archon-feature-development`, PR #1, merged as `5364dab`). ✓ 2026-07-02
- [x] **Add the missing AO1 tender page** — `tenders/french-ao1.md` created (France's first offshore wind tender, July 2011, ~1,928 MW across four zones), linked from `saint-brieuc.md` and `saint-nazaire.md`. Done via Archon, same PR. ✓ 2026-07-02
- [ ] Consider one `policy/` or `tenders/` overview page clarifying the full French AO1–AO10 history in one place — multiple sub-agents got tripped up by this numbering during v1; a single canonical reference reduces the chance the pipeline agent repeats the confusion. (Not done — optional, still open.)
- [ ] Widen `companies/`/`projects/` coverage if there's appetite — e.g. TotalEnergies, Shell, BP offshore wind arms; more projects (Hornsea 3, Baltic Eagle, South Fork Wind, He Dreiht, etc.). Not required for v2 completion — do only if time allows.

### Validation
- [x] Re-ran the broken-link scanner against the PR branch before merge: 0 broken links, 0 stray references to the old slugs, `type:` present on all concept files. ✓ 2026-07-02
- [x] `python3 okf-cli.py find "AO1"` confirms the new page is indexed and searchable. ✓ 2026-07-02

## Files to Create/Modify

| File | Action | Description |
|------|--------|--------------|
| `bundles/offshore-wind/tenders/french-ao1.md` | Create | Missing AO1 round, linked from Saint-Brieuc/Saint-Nazaire |
| `bundles/offshore-wind/tenders/french-ao5-dunkerque.md` → `french-ao3-dunkerque.md` | Rename + fix links | Correct AO numbering |
| `bundles/offshore-wind/tenders/french-ao6-centre-manche.md` → `french-ao4-centre-manche.md` | Rename + fix links | Correct AO numbering |
| `bundles/offshore-wind/pipeline/wiki_agent.py` | Modify (maybe) | Only if go-live surfaces a recurring quality issue |

## Notes
- Pipeline auth: `claude -p` headless mode, Claude Code/Max subscription login — no separate `ANTHROPIC_API_KEY` needed (see `pipeline/README.md`).
- Safety boundary for the pipeline agent: tools restricted to `Read,Write,Edit,Glob,Grep`, `--permission-mode bypassPermissions` — no hard directory jail, relies on the system prompt. Worth keeping an eye on `git diff` scope (should never touch anything outside `bundles/offshore-wind/`).
- LinkedIn demo post and BlueWind Companion integration were explicitly deferred out of this iteration (user chose go-live + content gaps as the v2 priority) — pick those up as v3 if/when relevant.

## Completion
- **Started**: 2026-07-02
- **Completed**: 2026-07-03 — content gaps (via Archon), AgentMail → RSS pivot, cron-based persistent scheduling, and validation against 10 real articles all done.
- **Commit**: `5364dab` (PR #1), `ca311d0` (AgentMail → RSS pivot), `a847cdb` (cron refactor), `c3c4eb2` (real-article validation)
- **Superseded by**: this v2 task file is done; new work items are tracked as GitHub Issues from here on (see `.claude/STATUS.md`), starting with [Issue #2](https://github.com/BluegReeno/OW-KWiki-llm/issues/2) (review gate before unattended commits).
