-- S111_R59_BACKFILL.sql - Supabase SQL Editor. Run ONLY AFTER S111_R59.sh has SHIPPED.
-- Brings the rows written before R59 into line with the code R59 ships:
--   (a) prediction_outcomes.direction_correct_3d / _7d judged on SPY (GPVS v1.2), from the
--       spy_change_3d / _7d already stored in each row - the same rule as direction() in the code.
--   (b) the 59 two-run reports' sentiment interval with t=12.706 instead of 2.576.
-- Both are derived from stored columns, and the old values are kept in two backup tables,
-- so every change here can be undone (STEP 4). Run each STEP on its own, in order.

-- ===== STEP 1 - backups (writes two NEW tables; touches nothing else) =====
create table s111_backup_gpvs_direction as
  select report_id, direction_correct_3d, direction_correct_7d
  from prediction_outcomes;
create table s111_backup_ci_two_run as
  select id, sentiment_score_lower, sentiment_score_upper, confidence_interval_width
  from reports
  where analysis_runs = 2;
select (select count(*) from s111_backup_gpvs_direction) as outcome_rows_backed_up,
       (select count(*) from s111_backup_ci_two_run)     as two_run_reports_backed_up;

-- ===== STEP 2 - preview (read-only): what STEP 3 will change =====
with x as (
  select direction_correct_3d as d3, direction_correct_7d as d7,
         case when spy_change_3d is null then null
              when lower(predicted_sentiment) = 'bearish' then spy_change_3d < 0
              when lower(predicted_sentiment) = 'bullish' then spy_change_3d > 0 end as n3,
         case when spy_change_7d is null then null
              when lower(predicted_sentiment) = 'bearish' then spy_change_7d < 0
              when lower(predicted_sentiment) = 'bullish' then spy_change_7d > 0 end as n7
  from prediction_outcomes
  where lower(predicted_sentiment) in ('bearish', 'bullish')
)
select 'gpvs direction'                                  as part,
       count(*) filter (where d3 is distinct from n3)    as change_3d,
       count(*) filter (where d7 is distinct from n7)    as change_7d,
       count(*) filter (where n3)                        as spy_right_3d_after,
       count(*) filter (where d3)                        as right_3d_before
from x
union all
select 'ci two-run',
       count(*) filter (where sentiment_score_lower > -1 and sentiment_score_upper < 1),
       count(*) filter (where sentiment_score_lower <= -1 or sentiment_score_upper >= 1),
       null, null
from reports where analysis_runs = 2;
-- ci two-run row: change_3d = rows STEP 3 recomputes (both bounds inside -1..1);
--                 change_7d = rows with a clipped bound, which STEP 3 leaves alone (report it).

-- ===== STEP 3 - the backfill (writes) =====
update prediction_outcomes set
  direction_correct_3d = case when spy_change_3d is null then null
                              when lower(predicted_sentiment) = 'bearish' then spy_change_3d < 0
                              else spy_change_3d > 0 end,
  direction_correct_7d = case when spy_change_7d is null then null
                              when lower(predicted_sentiment) = 'bearish' then spy_change_7d < 0
                              else spy_change_7d > 0 end
where lower(predicted_sentiment) in ('bearish', 'bullish');

-- two runs: mean = (lower+upper)/2, margin = (upper-lower)/2 x 12.706/2.576, clipped to [-1, 1]
update reports set
  sentiment_score_lower     = round(greatest(-1.0, (sentiment_score_lower + sentiment_score_upper) / 2
                                - (sentiment_score_upper - sentiment_score_lower) / 2 * 12.706 / 2.576)::numeric, 3),
  sentiment_score_upper     = round(least(1.0, (sentiment_score_lower + sentiment_score_upper) / 2
                                + (sentiment_score_upper - sentiment_score_lower) / 2 * 12.706 / 2.576)::numeric, 3)
where analysis_runs = 2 and sentiment_score_lower > -1 and sentiment_score_upper < 1;
update reports set
  confidence_interval_width = round((sentiment_score_upper - sentiment_score_lower)::numeric, 3)
where analysis_runs = 2;

-- ===== STEP 3b - after-check (read-only) =====
select 'gpvs' as part, count(*) as rows,
       count(*) filter (where direction_correct_3d) as right_3d,
       count(*) filter (where direction_correct_7d) as right_7d
from prediction_outcomes where lower(predicted_sentiment) in ('bearish', 'bullish')
union all
select 'ci two-run', count(*), round(avg(confidence_interval_width)::numeric * 1000), null
from reports where analysis_runs = 2;
-- ci two-run row: the third column is the new average width x 1000 (it was 163, i.e. 0.163).

-- ===== STEP 4 - UNDO, only if something looks wrong (writes) =====
-- update prediction_outcomes o set direction_correct_3d = b.direction_correct_3d,
--        direction_correct_7d = b.direction_correct_7d
--   from s111_backup_gpvs_direction b where b.report_id = o.report_id;
-- update reports r set sentiment_score_lower = b.sentiment_score_lower,
--        sentiment_score_upper = b.sentiment_score_upper,
--        confidence_interval_width = b.confidence_interval_width
--   from s111_backup_ci_two_run b where b.id = r.id;
