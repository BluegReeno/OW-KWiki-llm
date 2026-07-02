"""Poll offshoreWIND.biz's public RSS feed and update the OKF bundle from
new articles.

Simpler than the AgentMail/newsletter route: this is a public feed, no
account, no double opt-in, no email forwarding rules to configure. Uses
only the Python standard library.

Usage:
    python poll_rss.py
"""
from __future__ import annotations

import json
import os
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from dotenv import load_dotenv

from wiki_agent import update_wiki_from_email

load_dotenv()

FEED_URL = "https://www.offshorewind.biz/feed/"
STATE_FILE = Path(__file__).resolve().parent / ".rss_state.json"
POLL_INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL_SECONDS", "1800"))
USER_AGENT = "Mozilla/5.0 (offshore-wind-wiki-bot; +https://github.com/BluegReeno/OW-KWiki-llm)"


def _load_seen() -> set[str]:
    if STATE_FILE.exists():
        return set(json.loads(STATE_FILE.read_text()))
    return set()


def _save_seen(seen: set[str]) -> None:
    STATE_FILE.write_text(json.dumps(sorted(seen)))


def fetch_items() -> list[dict]:
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        xml_bytes = resp.read()
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall("./channel/item"):
        guid = item.findtext("guid") or item.findtext("link") or ""
        items.append(
            {
                "guid": guid,
                "title": (item.findtext("title") or "").strip(),
                "link": (item.findtext("link") or "").strip(),
                "pub_date": (item.findtext("pubDate") or "").strip(),
                "categories": [c.text for c in item.findall("category") if c.text],
                "description": (item.findtext("description") or "").strip(),
            }
        )
    return items


def main() -> None:
    first_run = not STATE_FILE.exists()
    print(f"Polling {FEED_URL} every {POLL_INTERVAL_SECONDS}s. Ctrl-C to stop.")

    if first_run:
        items = fetch_items()
        seen = {i["guid"] for i in items}
        _save_seen(seen)
        print(f"First run: baselined {len(seen)} existing articles as already-seen (not processed).")
    else:
        seen = _load_seen()

    while True:
        try:
            items = fetch_items()
            new_items = [i for i in items if i["guid"] not in seen]
            for item in reversed(new_items):  # oldest first
                print(f"New article: {item['title'][:70]!r}")
                body = (
                    f"Title: {item['title']}\n"
                    f"Link: {item['link']}\n"
                    f"Published: {item['pub_date']}\n"
                    f"Categories: {', '.join(item['categories'])}\n\n"
                    f"Excerpt: {item['description']}"
                )
                summary = update_wiki_from_email(
                    subject=item["title"], sender="offshorewind.biz", body=body
                )
                print(f"  -> {summary}")
                seen.add(item["guid"])
                _save_seen(seen)
        except Exception as e:
            print(f"poll error: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
