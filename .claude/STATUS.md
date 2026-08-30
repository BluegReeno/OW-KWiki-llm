# STATUS — Offshore Wind Knowledge Wiki

Last updated: 2026-08-30
State: **live** — the cron pipeline runs unattended and its output is committed again as of
2026-08-30.

> History lives in [`STATUS-ARCHIVE.md`](./STATUS-ARCHIVE.md), verbatim. Nothing below repeats it.

## Current Focus

v2 is live: the OKF bundle plus an unattended pipeline that polls offshoreWIND.biz's public RSS
feed and curates entries through `claude -p`, scheduled by cron (20:00 local, fcntl-locked against
overlapping runs). Validated against 15 real articles — 10 manual, 5 fully automatic.

**The pipeline never stopped, but for eight weeks none of its output was in git.** Measured
2026-08-30: the cron entry is live (`0 20 * * *`, `pipeline/poll_rss.py`), `poll.log` shows clean
runs, and `log.md` carried entries up to **2026-08-28** while the last commit was 2026-07-03 — 38
modified and 291 untracked files under `bundles/`, digests grown from 15 tracked to 163 on disk.
That backlog is now committed: the wiki has a backup and a history again.

**It was committed as a batch, unreviewed.** 291 files is past the point where a per-file read is
realistic, which is exactly the gap `#2` exists to close. Treat the content between 2026-07-03 and
2026-08-30 as pipeline output that no human has checked.

## In Progress

- [ ] Nothing.

## Backlog

- [ ] [#2](https://github.com/BluegReeno/OW-KWiki-llm/issues/2) — add a review gate before pipeline
      commits land unattended. Likely a PR plus a verification agent, following the PR #1 pattern.
      This is the one thing standing between "unattended" and "trusted".
- [ ] **Decide how the pipeline's output gets committed from now on.** Committing it by hand in
      batches reproduces the same gap in eight weeks. Either the pipeline commits per run (which
      makes `#2`'s review gate a precondition, not a nice-to-have), or a weekly reminder exists.
- [ ] Spot-check the 2026-07-03 → 2026-08-30 batch, which went in unreviewed. Cross-links and
      frontmatter validity were the two invariants the earlier phases checked by hand; nothing has
      checked them since.
- [ ] Nice to have: an AO1–AO10 overview page, wider `companies/` and `projects/` coverage, a
      LinkedIn demo post, the BlueWind Companion integration story.

## Done (current sprint)

Nothing since 2026-07-03. See the archive.
