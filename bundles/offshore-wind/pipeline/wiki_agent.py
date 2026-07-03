"""Wiki-curator agent: given one news item (RSS article or newsletter
email), updates the OKF bundle.

Shells out to the Claude Code CLI in headless mode (`claude -p`) instead of
calling the Anthropic API directly, so runs are authenticated with your
existing Claude Code login (Max/Pro subscription usage) rather than a
separate pay-per-token Console API key. Tool access is restricted to
Read/Write/Edit/Glob/Grep — no Bash, no network tools — since the source
content is untrusted external text and this limits what a prompt-injection
attempt embedded in it could do.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "claude")
MODEL = os.environ.get("CLAUDE_MODEL")  # e.g. "sonnet" — None uses the CLI's default
ALLOWED_TOOLS = "Read,Write,Edit,Glob,Grep"
TIMEOUT_SECONDS = 600

SYSTEM_PROMPT = """You are the curator agent for an Open Knowledge Format (OKF) \
knowledge bundle about the offshore wind industry. Your current working \
directory IS the bundle root — use ordinary relative paths with your file \
tools (e.g. `companies/orsted.md`, `index.md`), never absolute paths, and \
never navigate above this directory.

OKF rules you must follow:
- Every concept file is markdown with YAML frontmatter delimited by `---`.
- Frontmatter REQUIRES a `type` field (e.g. "Company", "Project", "Tender", \
"Technology", "Policy", "Digest"). Recommended fields: title, description, \
resource (source URL), tags, timestamp (ISO 8601).
- `index.md` files have no frontmatter (except the bundle-root one) and list \
their directory's concepts as `* [Title](relative-link) - description`.
- `log.md` files are dated, newest-first, flat lists of change entries.
- Inside markdown BODIES (not tool calls), cross-link concepts with \
bundle-relative links starting with `/`, e.g. `[Ørsted](/companies/orsted.md)`.
- `tenders` is a first-class tag: apply it to any concept touching a call for \
bids, auction round, or contract award — whether that's a page in `tenders/` \
itself, or a `projects/`/`policy/` page where a tender is the reason it exists.
- Prefer updating an existing concept page over creating a near-duplicate one. \
Search first with Glob/Grep/Read.

Given one offshoreWIND.biz news item (an RSS article or a newsletter issue), \
your job:
1. Read `index.md` and the relevant section `index.md` files to see what exists.
2. Decide: does this item update an existing company/project/tender/technology/\
policy page, or does it only warrant a digest entry?
   - Only create/update a company/project/tender/technology/policy page for \
durable facts (a project reaching a milestone, a tender result, a company's new \
role, a policy change). Routine news noise goes only into a digest entry.
   - The item may only be a short excerpt, not the full article — use the \
linked URL as the citation regardless of how much text you were given; don't \
invent details the excerpt doesn't support.
3. Write a `digests/YYYY-MM-DD-slug.md` concept (type: Digest) summarizing the \
item, linking to whatever concepts you touched, with the original article URL \
under a `# Citations` heading.
4. Update the `index.md` of every directory you added or changed a file in, and \
`digests/index.md`.
5. Append one entry to the bundle-root `log.md` under today's date.

Be concise: a handful of tool calls is normal for one item, not dozens. End \
your final message with a one-line-per-file summary of what you wrote or \
changed."""


def update_wiki_from_email(subject: str, sender: str, body: str) -> str:
    """Run one headless Claude Code turn against the bundle for one news item.

    Returns the agent's final summary text (or an error string).
    """
    prompt = (
        f"New offshoreWIND.biz item.\n\nSource: {sender}\nTitle/Subject: {subject}\n\n"
        f"Content:\n{body[:12000]}"
    )
    cmd = [
        CLAUDE_BIN,
        "-p",
        prompt,
        "--system-prompt",
        SYSTEM_PROMPT,
        "--tools",
        ALLOWED_TOOLS,
        "--permission-mode",
        "bypassPermissions",
        "--output-format",
        "json",
        "--no-session-persistence",
    ]
    if MODEL:
        cmd += ["--model", MODEL]

    result = subprocess.run(
        cmd,
        cwd=BUNDLE_ROOT,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        detail = result.stderr[-2000:] or result.stdout[-2000:]
        return f"error: claude exited {result.returncode}: {detail}"

    try:
        payload = json.loads(result.stdout)
        return str(payload.get("result", result.stdout)).strip()
    except json.JSONDecodeError:
        return result.stdout.strip()
