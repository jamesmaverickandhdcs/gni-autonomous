-- tools/gni_db_harvest.sql - S112 (DECISION S112-4, design docs/S112_RUNTIME_SNAPSHOT_DESIGN.md); R9 adds one fact.
-- READ-ONLY. One statement, ONE row, ONE cell: copy the cell into docs/gni_db_snapshot_S<N>.json.
-- Every fact carries the row count of the set it was computed from (R-S111-3). DATED facts only:
-- a closed window in the past, so the figure never goes stale (DECISION S90-3: a published figure
-- carries the window that produced it).
with aug as (
  select pipeline, tokens_used
  from groq_daily_usage
  where usage_date >= date '2026-08-01' and usage_date < date '2026-09-01'
)
select json_build_object(
  'harvested_at', now(),
  'facts', json_build_array(
    (select json_build_object('id', 'groq-tokens-' || pipeline || '-2026-08', 'kind', 'dated',
                              'window', '2026-08-01/2026-09-01', 'rows', count(*),
                              'value', json_build_object('mean', round(avg(tokens_used)), 'n', count(*),
                                                         'min', min(tokens_used), 'max', max(tokens_used)))
     from aug where pipeline = 'gni_pipeline' group by pipeline),
    (select json_build_object('id', 'groq-tokens-' || pipeline || '-2026-08', 'kind', 'dated',
                              'window', '2026-08-01/2026-09-01', 'rows', count(*),
                              'value', json_build_object('mean', round(avg(tokens_used)), 'n', count(*),
                                                         'min', min(tokens_used), 'max', max(tokens_used)))
     from aug where pipeline = 'gni_mad' group by pipeline),
    -- S112 R9: when report-level GPVS verification began (CLM-894 said "live since April 2026"). The
    -- first harvest (2026-10-12T21:00Z) read ZERO prediction_outcomes rows created before 2026-05-01,
    -- with the created_at column present, so the window is widened to end 2026-10-01: still closed
    -- and in the past, so its first row does not change. created_at is read through to_jsonb so the
    -- query cannot fail on a missing column; 'columns' reports whether it exists, and run_at (the
    -- REPORT's date, which precedes its verification) is never used in its place.
    (select json_build_object('id', 'gpvs-report-outcomes-first', 'kind', 'dated',
                              'window', '-/2026-10-01', 'rows', count(*),
                              'value', json_build_object('first_created_at', min(c), 'n', count(*)))
     from (select (to_jsonb(o) ->> 'created_at')::timestamptz as c from prediction_outcomes o) po
     where c < timestamptz '2026-10-01 00:00:00+00'),
    -- The first report the database holds, in the same window: if it is earlier than the first
    -- verification, the database is older than verification and the gap is not a lost history.
    (select json_build_object('id', 'reports-first', 'kind', 'dated',
                              'window', '-/2026-10-01', 'rows', count(*),
                              'value', json_build_object('first_created_at', min(created_at), 'n', count(*)))
     from reports where created_at < timestamptz '2026-10-01 00:00:00+00')
  ),
  'pipelines_in_window', (select json_object_agg(pipeline, n) from (select pipeline, count(*) as n from aug group by pipeline) p),
  'columns', json_build_object('prediction_outcomes.created_at',
    exists (select 1 from information_schema.columns where table_schema = 'public'
            and table_name = 'prediction_outcomes' and column_name = 'created_at'))
) as snapshot;
