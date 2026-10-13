-- S112_C1.sql - Supabase SQL Editor, READ-ONLY. The five S111 certs (S112 mission (a)).
-- Every query prints its own row count (R-S111-3); paste each result as text, not a CSV.
-- Ship times (UTC, the CI push run of each commit): 4a948cc 17:50, ab0353e 18:16, e258cfc 18:27,
-- 8396da8 19:47 on 2026-10-11. Each query reads AFTER its commit against a CONTROL window BEFORE it.

-- (2) Stage 1b removals, after ab0353e+8396da8 vs the 7 days before. A pass: after-window removals
--     carry only injection-shaped titles; the control shows the old patterns removing real news.
select case when created_at >= '2026-10-11 19:47+00' then 'after' else 'control' end as win,
       stage1b_reason, count(*) as removed,
       (array_agg(left(title, 90) order by created_at desc))[1:3] as three_titles,
       count(*) over () as rows_in_result
from pipeline_articles
where stage1b_passed = false
  and created_at >= '2026-10-04 18:16+00'
  and not (created_at >= '2026-10-11 18:16+00' and created_at < '2026-10-11 19:47+00')
group by 1, 2
order by 1, removed desc;

-- (2b) the denominator: articles that reached Stage 1b per window
select case when created_at >= '2026-10-11 19:47+00' then 'after' else 'control' end as win,
       count(*) as reached_1b, count(*) filter (where stage1b_passed = false) as removed,
       min(created_at) as first_at, max(created_at) as last_at
from pipeline_articles
where created_at >= '2026-10-04 18:16+00'
group by 1 order by 1;

-- (3a) source_health.alert_sent per run, after e258cfc vs before. Control: no row ever true
--      before the writer existed. A pass needs an after-run that alerted (the log says so).
select case when run_at >= '2026-10-11 18:27+00' then 'after' else 'control' end as win,
       run_at, count(*) as rows, count(*) filter (where alert_sent) as alert_sent_true,
       count(*) over () as rows_in_result
from source_health
where run_at >= '2026-10-08'
group by 1, run_at order by run_at desc;

-- (3b)+(4a) new prediction_outcomes rows since 8396da8 against the rows before it.
--      direction must equal the SPY rule; black_swan_48h_change is now a 48-hour move.
select case when measured_at >= '2026-10-11 19:47+00' then 'after' else 'control' end as win,
       report_id, measured_at, predicted_sentiment, spy_change_3d, direction_correct_3d,
       spy_change_7d, direction_correct_7d, black_swan_flag, black_swan_48h_change,
       (direction_correct_3d is not distinct from
          case when spy_change_3d is null then null
               when lower(predicted_sentiment) = 'bearish' then spy_change_3d < 0
               when lower(predicted_sentiment) = 'bullish' then spy_change_3d > 0 end) as d3_agrees,
       (direction_correct_7d is not distinct from
          case when spy_change_7d is null then null
               when lower(predicted_sentiment) = 'bearish' then spy_change_7d < 0
               when lower(predicted_sentiment) = 'bullish' then spy_change_7d > 0 end) as d7_agrees,
       count(*) over () as rows_in_result
from prediction_outcomes
where measured_at >= '2026-10-09'
order by measured_at desc;

-- (5) source credibility recomputed after the backfill (which ran after 8396da8 shipped).
select count(*) as sources, max(last_calculated) as newest, min(last_calculated) as oldest,
       count(*) filter (where last_calculated >= '2026-10-11 19:47+00') as recomputed_after_backfill
from source_credibility;

-- (5b) the backup tables are still there (to be dropped only after (5) passes)
select table_name, (xpath('/row/c/text()', query_to_xml('select count(*) as c from public.' || table_name, false, true, '')))[1]::text::int as rows
from information_schema.tables
where table_schema = 'public' and table_name like 's111_backup_%';
