-- S111_EXPORT7b.sql - Supabase SQL Editor, read-only. Replaces S111_EXPORT7.sql.
-- Why: the SQL Editor's result grid stops at 100 rows, so the two CSVs held only 2026-05-24..07-12
-- (100 of 274 outcomes, 100 of ~290 reports). This query returns ONE row: each column is a
-- whole CSV file as text, so nothing is cut. Download the result as CSV and upload it as
-- S111_B_full.csv.
select
  (select count(*) from prediction_outcomes)                                as outcome_rows,
  (select count(*) from reports)                                            as report_rows,
  (select string_agg(format('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s',
            p.report_id, r.created_at, r.sentiment, r.sentiment_score, r.escalation_score,
            r.escalation_score_raw, r.risk_level, p.spy_change_3d, p.spy_change_7d,
            p.spy_change_30d, p.black_swan_flag), E'\n' order by r.created_at)
     from prediction_outcomes p join reports r on r.id = p.report_id)       as outcomes_csv,
  (select string_agg(format('%s,%s,%s,%s,%s,%s',
            id, created_at, escalation_score, escalation_score_raw, sentiment_score, risk_level),
            E'\n' order by created_at)
     from reports)                                                          as reports_csv;
