-- S111_EVIDENCE5.sql - Supabase SQL Editor, read-only. Run each query on its own.
-- Is GPVS direction skill better than chance? (sweep item: base rate)
-- Reference: Pesaran & Timmermann (1992), JBES 10(4):461-465 - formula as implemented in
-- statsmodels.stats.diagnostic.pesaran_timmermann:
--   p_hat = share of rows where sign(predicted) = sign(actual)
--   p_y = share of actual SPY moves > 0,  p_z = share of predictions that are Bullish
--   p_ind = p_y*p_z + (1-p_y)*(1-p_z)        (hit rate expected if calls and moves are independent)
--   S = (p_hat - p_ind) / sqrt( p_ind(1-p_ind)/n - [ (2p_y-1)^2 p_z(1-p_z) + (2p_z-1)^2 p_y(1-p_y) ]/n )
--   S ~ N(0,1) under "no directional skill"; S > 1.645 = skill at 5% (one-sided).
-- Also the two do-nothing reference forecasts (WMO JWGFVR: skill is measured against a reference).

-- (11) contingency table + PT statistic, 3d and 7d
with h as (
  select 3 as days, lower(predicted_sentiment) = 'bullish' as z_pos, spy_change_3d > 0 as y_pos
  from prediction_outcomes
  where lower(predicted_sentiment) in ('bearish', 'bullish') and spy_change_3d is not null
  union all
  select 7, lower(predicted_sentiment) = 'bullish', spy_change_7d > 0
  from prediction_outcomes
  where lower(predicted_sentiment) in ('bearish', 'bullish') and spy_change_7d is not null
), s as (
  select days, count(*)::float8 as n,
         count(*) filter (where not z_pos and not y_pos) as bear_call_spy_down,
         count(*) filter (where not z_pos and y_pos)     as bear_call_spy_up,
         count(*) filter (where z_pos and y_pos)         as bull_call_spy_up,
         count(*) filter (where z_pos and not y_pos)     as bull_call_spy_down,
         avg(y_pos::int)::float8                         as p_y,
         avg(z_pos::int)::float8                         as p_z,
         avg((y_pos = z_pos)::int)::float8               as p_hat
  from h group by days
), t as (
  select *, p_y * p_z + (1 - p_y) * (1 - p_z) as p_ind from s
)
select days, n::int, bear_call_spy_down, bear_call_spy_up, bull_call_spy_up, bull_call_spy_down,
       round(p_hat::numeric, 3)        as hit_rate,
       round(p_ind::numeric, 3)        as hit_rate_if_no_skill,
       round((1 - p_y)::numeric, 3)    as always_bearish_hit_rate,
       round(p_y::numeric, 3)          as always_bullish_hit_rate,
       case when p_ind * (1 - p_ind) / n
                 - ((2 * p_y - 1) ^ 2 * p_z * (1 - p_z) + (2 * p_z - 1) ^ 2 * p_y * (1 - p_y)) / n > 0
            then round(((p_hat - p_ind) / sqrt(p_ind * (1 - p_ind) / n
                 - ((2 * p_y - 1) ^ 2 * p_z * (1 - p_z) + (2 * p_z - 1) ^ 2 * p_y * (1 - p_y)) / n))::numeric, 2)
       end                             as pt_statistic
from t order by days;

-- (12) how the calls and the market are spread over time (overlap check: PT assumes
--      independent pairs; two reports a day with 3-7 day windows share the same SPY move)
select date_trunc('month', run_at)::date                    as month,
       count(*)                                             as outcomes,
       count(*) filter (where lower(predicted_sentiment) = 'bearish') as bearish_calls,
       count(*) filter (where spy_change_7d > 0)            as spy_up_7d,
       count(distinct date_trunc('week', run_at))           as distinct_weeks
from prediction_outcomes
group by 1 order by 1;
