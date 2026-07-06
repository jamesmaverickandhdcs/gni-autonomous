# S47 PROPOSAL -- Two-Account MAD Split (SCRATCH -- review before any live edit)

Goal: evening MAD (10:43 UTC = 17:43 Chiang Mai) runs on the NEW Groq account
(secret `GROQ_MAD_EVENING`, separate Gmail = separate 100K pool) so it is never
blocked by the morning account's daily tokens. Morning MAD (02:43 UTC) keeps the
existing `GROQ_API_KEY`.

Three things change. Nothing else is touched. Each shown as EXACT before/after.

==============================================================================
PART 0 -- PREREQUISITES (you do these by hand, outside the code)
==============================================================================

A. GitHub repo secret (REQUIRED -- production runs here):
     Name:  GROQ_MAD_EVENING
     Value: <the new account's Groq API key>
   Settings -> Secrets and variables -> Actions -> New repository secret.

B. .env (OPTIONAL -- only if you ever run the evening account locally):
     GROQ_MAD_EVENING=<same key>
   GitHub Actions ignores .env, so this is purely for local testing. Skip if
   you don't run MAD on your machine.

C. Supabase schema (REQUIRED -- the L2 you approved):
   Add one column to groq_daily_usage:
     ALTER TABLE groq_daily_usage
       ADD COLUMN account text NOT NULL DEFAULT 'primary';
   - DEFAULT 'primary' means every EXISTING row (all of today's history and
     past days) is treated as the morning/primary account -- no backfill needed,
     no historical row breaks.
   - New evening runs will write account='evening'.
   Run this BEFORE the code ships, so the first evening run can write the column.

==============================================================================
PART 1 -- gni_mad.yml : inject the right key per cron
==============================================================================

The job has ONE env block on the "Run GNI MAD Pipeline" step. Today it injects:

    GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}

GitHub exposes which cron fired via `github.event.schedule`, whose value is the
RAW UTC cron string. For the evening cron that string is exactly:  43 10 * * *

We branch the key on that. Also inject a GNI_MAD_ACCOUNT label so the Python
side knows which account it is using (used by the quota guard, Part 2/3).

----- BEFORE (exact lines in the step's env:) -----
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          GROQ_MODEL: ${{ secrets.GROQ_MODEL }}

----- AFTER -----
          GROQ_API_KEY: ${{ github.event.schedule == '43 10 * * *' && secrets.GROQ_MAD_EVENING || secrets.GROQ_API_KEY }}
          GNI_MAD_ACCOUNT: ${{ github.event.schedule == '43 10 * * *' && 'evening' || 'primary' }}
          GROQ_MODEL: ${{ secrets.GROQ_MODEL }}

Notes / BEV:
- The `A && B || C` form is GitHub Actions' ternary. If schedule == evening cron,
  use GROQ_MAD_EVENING; else use GROQ_API_KEY. Standard, widely used pattern.
- workflow_dispatch (manual) and the morning cron both have schedule != '43 10',
  so they fall through to GROQ_API_KEY + account='primary'. Manual evening tests
  would therefore use the MORNING key -- see OPEN QUESTION Q1 below.
- We do NOT rename GROQ_API_KEY. mad_protocol still reads GROQ_API_KEY from env;
  we're only changing WHICH secret fills it. Zero change to mad_protocol.

==============================================================================
PART 2 -- quota_guard.py : make usage account-aware
==============================================================================

PROBLEM (verified in file): get_today_usage() sums tokens_used for today across
ALL rows, unfiltered. With two accounts logging 'gni_mad' into one table, the
evening run would see the morning account's ~63K and block -- even though the
evening pool is fresh at 0. We filter by account.

--- 2a. get_today_usage: add an account filter ---

----- BEFORE -----
def get_today_usage(client) -> int:
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        result = client.table('groq_daily_usage') \
            .select('tokens_used') \
            .eq('usage_date', today) \
            .execute()
        total = sum(row['tokens_used'] for row in (result.data or []))
        return total
    except Exception as e:
        print('  ERROR reading groq_daily_usage: ' + str(e)[:80])
        return -1

----- AFTER -----
def get_today_usage(client, account: str = 'primary') -> int:
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        result = client.table('groq_daily_usage') \
            .select('tokens_used') \
            .eq('usage_date', today) \
            .eq('account', account) \
            .execute()
        total = sum(row['tokens_used'] for row in (result.data or []))
        return total
    except Exception as e:
        print('  ERROR reading groq_daily_usage: ' + str(e)[:80])
        return -1

--- 2b. log_usage: stamp the account on every write ---

----- BEFORE -----
def log_usage(client, pipeline: str, tokens_used: int,
              requests_used: int, run_id: str = None,
              reason: str = '') -> bool:
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        client.table('groq_daily_usage').insert({
            'usage_date':    today,
            'pipeline':      pipeline,
            'tokens_used':   tokens_used,
            'requests_used': requests_used,
            'run_id':        run_id or '',
            'reason':        reason or '',
        }).execute()

----- AFTER -----
def log_usage(client, pipeline: str, tokens_used: int,
              requests_used: int, run_id: str = None,
              reason: str = '', account: str = 'primary') -> bool:
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        client.table('groq_daily_usage').insert({
            'usage_date':    today,
            'pipeline':      pipeline,
            'tokens_used':   tokens_used,
            'requests_used': requests_used,
            'run_id':        run_id or '',
            'reason':        reason or '',
            'account':       account,
        }).execute()

--- 2c. check_quota: accept account, pass it to get_today_usage ---

----- BEFORE -----
def check_quota(pipeline: str, sacred: bool = False) -> dict:
    client = _get_supabase_client()
    if not client:
        return { ... }                       # (unchanged dict)

    tokens_used = get_today_usage(client)
    pipeline_cost = PIPELINE_COSTS.get(pipeline, 0)

----- AFTER -----
def check_quota(pipeline: str, sacred: bool = False, account: str = 'primary') -> dict:
    client = _get_supabase_client()
    if not client:
        return { ... }                       # (unchanged dict)

    tokens_used = get_today_usage(client, account)
    pipeline_cost = PIPELINE_COSTS.get(pipeline, 0)

  BEV note: every other line of check_quota is untouched. Only the signature
  and the single get_today_usage call change. The sacred/non-sacred logic,
  ceilings, alerts -- all identical.

--- 2d. print_status: default account view (cosmetic, keeps CLI working) ---
   get_today_usage(client) call inside print_status() becomes
   get_today_usage(client, 'primary'). Optional this session; flag only.

==============================================================================
PART 3 -- mad_runner.py : read the account label, thread it through
==============================================================================

mad_runner calls check_quota and log_usage. Both need the account label, read
from the GNI_MAD_ACCOUNT env var the yml now sets. Default 'primary' so the
morning run and any local run behave exactly as today.

--- 3a. read the label once, near the top of run_mad_pipeline() ---

----- ADD (right after `client = _get_client()` succeeds) -----
    mad_account = os.getenv('GNI_MAD_ACCOUNT', 'primary')
    print('  MAD account: ' + mad_account)

--- 3b. quota check passes the account ---

----- BEFORE -----
    _quota = check_quota('gni_mad', sacred=False)

----- AFTER -----
    _quota = check_quota('gni_mad', sacred=False, account=mad_account)

--- 3c. usage log stamps the account ---

----- BEFORE -----
            log_usage(_sb, 'gni_mad', _real_tokens, _usage['calls'], report_id or '')

----- AFTER -----
            log_usage(_sb, 'gni_mad', _real_tokens, _usage['calls'], report_id or '',
                      account=mad_account)

  BEV note: log_usage's 5th positional arg is run_id, 'reason' is 6th. We pass
  account as a KEYWORD to avoid colliding with the empty reason default. Verified
  against the live signature in Part 2b.

==============================================================================
WHAT WE ARE NOT CHANGING THIS SESSION (honest parking)
==============================================================================

- PIPELINE_COSTS['gni_mad'] = 7433 stays stale (real ~63005). The split makes
  the block moot for the evening account, but the morning account can still
  mis-gate on the bad estimate. CORRECTING 7433 + adding the divergence
  ASSERTION (Treasure 3) is a SEPARATE commit -- do NOT fold it in here; it
  changes morning behavior and deserves its own BEV + dry run. Banked as the
  immediate next step after this lands.
- PIPELINE_RESERVATIONS comment math (still cites 7433) -- same parking.
- Pipeline itself stays single-account (only ~6175/run; no pressure).

==============================================================================
OPEN QUESTIONS FOR JAMES (answer before wiring)
==============================================================================

Q1. Manual evening test: with the Part-1 branch, a workflow_dispatch run always
    uses the MORNING key (schedule is empty on manual runs). If you want to
    manually test the EVENING account, options:
      (a) accept it -- manual = morning only; evening proven by the real 10:43
          cron tomorrow; OR
      (b) add a workflow_dispatch input 'account' (morning/evening) that
          overrides the branch for manual runs only.
    My lean: (a) for THIS commit -- smallest surface, and the real cron is the
    true test. Add (b) later only if manual evening testing becomes a need.

Q2. Column name/values: I've used column `account` with values 'primary' /
    'evening'. Alternative naming if you prefer ('morning'/'evening', or the
    secret-style 'default'/'mad_evening'). Your call -- whatever you pick, it
    must match the ALTER TABLE default in Part 0C and the yml label in Part 1.

==============================================================================
SEQUENCE ONCE APPROVED
==============================================================================

1. You: add GROQ_MAD_EVENING GitHub secret (Part 0A).
2. You: run the ALTER TABLE on groq_daily_usage (Part 0C).
3. Me: ship-to-file patches (LR-078) for gni_mad.yml, quota_guard.py,
   mad_runner.py -- pure ASCII anchors (LR-101).
4. py_compile both .py files (W2).
5. Offline dry-run harness (dummy key, GITHUB_ACTIONS=true, monkeypatched
   client) -- assert: primary path reads/writes account='primary'; evening
   path reads/writes account='evening'; get_today_usage filters correctly.
6. git push origin main -> git ls-remote origin main to confirm hash.
7. Watch the real 02:43 (primary) and 10:43 (evening) crons land tomorrow;
   confirm groq_daily_usage shows two account values, evening pool independent.
