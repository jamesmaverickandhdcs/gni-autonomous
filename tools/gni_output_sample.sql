-- tools/gni_output_sample.sql - S114, roadmap 5 row R5-1 (docs/GNI_ROADMAP5_SPEC_S113.md, section 3).
-- READ-ONLY. One statement, ONE row, ONE cell - the S112 snapshot pattern (DECISION S112-4).
-- Copy the cell AS TEXT into a file and give it to tools/gni_output_sample.py, which writes
-- docs/gni_output_sample_S<N>.json and REFUSES a copy that lost a row or a character: every
-- output carries the md5 of its five published texts, computed here by Postgres.
--
-- WHAT IS SAMPLED. The published text of every report in the window: title, summary and the three
-- Freedom from Fear sections. These are what /brief renders (through /api/reports) and what every
-- Telegram report carries. Reports come from the main pipeline only; the adaptive run writes none.
-- pillar_reports also store the three sections, and no page renders them: not sampled.
--
-- THE WINDOW is the operator's ruling (spec section 5). It is a closed window in the past, so the
-- sample never goes stale (DECISION S90-3). Both bounds sit on the next two lines and nowhere else.
with win as (
  select timestamptz '2026-08-31 09:02:39+00' as t0,   -- fd43129: the last change to the report-writing code
         timestamptz '2026-10-14 00:00:00+00' as t1    -- exclusive
), r as (
  select r.id, r.created_at, r.title, r.summary,
         r.fff_what_is_happening, r.fff_honest_analysis, r.fff_human_path,
         r.sentiment, r.risk_level, r.escalation_level, r.llm_source,
         (select p.pipeline_type from pipeline_runs p where p.report_id = r.id limit 1) as pipeline_type
  from reports r, win
  where r.created_at >= win.t0 and r.created_at < win.t1
)
select json_build_object(
  'harvested_at', now(),
  'window', (select json_build_object('from', t0, 'to', t1) from win),
  'rows', (select count(*) from r),
  'empty', json_build_object(
    'summary',               (select count(*) from r where coalesce(btrim(summary), '') = ''),
    'fff_what_is_happening', (select count(*) from r where coalesce(btrim(fff_what_is_happening), '') = ''),
    'fff_honest_analysis',   (select count(*) from r where coalesce(btrim(fff_honest_analysis), '') = ''),
    'fff_human_path',        (select count(*) from r where coalesce(btrim(fff_human_path), '') = '')),
  -- A report row does not store its model. A fallback model is written to the audit trail
  -- (main.py, GROQ_MODEL_FALLBACK_ACTIVE); every such event in the window is listed here.
  'fallback_events', (select coalesce(json_agg(json_build_object('created_at', a.created_at,
                                                                  'event_data', a.event_data)
                                               order by a.created_at), '[]'::json)
                      from audit_trail a, win
                      where a.event_type = 'GROQ_MODEL_FALLBACK_ACTIVE'
                        and a.created_at >= win.t0 and a.created_at < win.t1),
  'outputs', (select coalesce(json_agg(json_build_object(
                'id', id, 'created_at', created_at, 'pipeline_type', pipeline_type,
                'llm_source', llm_source, 'sentiment', sentiment, 'risk_level', risk_level,
                'escalation_level', escalation_level,
                'title', title, 'summary', summary,
                'fff_what_is_happening', fff_what_is_happening,
                'fff_honest_analysis', fff_honest_analysis,
                'fff_human_path', fff_human_path,
                'md5', md5(concat_ws(chr(31), coalesce(title, ''), coalesce(summary, ''),
                                     coalesce(fff_what_is_happening, ''),
                                     coalesce(fff_honest_analysis, ''),
                                     coalesce(fff_human_path, ''))))
              order by created_at), '[]'::json)
              from r)
) as sample;
