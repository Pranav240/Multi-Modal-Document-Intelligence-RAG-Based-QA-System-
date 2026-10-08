# Power BI report: Multi-Modal Document Intelligence

Place this folder at `powerbi/` in the repo.

## Setup (Power BI Desktop, Windows)
1. Transform data > Manage Parameters > New: `DataFolder` (Text) = full path to `powerbi\data`.
2. For each block in `queries.pq`: New Source > Blank Query > Advanced Editor > paste > rename to the block name.
3. Close & Apply. Add `DimDate` and measures from `measures.dax` (mark DimDate as date table).
4. View > Themes > Browse > `theme.json`.
5. Relationships (1 -> *): `dim_repo[repo]` to `fact_commits[repo]` and `fact_repo_language[repo]`; `DimDate[Date]` to `fact_commits[commit_date]`.

This repo has no recorded metrics, only 2 commits. The pack is an activity report only (commits, lines by language).
Pages: one overview page: cards Commits, Lines Added, Repo Lines; commits by month; language bar.
Resume-stated qualitative result (not charted): works on the Qatar IMF 2024 Article IV report, known table-extraction limitation. To add real metrics (retrieval hit rate, answer accuracy) you would need to run an evaluation first.

Data snapshot: 2026-10-08.
