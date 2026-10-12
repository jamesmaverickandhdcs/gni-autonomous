-- S111_C_INJECT.sql - Supabase SQL Editor, read-only. Item C (injection patterns), evidence before design.
-- Run each query on its own (select it, Ctrl+Enter) and paste or screenshot each result grid.

-- (1) What Stage 1b has actually REMOVED from the stored articles, by pattern.
--     A REMOVE is silent: the article never reaches scoring. Look for real news in sample_title.
select stage1b_reason,
       count(*)                                         as removed,
       max(created_at)                                  as latest,
       (array_agg(title order by created_at desc))[1]   as sample_title
from pipeline_articles
where stage1b_passed = false
group by stage1b_reason
order by removed desc
limit 40;

-- (2) The base: how many stored articles reached Stage 1b, how many it removed, over what dates.
select count(*) filter (where stage1_passed)                              as reached_1b,
       count(*) filter (where stage1_passed and stage1b_passed = false)   as removed_1b,
       min(created_at) as first_row, max(created_at) as last_row
from pipeline_articles;

-- (3) Candidate patterns for the 7 listed attacks that pass today, tested on every stored
--     article (title + summary). A candidate is safe only if real news never matches it.
with cands(name, rx) as (values
  ('c1 you are now DAN',          'you\s+are\s+now\s+dan'),
  ('c2 repeat after me:',         'repeat\s+after\s+me\s*:'),
  ('c3 print training data',      '(print|reveal|output|show|dump)\s+(your|the)\s+(training\s+data|system\s+prompt)'),
  ('c4 as a financial advisor',   'as\s+a\s+financial\s+advisor,?\s+i\s+recommend'),
  ('c5 translate this text:',     'translate\s+this\s+text\s*:'),
  ('c6 ignore your instructions', 'ignor\w*\s+your\s+(instructions|rules|guidelines|programming)'),
  ('c7 complete this sentence',   'complete\s+this\s+sentence\s+with')
)
select c.name,
       count(a.*) filter (where (a.title || ' ' || coalesce(a.summary, '')) ~* c.rx)   as matches,
       (array_agg(a.title) filter (where (a.title || ' ' || coalesce(a.summary, '')) ~* c.rx))[1] as sample_title
from cands c cross join pipeline_articles a
group by c.name
order by c.name;
