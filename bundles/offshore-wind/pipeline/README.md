# Ingestion pipeline

Keeps `../` (the offshore wind OKF bundle) current by polling
offshoreWIND.biz's public RSS feed and having a Claude Code agent —
scoped to read/write only inside the bundle — update the relevant
concept pages, the way the OKF spec expects an "enrichment agent" to work.

```
cron (every 30 min) → poll_rss.py checks https://www.offshorewind.biz/feed/ once, exits
   → wiki_agent.py shells out to `claude -p` (Read/Write/Edit/Glob/Grep
     tools only, cwd = bundle root) → updates companies/projects/tenders/
     technology/policy pages, writes a digests/YYYY-MM-DD-*.md entry,
     logs to log.md
```

No account, no API key, no email — the feed is public. The curator agent
runs via `claude -p` (Claude Code's headless mode) rather than the
Anthropic API SDK, so it's authenticated with your existing Claude Code
login and draws on your Claude Code/Max subscription usage.

## One-time setup

1. **Claude Code must be logged in** — if `claude` already works
   interactively in your terminal, you're set. Otherwise run `claude` once
   and complete login, or `claude auth login`.
2. Install dependencies (a virtualenv is recommended):
   ```bash
   cd bundles/offshore-wind/pipeline
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
3. (Optional) copy `.env.example` to `.env` to override the model or the
   `claude` binary path — defaults work fine without it. If you do run it
   via cron (see below), set `CLAUDE_BIN` to `claude`'s absolute path
   (`which claude`) since cron's `PATH` won't include it otherwise.
4. First run — baselines every article currently in the feed as "already
   seen" without processing them (so you don't get a burst of ~20 pages
   on day one):
   ```bash
   python poll_rss.py
   ```

## Running it periodically (cron)

`poll_rss.py` checks the feed once and exits — it is NOT a long-running
daemon, so it's meant to be invoked periodically rather than kept alive.
offshoreWIND.biz publishes roughly hourly, so every 30 minutes is plenty:

```cron
*/30 * * * * cd /path/to/bundles/offshore-wind/pipeline && /path/to/bundles/offshore-wind/pipeline/venv/bin/python poll_rss.py >> /path/to/bundles/offshore-wind/pipeline/poll.log 2>&1
```

Add it with `crontab -e` (or non-interactively:
`(crontab -l; echo "...") | crontab -`). Notes:
- Use the venv's `python` directly (absolute path) rather than relying on
  `source venv/bin/activate`, which doesn't work in cron's non-interactive
  shell.
- `poll.log` accumulates output — it's gitignored (`*.log`).
- A file lock (`.rss_poll.lock`, via `fcntl.flock`) makes concurrent
  invocations a no-op, in case one run is still curating articles when
  the next cron tick fires.
- To stop: `crontab -e` and delete the line, or `crontab -r` to clear
  your whole crontab (careful if you have other cron jobs).

## Cost / safety notes

- Each new article triggers one `claude -p` invocation
  (`wiki_agent.TIMEOUT_SECONDS` caps it at 10 minutes) — Claude Code
  manages its own internal tool-call loop for that single invocation.
- Tool access is restricted to `Read,Write,Edit,Glob,Grep` — no `Bash`, no
  network tools. Feed content is untrusted external text fed into an
  agent running with `--permission-mode bypassPermissions` (no human
  approval prompts), so this restriction is the actual safety boundary:
  worst case a prompt-injection attempt in an article causes a bad
  markdown edit inside the bundle, not arbitrary code execution or data
  exfiltration.
- Unlike a hand-rolled tool sandbox, `claude -p` does not hard-enforce
  staying inside `cwd` — it relies on the system prompt instructing the
  agent to use only relative paths within the bundle. Review `git diff`
  on the bundle periodically like you would any other agent-authored
  content, and keep an eye out for changes outside `bundles/offshore-wind/`.

## Why not AgentMail / the newsletter?

An earlier version of this pipeline polled an AgentMail inbox subscribed
to offshoreWIND.biz's newsletter. In practice the newsletter signup's
confirmation email never arrived reliably, and the correct pattern (per
AgentMail's own
[newsletter-digest example](https://github.com/agentmail-to/agentmail-examples/tree/main/newsletter-digest))
requires subscribing with a real, human-monitored inbox and setting up
mail-forwarding rules to the AgentMail address — more moving parts than
this project needs, since offshoreWIND.biz happens to publish a public
RSS feed that gives the same content with none of that friction. An
AgentMail account/API key/MCP connection may still exist from that
attempt — it's unused by this pipeline now, but harmless to keep around
for a future source that's actually email-only.
