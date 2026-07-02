"""Poll an AgentMail inbox for offshoreWIND.biz newsletter issues and update
the OKF bundle from each new issue.

Usage:
    python run.py

First run creates the inbox and prints its address — subscribe that address
to the offshoreWIND.biz newsletter, then leave this running. See README.md
in this directory for full setup.
"""
from __future__ import annotations

import json
import os
import time
from email.utils import parseaddr
from pathlib import Path

from agentmail import AgentMail
from agentmail.inboxes import CreateInboxRequest
from dotenv import load_dotenv

from wiki_agent import update_wiki_from_email

load_dotenv()

STATE_FILE = Path(__file__).resolve().parent / ".agent_state.json"
POLL_INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL_SECONDS", "30"))
INBOX_USERNAME = os.environ.get("AGENTMAIL_INBOX_USERNAME") or None


def _load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def _save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))


def _sender_email(message) -> str:
    sender = getattr(message, "from_", None) or getattr(message, "from", None) or ""
    _, email = parseaddr(str(sender))
    return email.lower()


def get_or_create_inbox(client: AgentMail):
    state = _load_state()
    if state.get("inbox_id"):
        try:
            return client.inboxes.get(state["inbox_id"])
        except Exception as e:
            print(f"(stale state, creating new inbox: {e})")

    inbox = client.inboxes.create(
        request=CreateInboxRequest(
            username=INBOX_USERNAME,
            display_name="Offshore Wind Wiki curator",
        )
    )
    state["inbox_id"] = inbox.inbox_id
    state["email"] = inbox.email
    _save_state(state)
    return inbox


def process_message(agentmail_client: AgentMail, message, inbox) -> None:
    full = agentmail_client.inboxes.messages.get(inbox.inbox_id, message.message_id)
    body = (getattr(full, "extracted_text", None) or full.text or "").strip()
    if not body:
        body = getattr(full, "extracted_html", None) or full.html or ""
    if not body:
        print("  ! empty body, skipping")
        agentmail_client.inboxes.messages.update(
            inbox.inbox_id, message.message_id, remove_labels=["unread"], add_labels=["empty"]
        )
        return

    summary = update_wiki_from_email(subject=full.subject or "", sender=full.from_ or "", body=body)
    print(f"  -> {summary}")
    agentmail_client.inboxes.messages.update(
        inbox.inbox_id, message.message_id, remove_labels=["unread"], add_labels=["digested"]
    )


def main() -> None:
    agentmail_client = AgentMail(api_key=os.environ["AGENTMAIL_API_KEY"])

    inbox = get_or_create_inbox(agentmail_client)
    print(f"\nOffshore Wind Wiki curator live at: {inbox.email}")
    print("Subscribe this address to the offshoreWIND.biz newsletter.")
    print(f"Polling every {POLL_INTERVAL_SECONDS}s. Ctrl-C to stop.\n")

    seen: set[str] = set()
    while True:
        try:
            resp = agentmail_client.inboxes.messages.list(inbox.inbox_id, labels=["unread"])
            new_messages = [m for m in (resp.messages or []) if m.message_id not in seen]
            for message in new_messages:
                seen.add(message.message_id)
                if _sender_email(message) == inbox.email.lower():
                    continue  # skip our own state, if any
                print(f"New message: {(message.subject or '(no subject)')[:70]!r} from {_sender_email(message)}")
                try:
                    process_message(agentmail_client, message, inbox)
                except Exception as e:
                    print(f"  ! error processing message: {e}")
        except Exception as e:
            print(f"poll error: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
