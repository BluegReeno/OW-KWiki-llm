"""Check offshoreWIND.biz's public RSS feed once and update the OKF bundle
from any new articles, then exit.

Designed to be invoked periodically by cron/launchd — not a long-running
daemon. Uses only the Python standard library plus python-dotenv.

Usage:
    python poll_rss.py
"""
from __future__ import annotations

import fcntl
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from dotenv import load_dotenv

from wiki_agent import update_wiki_from_email

load_dotenv()

FEED_URL = "https://www.offshorewind.biz/feed/"
HERE = Path(__file__).resolve().parent
STATE_FILE = HERE / ".rss_state.json"
LOCK_FILE = HERE / ".rss_poll.lock"
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


def run_once() -> None:
    first_run = not STATE_FILE.exists()

    if first_run:
        items = fetch_items()
        seen = {i["guid"] for i in items}
        _save_seen(seen)
        print(f"First run: baselined {len(seen)} existing articles as already-seen (not processed).")
        return

    seen = _load_seen()
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
        summary = update_wiki_from_email(subject=item["title"], sender="offshorewind.biz", body=body)
        print(f"  -> {summary}")
        if summary.startswith("error:"):
            print(f"  ! not marking as seen, will retry next run: {item['guid']}")
            continue
        seen.add(item["guid"])
        _save_seen(seen)

    if not new_items:
        print("No new articles.")


def main() -> None:
    # Guards against overlapping runs if one invocation takes longer than
    # the cron interval (e.g. several articles need curating at once).
    lock_fp = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lock_fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("Another poll is already running, skipping this invocation.")
        sys.exit(0)

    try:
        run_once()
    except Exception as e:
        print(f"poll error: {e}")
        sys.exit(1)
    finally:
        fcntl.flock(lock_fp, fcntl.LOCK_UN)
        lock_fp.close()


if __name__ == "__main__":
    main()
