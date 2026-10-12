-- S111_EVIDENCE3.sql - Supabase SQL Editor, read-only. Run each query on its own.
-- (6) = item B (the two Stage 1b leftovers). (7) = sweep: CI run count. (8) = item A: how often the instrument split changes a verdict.

-- (6) Candidates on EVERY stored article (title + summary).
--     e1 = the S44 exfil pattern, narrowed to "send/leak <the|all|your> data ... to http(s)://"
--     j1 = the attack the S111 narrowing stopped catching: "jailbreak the model / the AI"
--     old_exfil = the S44 pattern as it is today, for comparison
with cands(name, rx) as (values
  ('e1 send data TO a URL',   '(send|forward|upload|exfiltrate|leak)\s+(all|this|the|your|any)\s+(data|information|results|credentials|content|articles?)\s+to\s+https?://'),
  ('j1 jailbreak the model',  'jailbreak\s+(the|this|your)\s+(ai|model|assistant|system|llm|chatbot)'),
  ('old_exfil (today)',       '(send|forward|upload|exfiltrate|leak)[^\n]{0,30}(data|information|results|credentials|content|article)s?[^\n]{0,30}https?://')
)
select c.name,
       count(a.*) filter (where (a.title || ' ' || coalesce(a.summary, '')) ~* c.rx)   as matches,
       (array_agg(a.title) filter (where (a.title || ' ' || coalesce(a.summary, '')) ~* c.rx))[1:3] as sample_titles
from cands c cross join pipeline_articles a
group by c.name
order by c.name;

-- (7) Sweep: how many sentiment samples stand behind each report's "95% CI".
--     The code uses t=4.303 only when runs=3; any other count gets 2.576 (a 99% z value).
--     runs=2 would need t=12.706, so a runs=2 interval is about five times too narrow.
select analysis_runs, count(*) as reports,
       round(avg(confidence_interval_width)::numeric, 3) as avg_ci_width,
       min(created_at) as first_seen, max(created_at) as last_seen
from reports
group by analysis_runs
order by analysis_runs;

-- (8) Item A: how often judging direction on the primary instrument (USO/GLD) gives a
--     different verdict from SPY, which the accuracy score uses.
with x as (
  select predicted_sentiment as s, direction_correct_3d as d3, direction_correct_7d as d7, accuracy_score,
         case when spy_change_3d is null then null
              when lower(predicted_sentiment) = 'bearish' then spy_change_3d < 0
              else spy_change_3d > 0 end as spy_d3,
         case when spy_change_7d is null then null
              when lower(predicted_sentiment) = 'bearish' then spy_change_7d < 0
              else spy_change_7d > 0 end as spy_d7
  from prediction_outcomes
  where lower(predicted_sentiment) in ('bearish', 'bullish')
)
select count(*)                                                   as directional_rows,
       count(*) filter (where d3 is distinct from spy_d3)         as differ_3d,
       count(*) filter (where d7 is distinct from spy_d7)         as differ_7d,
       count(*) filter (where d3 is distinct from spy_d3
                           or d7 is distinct from spy_d7)         as differ_any,
       count(*) filter (where (d3 is distinct from spy_d3 or d7 is distinct from spy_d7)
                           and accuracy_score >= 0.5)             as split_rows_scored_right_on_spy
from x;
