# NO-STORE SUPABASE SWEEP — for Claude Code (S62)
Repo: C:/HDCS_Project/03/GNI_Autonomous | HEAD at spec time: e3a10c7 | Next.js 14.2.35 on Vercel
Rules in force: GNI-R-076 (read full files before patching), R-S59-1 (census before sweep),
LR-101 (pure-ASCII str-replace anchors), NO git commands — James commits himself.

## MISSION
Fix the MC-FREEZE class bug: API route handlers create supabase-js clients with no
fetch-cache opt-out. On Vercel, library-level fetches can hit the Next Data Cache even
under `export const dynamic = 'force-dynamic'`, serving fossilized query results.
Confirmed live: /api/mission-control reported a Jul-9 report as "latest" (ages
incrementing 26h -> 29h -> 31h -> 34h across runs) while the DB and the armored
/api/reports served Jul-10 data. Homepage "Pipeline: Offline" badge = same disease
via an un-armored route feeding `latestRun`.
This build armors the ENTIRE server-side Supabase data path with cache: 'no-store'.
Pure data-path change — ZERO logic changes.

## DELIVERABLE 1 — src/lib/supabaseNoStore.ts (new file, ~20 lines)
Single factory, the one place the armor lives:

    import { createClient, SupabaseClient } from '@supabase/supabase-js'

    export function createNoStoreClient(url: string, key: string): SupabaseClient {
      return createClient(url, key, {
        global: {
          fetch: (input, init) => fetch(input, { ...init, cache: 'no-store' }),
        },
      })
    }

Read package.json FIRST and adjust typing to the installed @supabase/supabase-js
version. Verify the `@/` path alias exists in tsconfig.json; if absent, plan for
relative imports in Deliverable 2.

## DELIVERABLE 2 — migrate ALL API routes using supabase-js
Census FIRST (R-S59-1) — trust your own grep, not this spec's count of 25:
    grep -rln "from '@supabase/supabase-js'" src/app/api/
For every file found:
  - Replace the supabase-js import with the factory import
    (import { createNoStoreClient } from '@/lib/supabaseNoStore')
  - Replace each `createClient(` call with `createNoStoreClient(` — arguments unchanged
  - Do NOT touch any other logic
Includes reports/ and about-stats/ (uniformity beats exceptions). Their existing
raw-fetch `cache: 'no-store'` armor STAYS as-is — only swap supabase-js client
construction where present.
ALSO census src/lib/ and src/app/**/page.tsx for server-side createClient usage:
REPORT any found; migrate only clear server-side data fetching. Do NOT touch
client-component ('use client') usage — report those, leave them alone.

## DELIVERABLE 3 — mission-control route internal fetches
In src/app/api/mission-control/route.ts, add `cache: 'no-store'` to the fetch
options of the THREE internal calls: /api/quota, /api/source-health, /api/reports.
Leave the Telegram POST fetches untouched.

## DELIVERABLE 4 — force-dynamic coverage
Every migrated route file must have `export const dynamic = 'force-dynamic'` at top.
Grep first; add ONLY where missing.

## CONSTRAINTS (hard)
- NO git commands anywhere — produce files + diff summary; James stages EXPLICITLY
  (never add -A) and commits himself.
- No new dependencies (package.json diff must be empty).
- Zero behavior/logic changes beyond the data-path armor.
- Windows Git Bash environment. Pure-ASCII anchors in any str-replace (LR-101).
- Read each route file IN FULL before editing it (GNI-R-076).

## ACCEPTANCE CHECKLIST (Claude Code self-verify before handing back)
[ ] grep -rn "createClient(" src/app/api/ returns ZERO direct supabase-js
    constructions (all via createNoStoreClient)
[ ] Every migrated route file carries `export const dynamic = 'force-dynamic'`
[ ] mission-control route: all three internal fetches carry cache: 'no-store'
[ ] npm run build passes 40/40 pages
[ ] package.json unchanged
[ ] Print final summary: files touched + insertions/deletions, so James can stage
    explicitly file-by-file
