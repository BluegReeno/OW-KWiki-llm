# Ingestion pipeline

Keeps `../` (the offshore wind OKF bundle) current by reading the
offshoreWIND.biz daily newsletter through an [AgentMail](https://agentmail.to)
inbox and having a Claude Code agent — scoped to read/write only inside the
bundle — update the relevant concept pages, the way the OKF spec expects
an "enrichment agent" to work.

```
offshoreWIND.biz newsletter → AgentMail inbox → run.py polls unread mail
   → wiki_agent.py shells out to `claude -p` (Read/Write/Edit/Glob/Grep
     tools only, cwd = bundle root) → updates companies/projects/tenders/
     technology/policy pages, writes a digests/YYYY-MM-DD-*.md entry,
     logs to log.md
```

Runs via `claude -p` (Claude Code's headless mode) rather than the
Anthropic API SDK, so it's authenticated with your existing Claude Code
login and draws on your Claude Code/Max subscription usage — no separate
pay-per-token API key needed.

## One-time setup

1. **AgentMail account + API key** — sign up at
   [console.agentmail.to](https://console.agentmail.to), create an API key.
2. **Claude Code must be logged in** — if `claude` already works
   interactively in your terminal, you're set. Otherwise run `claude` once
   and complete login, or `claude auth login`.
3. Copy the env file and fill in the AgentMail key:
   ```bash
   cd bundles/offshore-wind/pipeline
   cp .env.example .env
   # edit .env
   ```
4. Install dependencies (a virtualenv is recommended):
   ```bash
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
5. First run creates the AgentMail inbox and prints its address:
   ```bash
   python run.py
   ```
   Leave it running — it also polls. In a separate step, subscribe that
   printed address to the **offshoreWIND.biz newsletter**
   (newsletter signup form on [offshorewind.biz](https://www.offshorewind.biz/)).
6. From then on, every newsletter issue that arrives gets processed
   automatically: the agent reads it, updates or creates concept pages,
   and logs the change. Re-running `python run.py` later reuses the same
   inbox (its id is cached in `.agent_state.json`, which is gitignored).

## Running it continuously

`run.py` is a plain polling loop (`POLL_INTERVAL_SECONDS`, default 30s) —
no external infrastructure required, just keep the process alive (tmux,
a systemd/launchd service, or a background `nohup` are all fine for a
demo). AgentMail also supports webhooks if you want push instead of
poll — see `docs.agentmail.to/webhooks-overview` — not implemented here
to keep the demo dependency-free.

## Cost / safety notes

- Each newsletter issue triggers one `claude -p` invocation
  (`wiki_agent.TIMEOUT_SECONDS` caps it at 10 minutes) — Claude Code
  manages its own internal tool-call loop for that single invocation.
- Tool access is restricted to `Read,Write,Edit,Glob,Grep` — no `Bash`, no
  network tools. The newsletter body is untrusted external text fed into
  an agent running with `--permission-mode bypassPermissions` (no
  human approval prompts), so this restriction is the actual safety
  boundary: worst case a prompt-injection attempt in a newsletter causes
  a bad markdown edit inside the bundle, not arbitrary code execution or
  data exfiltration.
- Unlike a hand-rolled tool sandbox, `claude -p` does not hard-enforce
  staying inside `cwd` — it relies on the system prompt instructing the
  agent to use only relative paths within the bundle. Review `git diff`
  on the bundle periodically like you would any other agent-authored
  content, and keep an eye out for changes outside `bundles/offshore-wind/`.
