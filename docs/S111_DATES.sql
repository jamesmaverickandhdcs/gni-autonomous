-- S111_DATES.sql - Supabase SQL Editor, read-only. Run each query on its own (select it, Ctrl+Enter).
-- (1) Which first-prediction date is true? /reports says "April 10, 2026"; /validation-log says the
--     earliest MAD predictions were made in March 2026 with verify dates "starting April 14, 2026".
select min(created_at) as first_made, min(verify_by) as first_verify_by,
       count(*) filter (where created_at < '2026-04-01') as made_in_march
from debate_predictions;

-- (2) The /comparison screenshot showed MAD confidence 53% on 9 of the last 10 debates.
--     Is 0.53 the Arbitrator's real spread, or a value it keeps repeating?
select round(mad_confidence::numeric, 2) as confidence, count(*) as reports
from reports
where mad_confidence is not null and created_at > now() - interval '60 days'
group by 1 order by 2 desc limit 8;
