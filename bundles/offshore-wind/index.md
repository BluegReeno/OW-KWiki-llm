---
okf_version: "0.1"
---

# Offshore Wind Knowledge Bundle

A living knowledge base on the global offshore wind sector, in the
[Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) (OKF).
Read directly as markdown, or navigate with `okf-cli.py`. New industry
news is ingested continuously via an [AgentMail](https://agentmail.to)
inbox subscribed to the [offshoreWIND.biz](https://www.offshorewind.biz/)
daily newsletter — see `pipeline/`.

# Sections

* [companies](companies/) - Developers, OEMs, and marine contractors active in offshore wind.
* [projects](projects/) - Notable offshore wind farms, by stage (planning, construction, operating).
* [tenders](tenders/) - Tender/auction rounds and calls for bids, by market (contract terms, award criteria, timelines, results).
* [technology](technology/) - Cross-cutting technical concepts: foundations, grid connection, power-to-x.
* [policy](policy/) - Regulatory and permitting frameworks by region.
* [digests](digests/) - Dated summaries of industry news, auto-generated from the newsletter ingestion pipeline.

# Tagging convention

`tenders` is a first-class tag: apply it to any concept touching a call
for bids, auction round, or contract award (a `tenders/` page itself, but
also a `projects/` or `policy/` page where a tender is the reason the page
exists). This keeps everything tender-related cross-searchable with
`okf-cli.py find tenders`, independent of which directory a page lives in.

# How this bundle stays current

`pipeline/` polls an AgentMail inbox for new offshoreWIND.biz newsletter
issues, and has an agent read each issue, update or create the relevant
concept pages above, and log a dated entry in `digests/` and `log.md`.
See `pipeline/README.md` to run it.
