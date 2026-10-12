-- S111_WAITED.sql - Supabase SQL Editor, read-only. Three things past sessions waited on and never read.
-- (A) S109 UNKNOWN: "the first health run after d87f57a writes no avg 0 alert".
--     d87f57a = 2026-10-04 12:58:33Z. The health agent runs when the main run count is a multiple of 10.
select created_at, alert_type, severity, metric_name, metric_value, threshold, left(message, 90) as message
from health_alerts
where created_at > timestamptz '2026-10-04 12:58:33+00'
order by created_at;

-- (A') the main runs since d87f57a, numbered as the agent counts them, to see which one was the
--      multiple of ten (if (A) is empty, this shows whether a health run was even due)
select count(*) filter (where pipeline_type = 'main') as main_rows_total,
       count(*) filter (where pipeline_type = 'main' and run_at > timestamptz '2026-10-04 12:58:33+00') as main_rows_since,
       count(*) as all_rows
from pipeline_runs;

-- (B) S109 UNKNOWN: prompt v1 run_count 383 against 265 main rows
select version, active, run_count, avg_quality_score from prompt_variants order by version;
