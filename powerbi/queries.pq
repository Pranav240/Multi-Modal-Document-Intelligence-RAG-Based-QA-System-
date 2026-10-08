// Create a Text parameter DataFolder = <path to this repo>\powerbi\data, then one blank query per block.

// ---- dim_repo ------------------------------------------------
let
  Src = Csv.Document(File.Contents(DataFolder & "\dim_repo.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
  H = Table.PromoteHeaders(Src, [PromoteAllScalars=true]),
  T = Table.TransformColumnTypes(H, {{"repo",type text},{"project_name",type text},{"category",type text},{"url",type text},
        {"first_commit",type date},{"last_commit",type date},{"commits_in_clone",Int64.Type},{"tracked_files",Int64.Type},{"lines_total",Int64.Type}}, "en-US")
in T

// ---- fact_commits --------------------------------------------
let
  Src = Csv.Document(File.Contents(DataFolder & "\fact_commits.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
  H = Table.PromoteHeaders(Src, [PromoteAllScalars=true]),
  T = Table.TransformColumnTypes(H, {{"repo",type text},{"sha",type text},{"author",type text},{"committed_at",type datetimezone},
        {"commit_date",type date},{"message",type text},{"files_changed",Int64.Type},{"insertions",Int64.Type},{"deletions",Int64.Type}}, "en-US"),
  Kind = Table.AddColumn(T, "commit_kind", each
        let m = Text.Lower(Text.Start([message], 12)) in
        if Text.Contains(m,"fix") then "Fix" else if Text.Contains(m,"test") then "Test"
        else if Text.Contains(m,"doc") or Text.Contains(m,"readme") then "Docs" else "Other", type text)
in Kind

// ---- fact_repo_language --------------------------------------
let
  Src = Csv.Document(File.Contents(DataFolder & "\fact_repo_language.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
  H = Table.PromoteHeaders(Src, [PromoteAllScalars=true]),
  T = Table.TransformColumnTypes(H, {{"repo",type text},{"language",type text},{"lines",Int64.Type}}, "en-US")
in T

