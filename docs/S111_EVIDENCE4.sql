-- S111_EVIDENCE4.sql - Supabase SQL Editor, read-only. Item A, second half. Run each query on its own.
-- The report prompt defines sentiment "for markets" and its own example says tickers_affected ["SPY", "GLD"].
-- The direction check then judges a Bearish (markets down) call on GLD when GLD is listed and USO/XOM is not.
-- Gold is often bought when markets fall, so a correct "markets down" call can be marked wrong on GLD.

-- (9) Which instrument each report's direction is judged on, and how many are Bearish.
select case when r.tickers_affected::text ~* '\m(USO|XOM)\M' then 'USO'
            when r.tickers_affected::text ~* '\mGLD\M'      then 'GLD'
            else 'SPY' end                                       as primary_inst,
       count(*)                                                  as reports,
       count(*) filter (where r.sentiment = 'Bearish')           as bearish,
       count(*) filter (where r.sentiment = 'Bullish')           as bullish
from reports r
group by 1
order by 1;

-- (10) On GLD-judged Bearish outcomes: how often SPY fell (call right for "markets")
--      while GLD rose (call marked wrong on the instrument it was judged on).
select count(*)                                                              as gld_bearish_rows,
       count(*) filter (where o.spy_change_3d < 0)                           as spy_down_3d,
       count(*) filter (where o.spy_change_3d < 0 and o.gld_change_3d > 0)   as spy_down_gld_up_3d,
       count(*) filter (where o.spy_change_7d < 0 and o.gld_change_7d > 0)   as spy_down_gld_up_7d,
       count(*) filter (where o.direction_correct_3d is false)               as marked_wrong_3d
from prediction_outcomes o
join reports r on r.id = o.report_id
where lower(o.predicted_sentiment) = 'bearish'
  and r.tickers_affected::text !~* '\m(USO|XOM)\M'
  and r.tickers_affected::text ~*  '\mGLD\M';
