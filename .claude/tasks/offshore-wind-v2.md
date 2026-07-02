# Feature: Offshore Wind Wiki v2 — go-live + content gaps

## Goal
Get the ingestion pipeline running against real offshoreWIND.biz newsletter issues, and close the content gaps the seed-content agents flagged, so the bundle is a trustworthy day-to-day reference.

## Context
- **Related Files**: `bundles/offshore-wind/**`, especially `pipeline/run.py`, `pipeline/wiki_agent.py`, `tenders/*.md`
- v1 (bundle scaffold + seed content + pipeline) shipped in commit `0a18a76` — see `.claude/STATUS.md` for what's already done.
- User has an AgentMail account and API key already (stored in `bundles/offshore-wind/pipeline/.env`, gitignored).

## Tasks

### Go-live
- [ ] `pip install -r requirements.txt` in a venv under `pipeline/`
- [ ] Confirm `claude` CLI is logged in (it should be — same login as this session)
- [ ] Run `python run.py` once; capture the printed AgentMail inbox address
- [ ] Subscribe that address to the offshoreWIND.biz daily newsletter (signup form on offshorewind.biz)
- [ ] Keep `run.py` running continuously (tmux/nohup) for at least a few real newsletter issues
- [ ] After each digested issue, `git diff` the bundle and read the new/changed pages — check for hallucinated facts, wrong cross-links, or duplicate concepts before trusting the page long-term
- [ ] Tune `wiki_agent.SYSTEM_PROMPT` if a recurring quality problem shows up (e.g. over-eager page creation, missed cross-links)

### Content gaps
- [ ] **Fix the AO-numbering slug mismatch**: `tenders/french-ao5-dunkerque.md` is actually about AO3 (Dunkerque), and `tenders/french-ao6-centre-manche.md` is actually AO4 (Centre Manche 1) — the research agent documented this correction inside the files but kept the originally-assigned slugs to avoid breaking cross-links written by other agents in the same parallel run. Decide: rename to accurate slugs (`french-ao3-dunkerque.md`, `french-ao4-centre-manche.md`) and grep-fix every incoming link across the bundle, or leave as-is with the in-file correction note. Recommend renaming — the mismatch will confuse the ingestion pipeline agent later when new newsletter issues reference "AO3" or "AO5" by their real numbers.
- [ ] **Add the missing AO1 tender page** — `projects/saint-brieuc.md` and `projects/saint-nazaire.md` both tag `tenders` and reference France's first tender round (AO1), but no `tenders/french-ao1.md` exists yet. Add it, and link both projects to it.
- [ ] Consider one `policy/` or `tenders/` overview page clarifying the full French AO1–AO10 history in one place — multiple sub-agents got tripped up by this numbering during v1; a single canonical reference reduces the chance the pipeline agent repeats the confusion.
- [ ] Widen `companies/`/`projects/` coverage if there's appetite — e.g. TotalEnergies, Shell, BP offshore wind arms; more projects (Hornsea 3, Baltic Eagle, South Fork Wind, He Dreiht, etc.). Not required for v2 completion — do only if time allows.

### Validation
- [ ] Re-run the broken-link scanner (python script used in v1, see session history or rewrite: scan all `.md` for `](/…\.md)` links and check targets exist)
- [ ] `python3 okf-cli.py find "AO1"` / similar spot checks after adding new tender content

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
- **Completed**: (fill when done)
- **Commit**: (link to commit when done)
