-- S112_C2.sql - Supabase SQL Editor, READ-ONLY. Two reads that S112_C1 opened.

-- (A) Cert (2) replay input: the articles the OLD Stage 1b patterns removed in the 7-day control
--     window. Download this result as CSV (14 rows expected; the grid's 100-row limit is not hit,
--     R-S111-3) and upload it: the current funnel and the pre-S111 funnel will both be IMPORTED
--     and run on these exact texts, so the cert discriminates instead of resting on 0 of 221.
select id, created_at, source, stage1b_reason, title, summary, count(*) over () as rows_in_result
from pipeline_articles
where stage1b_passed = false
  and stage1b_reason like 'Injection pattern:%'
  and created_at >= '2026-10-04 18:16+00' and created_at < '2026-10-11 18:16+00'
order by created_at;

-- (B) The "every 10th run" rule behind credibility and health (main.py: run_count % 10 == 0).
--     get_pipeline_run_count() counts EVERY pipeline_runs row, not main runs. How many rows of
--     each type were written per day since credibility last ran (2026-10-05 19:20)?
select pipeline_type, count(*) as rows, min(run_at) as first_at, max(run_at) as last_at,
       count(*) over () as rows_in_result
from pipeline_runs
where run_at >= '2026-10-05 19:00+00'
group by pipeline_type order by rows desc;
select count(*) as total_rows_now, count(*) % 10 as mod10_now from pipeline_runs;
