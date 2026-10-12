-- S111_C_INJECT2.sql - Supabase SQL Editor, read-only. Item C, second read: NARROWED versions of the
-- patterns that removed real news in S111_C_INJECT.sql (1). Run each query on its own.

-- (4) Each narrowed pattern on EVERY stored article (title + summary). A narrowed pattern is
--     acceptable only if its matches are near zero and its sample is not ordinary news.
with cands(name, rx) as (values
  ('n1 act as an AI',          'act\s+as\s+(a|an)\s+(ai|assistant|chatbot|language\s+model|unrestricted|unfiltered)\y'),
  ('n2 jailbreak mode/prompt', '(jailbreak\s+(mode|prompt)|jailbroken\s+(ai|model|assistant|mode))'),
  ('n3 pretend you are an AI', 'pretend\s+(you\s+are|to\s+be)\s+(an?\s+)?(ai|assistant|chatbot|unrestricted|unfiltered|dan)\y'),
  ('n4 bypass your safety',    '(bypass|circumvent|override)\s+(your|its)\s+(safety|filter|restriction|guideline)'),
  ('n5 send secret to URL',    '(send|post|paste|enter|submit|upload)\s+.{0,30}(api.key|password|token|secret).{0,30}https?://'),
  ('n6 you are now DAN/AI',    'you\s+are\s+now\s+(a\s+)?(dan|jailbroken|unrestricted|unfiltered|in\s+developer\s+mode)\y')
)
select c.name,
       count(a.*) filter (where (a.title || ' ' || coalesce(a.summary, '')) ~* c.rx)   as matches,
       (array_agg(a.title) filter (where (a.title || ' ' || coalesce(a.summary, '')) ~* c.rx))[1] as sample_title
from cands c cross join pipeline_articles a
group by c.name
order by c.name;

-- (5) The articles the CURRENT patterns removed since 2026-06-16 (after the S44 exfil fix), by
--     pattern, with three titles each - to judge whether any was a real injection.
select stage1b_reason, count(*) as removed,
       (array_agg(title order by created_at desc))[1:3] as three_titles
from pipeline_articles
where stage1b_passed = false
  and stage1b_reason like 'Injection pattern:%'
  and created_at >= '2026-06-16'
group by stage1b_reason
order by removed desc;
