-- tools/gni_db_harvest.sql - S112 (DECISION S112-4, design docs/S112_RUNTIME_SNAPSHOT_DESIGN.md).
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
     from aug where pipeline = 'gni_mad' group by pipeline)
  ),
  'pipelines_in_window', (select json_object_agg(pipeline, n) from (select pipeline, count(*) as n from aug group by pipeline) p)
) as snapshot;
