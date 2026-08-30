# STATUS — Offshore Wind Knowledge Wiki

Last updated: 2026-08-30
State: **running unattended, uncommitted** — last commit 2026-07-03; the cron pipeline has been
writing ever since.

> History lives in [`STATUS-ARCHIVE.md`](./STATUS-ARCHIVE.md), verbatim. Nothing below repeats it.

## Current Focus

v2 is live: the OKF bundle plus an unattended pipeline that polls offshoreWIND.biz's public RSS
feed and curates entries through `claude -p`, scheduled by cron (20:00 local, fcntl-locked against
overlapping runs). Validated against 15 real articles — 10 manual, 5 fully automatic.

**The pipeline never stopped, and none of its output is in git.** Measured 2026-08-30: the cron
entry is live (`0 20 * * *`, `pipeline/poll_rss.py`), `poll.log` shows clean runs, and `log.md`
carries entries up to **2026-08-28** — but the last commit is 2026-07-03. The working tree holds
**38 modified and 291 untracked files** under `bundles/`, and the digests directory has grown from
**15 tracked to 163 on disk**. Nearly two months of curated content exists only on this machine,
with no backup and no review.

## In Progress

- [ ] Nothing.

## Backlog

- [ ] [#2](https://github.com/BluegReeno/OW-KWiki-llm/issues/2) — add a review gate before pipeline
      commits land unattended. Likely a PR plus a verification agent, following the PR #1 pattern.
      This is the one thing standing between "unattended" and "trusted".
- [ ] **Review and commit the backlog of pipeline output**, or decide it is not worth keeping.
      291 untracked files is past the point where a per-file review is realistic, which is exactly
      the situation `#2`'s review gate was meant to prevent. Until this is resolved the repo's git
      history describes a wiki that no longer matches the disk.
- [ ] Nice to have: an AO1–AO10 overview page, wider `companies/` and `projects/` coverage, a
      LinkedIn demo post, the BlueWind Companion integration story.

## Done (current sprint)

Nothing since 2026-07-03. See the archive.
