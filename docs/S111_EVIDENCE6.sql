-- S111_EVIDENCE6.sql - Supabase SQL Editor, read-only. Run each query on its own.
-- Item (b), measure before designing: if GPVS judged RISK (a downside / large move) instead of
-- direction, (13) how often does each candidate event happen (the climatology a Brier skill
-- score is measured against), and (14) does anything GNI already outputs separate the windows
-- where it happened from those where it did not (AUC: 0.5 = no signal, 1.0 = perfect)?

-- (13) base rates of candidate events over the stored outcomes
select count(*)                                                        as windows,
       round(avg((spy_change_3d <= -1)::int)::numeric, 3)              as p_spy_3d_down_1pct,
       round(avg((spy_change_7d <= -1)::int)::numeric, 3)              as p_spy_7d_down_1pct,
       round(avg((spy_change_7d <= -2)::int)::numeric, 3)              as p_spy_7d_down_2pct,
       round(avg((abs(spy_change_7d) >= 2)::int)::numeric, 3)          as p_spy_7d_move_2pct,
       round(avg((abs(spy_change_3d) >= 2)::int)::numeric, 3)          as p_spy_3d_move_2pct
from prediction_outcomes
where spy_change_3d is not null and spy_change_7d is not null;

-- (14) AUC of each GNI output for each candidate event (Mann-Whitney: share of
--      (event, no-event) pairs where the event window had the higher risk score, ties count half)
with o as (
  select r.escalation_score::float8              as esc,
         -r.sentiment_score::float8              as neg_sent,
         p.spy_change_3d as s3, p.spy_change_7d as s7
  from prediction_outcomes p join reports r on r.id = p.report_id
  where p.spy_change_3d is not null and p.spy_change_7d is not null
    and r.escalation_score is not null and r.sentiment_score is not null
), ev as (
  select 'spy_7d <= -1%' as event, esc, neg_sent, s7 <= -1 as hit from o
  union all select 'spy_7d <= -2%', esc, neg_sent, s7 <= -2 from o
  union all select '|spy_7d| >= 2%', esc, neg_sent, abs(s7) >= 2 from o
  union all select 'spy_3d <= -1%', esc, neg_sent, s3 <= -1 from o
)
select a.event,
       (select count(*) from ev e where e.event = a.event and e.hit)     as events,
       (select count(*) from ev e where e.event = a.event and not e.hit) as non_events,
       round(avg(case when a.esc > b.esc then 1.0 when a.esc = b.esc then 0.5 else 0 end)::numeric, 3)
                                                   as auc_escalation_score,
       round(avg(case when a.neg_sent > b.neg_sent then 1.0 when a.neg_sent = b.neg_sent then 0.5 else 0 end)::numeric, 3)
                                                   as auc_minus_sentiment
from ev a join ev b on a.event = b.event and a.hit and not b.hit
group by a.event
order by a.event;
