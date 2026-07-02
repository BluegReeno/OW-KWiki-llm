# OW-KWiki-llm

A continuously-updated **AI-queryable knowledge base for the offshore
wind industry** — an experiment applying Andrej Karpathy's "LLM wiki"
idea and Google's [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) (OKF)
to a real sector: companies, projects, tenders, technology, and policy,
kept current by an automated ingestion pipeline instead of manual upkeep.

> "Instead of just dumping documents into RAG, let an LLM incrementally
> build and maintain a structured, interlinked wiki." — the idea this
> project tests, from [the video that inspired it](transcript.md).

## What's here

```
bundles/offshore-wind/     the knowledge bundle itself (start here)
├── index.md                 table of contents
├── okf-cli.py                dependency-free navigation/search CLI
├── companies/ projects/      OKF concept pages: developers, OEMs,
├── tenders/ technology/      contractors, wind farms, auction rounds,
├── policy/ digests/          tech concepts, regulation, news digests
└── pipeline/                 keeps the bundle current automatically
    ├── poll_rss.py             checks offshoreWIND.biz's RSS feed
    ├── wiki_agent.py           the curator agent (`claude -p`, sandboxed)
    └── README.md               pipeline setup + cron scheduling

examples/cole-medin-ai-coding/   reference OKF bundle (separate git clone,
                                 not vendored — see .gitignore)
reflexion.md, transcript.md       the idea and its source material
```

## Quick start

**Ask it questions** — point any coding agent (Claude Code, Cursor, Codex...)
at `bundles/offshore-wind/`, tell it to read `README.md`, and start asking
about the offshore wind sector. Or browse it yourself:

```bash
cd bundles/offshore-wind
python3 okf-cli.py index              # table of contents
python3 okf-cli.py find "floating"    # keyword search across the bundle
python3 okf-cli.py read tenders/uk-cfd-allocation-round-7
```

It also opens directly as an **Obsidian vault** (File → Open folder as
vault) for browsing and the graph view.

**Keep it current** — see `bundles/offshore-wind/pipeline/README.md` to
run the ingestion pipeline, which polls offshoreWIND.biz's public RSS
feed on a cron schedule and has a sandboxed Claude Code agent update the
relevant pages for any durable news (no API key required — it runs on
your Claude Code login).

## Why OKF

A plain "LLM wiki" works, but everyone builds one differently — no
shared structure means no agent can traverse someone else's wiki
confidently, and no two wikis can be merged or compared. OKF is a
minimal standard on top: a required `type` field, conventional
`index.md`/`log.md` files, and a bundle-relative linking convention —
just enough for any agent to consume or produce a bundle predictably.
See the [full spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
or the reference bundle in `examples/cole-medin-ai-coding/`.

## Status

Current focus, what's done, and what's next: see
[`.claude/STATUS.md`](.claude/STATUS.md) and the task file it points to
in [`.claude/tasks/`](.claude/tasks/).

## License

Personal project, no license specified.
