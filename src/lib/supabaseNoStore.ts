import { createClient, SupabaseClient } from '@supabase/supabase-js'

// MC-FREEZE armor (S62): a single Supabase factory that forces every
// library-level fetch to bypass the Next.js Data Cache. On Vercel,
// supabase-js fetches can be cached even under `dynamic = 'force-dynamic'`,
// serving fossilized query results. `cache: 'no-store'` opts every query out.
// Pure data-path change -- zero logic changes at call sites.
export function createNoStoreClient(url: string, key: string): SupabaseClient {
  return createClient(url, key, {
    global: {
      fetch: (input, init) => fetch(input, { ...init, cache: 'no-store' }),
    },
  })
}
