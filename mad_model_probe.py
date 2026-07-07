# ============================================================
# mad_model_probe.py -- U3 PROBE HARNESS (S56 build, S57 rebuild, standalone, read-only)
# Purpose: baseline the dying llama-3.3-70b-versatile Arbitrator behavior
#          BEFORE Aug 16, and profile candidate models (gpt-oss-120b etc.)
#          on the REAL 12-key Arbitrator JSON contract + token economics.
# Fidelity: imports the byte-exact ARB_FINAL system prompt from
#           ai_engine/analysis/mad_protocol.py (SENIOR_FOUNDATION +
#           GROUNDING_RULE included). Parse logic below is a byte-faithful
#           copy of the production path (fence-strip + brace-fallback).
# S57 note: original S56 file was never saved to disk; this rebuild is
#           byte-faithful from the S56 session archive EXCEPT FIXTURE_USER,
#           which is a fresh freeze (spec-faithful, never previously fired --
#           frozen from this file's first run onward).
# Cost:     ~3-4K prompt tokens per call. Default = 3 trials, 1 model.
#           NEVER run this on the morning/evening MAD accounts near red
#           line, and NEVER on not_mad (reserved -- James's ruling).
# Key:      read from GROQ_API_KEY env var, or --keyfile <path> (file is
#           never echoed; keep it out of shell history and .gitignore'd).
# Run:      python mad_model_probe.py                       # llama baseline x3
#           python mad_model_probe.py --model openai/gpt-oss-120b --trials 3
#           python mad_model_probe.py --model openai/gpt-oss-120b --max-tokens 1200
# Output:   probe_results.jsonl (raw dumps, append) + summary table (stdout)
# ============================================================
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

# --- locate repo root so mad_protocol imports resolve -------------
_HERE = os.path.dirname(os.path.abspath(__file__))
for _cand in (_HERE, os.path.dirname(_HERE)):
    if os.path.isdir(os.path.join(_cand, 'ai_engine')):
        sys.path.insert(0, _cand)
        break

VALID_VERDICTS = {'bullish', 'bearish', 'neutral'}
SCHEMA_KEYS = [
    'verdict', 'confidence', 'reasoning',
    'blind_spot_quadrant', 'blind_spot_explanation',
    'action_recommendation',
    'short_focus_threats', 'short_verify_days',
    'long_shoot_threats', 'long_verify_days',
    'short_focus_opportunities', 'preparedness_path',
]

# --- FROZEN FIXTURE: realistic arb_final_user shape ----------------
# Same bytes every run/model => fair comparison. Mirrors production
# assembly: ctx + R1/R2 summaries + R3 fulls + escalation + pillar line.
# FROZEN as of S57 first run. DO NOT EDIT after any trial has been fired.
FIXTURE_USER = (
    "INTELLIGENCE SUMMARY (22 articles, GEO-dominant):\n"
    "Regional tensions escalate around the Strait of Hormuz following a "
    "leadership transition in Iran. Naval assets reposition; maritime "
    "insurers raise war-risk premiums 40%. NATO summit convenes amid "
    "allied disagreement on response posture. Oil futures volatile: Brent "
    "swung 6% intraday. Central banks signal readiness to provide dollar "
    "liquidity. Separately: a major cloud provider disclosed a supply-chain "
    "compromise affecting defense contractors; attribution contested. "
    "Sovereign debt spreads widen across emerging markets exposed to "
    "energy import costs. Low-scoring signals: unusual grain-shipment "
    "rerouting through the Cape; a mid-tier chipmaker halted exports "
    "pending license review; three regional carriers suspended Gulf "
    "overflights citing insurance costs.\n\n"
    "FULL DEBATE TRANSCRIPT:\n\n"
    "=== ROUND 1 (summary) ===\n"
    "Bull: Energy shock is priced in; defense and logistics sectors gain. "
    "Dollar liquidity backstops cap tail risk. Opportunity in reshoring plays.\n"
    "Bear: Insurance repricing is the tell -- physical trade disruption is "
    "beginning, not ending. Earnings revisions lag reality by a quarter.\n"
    "Black Swan: The chipmaker export halt is the ignored signal. If licensing "
    "seizes up, the tech pillar inherits the geo shock with a 60-day lag.\n"
    "Ostrich: Markets ignore the overflight suspensions. Institutions in denial: "
    "airline hedging desks and tourism-dependent sovereigns.\n\n"
    "=== ROUND 2 (summary) ===\n"
    "Bull: Concedes near-term chop; maintains 3-6 month constructive view on "
    "liquidity support and inventory buffers at 2019 highs.\n"
    "Bear: Sharpens: war-risk premium at 40% historically precedes 2-3% SPY "
    "drawdown within 10 sessions; consensus underweights second-order credit.\n"
    "Black Swan: Links grain rerouting + chip halt: dual-chokepoint stress is "
    "the unmodeled correlation. Names verify window 21 days.\n"
    "Ostrich: The denial has a cost: every week of ignored overflight data adds "
    "basis-point drag to Gulf-exposed sovereign spreads.\n\n"
    "=== ROUND 3 (final positions) ===\n"
    "Bull: Final -- neutral-to-constructive. The liquidity backstop plus full "
    "strategic reserves cap downside at correction, not crisis. Watch reserve "
    "release announcements as the confirming signal within 14 days. The "
    "reshoring and defense-logistics complex outperforms on any resolution.\n"
    "Bear: Final -- bearish with conviction. Insurance and freight repricing "
    "lead equities by 5-10 sessions and both are still deteriorating. Credit "
    "spreads in energy-importing EMs are the transmission channel. Expect "
    "risk-off rotation and a 2-3% index drawdown inside 10 sessions.\n"
    "Black Swan: Final -- the correlated chokepoint scenario deserves 15% "
    "probability, up from consensus 3%. If Hormuz friction and chip-license "
    "seizure overlap for 30+ days, the shock migrates from energy to hardware "
    "supply chains and no current hedge structure covers both.\n"
    "Ostrich: Final -- the specific ignored threat is Gulf overflight economics. "
    "Named institutions in denial: sovereign wealth funds still marked to "
    "pre-crisis tourism projections. Cost of inaction compounds weekly and "
    "repricing will be abrupt, not gradual.\n\n"
    "Current escalation: CRITICAL (10.0/10) | Risk: High\n"
    "PILLAR WEIGHTING -- GEOPOLITICAL DOMINANT: weigh GEO evidence first.\n\n"
    "Deliver your final synthesis as JSON only."
)


def _load_key(args) -> str:
    if args.keyfile:
        with open(args.keyfile, 'r', encoding='utf-8') as f:
            return f.read().strip()
    key = os.getenv('GROQ_API_KEY', '').strip()
    if not key:
        sys.exit('FATAL: no key. Set GROQ_API_KEY or pass --keyfile <path>.')
    return key


def _production_parse(raw: str) -> dict:
    """Byte-faithful copy of mad_protocol.py final-parse path."""
    out = {'parse_ok': False, 'parse_error': '', 'json': None,
           'fence_stripped': ('```' in raw), 'brace_fallback': False}
    clean = raw.replace('```json', '').replace('```', '').strip()
    try:
        try:
            out['json'] = json.loads(clean)
        except json.JSONDecodeError:
            start = clean.find('{')
            end = clean.rfind('}') + 1
            if start >= 0 and end > start:
                out['json'] = json.loads(clean[start:end])
                out['brace_fallback'] = True
            else:
                raise json.JSONDecodeError('No JSON object found', clean, 0)
        out['parse_ok'] = True
    except (json.JSONDecodeError, ValueError) as e:
        out['parse_error'] = str(e)[:120]
    return out


def _field_audit(j: dict) -> dict:
    present = [k for k in SCHEMA_KEYS if k in j and j[k] not in (None, '')]
    audit = {
        'fields_present': len(present),
        'fields_total': len(SCHEMA_KEYS),
        'missing': [k for k in SCHEMA_KEYS if k not in present],
        'verdict_valid': str(j.get('verdict', '')).lower() in VALID_VERDICTS,
        'confidence_ok': False,
        'confidence_in_band': False,   # prompt demands 0.40-1.00
    }
    try:
        c = float(j.get('confidence', -1))
        audit['confidence_ok'] = 0.0 <= c <= 1.0
        audit['confidence_in_band'] = 0.40 <= c <= 1.00
    except (TypeError, ValueError):
        pass
    return audit


def _dig(obj, *path):
    """Defensive nested getattr/dict-get for usage detail extraction."""
    cur = obj
    for p in path:
        if cur is None:
            return None
        cur = cur.get(p) if isinstance(cur, dict) else getattr(cur, p, None)
    return cur


def run_trial(client, model: str, arb_final: str, max_tokens: int, trial: int) -> dict:
    rec = {'ts': datetime.now(timezone.utc).isoformat(), 'model': model,
           'trial': trial, 'max_tokens': max_tokens}
    t0 = time.time()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': arb_final},
                {'role': 'user', 'content': FIXTURE_USER},
            ],
            max_tokens=max_tokens,
            temperature=0.7,           # production value -- do not change
        )
    except Exception as e:
        rec.update({'ok': False, 'error': str(e)[:300],
                    'latency_s': round(time.time() - t0, 2)})
        return rec
    rec['latency_s'] = round(time.time() - t0, 2)
    rec['ok'] = True

    choice = resp.choices[0]
    msg = choice.message
    content = (msg.content or '').strip()
    rec['finish_reason'] = getattr(choice, 'finish_reason', None)
    rec['content_chars'] = len(content)
    rec['content_head'] = content[:200]

    # reasoning capture (gpt-oss on Groq may expose message.reasoning
    # and/or usage.completion_tokens_details.reasoning_tokens)
    reasoning_txt = getattr(msg, 'reasoning', None)
    rec['reasoning_chars'] = len(reasoning_txt) if reasoning_txt else 0

    u = getattr(resp, 'usage', None)
    rec['usage'] = {
        'prompt': _dig(u, 'prompt_tokens'),
        'completion': _dig(u, 'completion_tokens'),
        'total': _dig(u, 'total_tokens'),
        'reasoning': _dig(u, 'completion_tokens_details', 'reasoning_tokens'),
    }

    parse = _production_parse(content)
    rec['parse'] = {k: v for k, v in parse.items() if k != 'json'}
    if parse['parse_ok']:
        rec['field_audit'] = _field_audit(parse['json'])
        rec['verdict'] = parse['json'].get('verdict')
        rec['confidence'] = parse['json'].get('confidence')

    # full raw dump so NOTHING is lost for later forensics
    try:
        rec['raw_response'] = resp.model_dump()
    except Exception:
        rec['raw_response'] = None
    return rec


def main():
    ap = argparse.ArgumentParser(description='U3 MAD Arbitrator model probe')
    ap.add_argument('--model', default='llama-3.3-70b-versatile',
                    help='Groq model id (verify candidate ids on Groq models page first)')
    ap.add_argument('--trials', type=int, default=3)
    ap.add_argument('--max-tokens', type=int, default=600,
                    help='production=600; sweep upward for reasoning models')
    ap.add_argument('--keyfile', default=None,
                    help='path to file containing the API key (preferred over shell env)')
    ap.add_argument('--out', default='probe_results.jsonl')
    ap.add_argument('--gap', type=float, default=20.0,
                    help='seconds between trials (TPM kindness)')
    args = ap.parse_args()

    key = _load_key(args)

    # import AFTER key load so a bad key fails fast, before heavy imports
    try:
        from ai_engine.analysis.mad_protocol import ARB_FINAL as arb_final
        prompt_source = 'imported from mad_protocol (byte-exact)'
    except Exception as e:
        sys.exit('FATAL: could not import ARB_FINAL from mad_protocol '
                 '(' + str(e)[:200] + ')\n'
                 'Fidelity rule: we do NOT reconstruct the prompt from memory. '
                 'Fix the import path/deps and rerun.')

    from groq import Groq
    client = Groq(api_key=key, max_retries=0)

    print('=== U3 PROBE ===')
    print('model=' + args.model + ' trials=' + str(args.trials) +
          ' max_tokens=' + str(args.max_tokens))
    print('system prompt: ' + prompt_source + ' (' + str(len(arb_final)) + ' chars)')
    print('fixture user prompt: ' + str(len(FIXTURE_USER)) + ' chars (frozen)')

    rows = []
    with open(args.out, 'a', encoding='utf-8') as f:
        for t in range(1, args.trials + 1):
            print('--- trial ' + str(t) + '/' + str(args.trials) + ' ---')
            rec = run_trial(client, args.model, arb_final, args.max_tokens, t)
            f.write(json.dumps(rec, default=str) + '\n')
            f.flush()
            rows.append(rec)
            if rec.get('ok'):
                fa = rec.get('field_audit', {})
                print('  finish=' + str(rec['finish_reason']) +
                      ' | parse=' + str(rec['parse']['parse_ok']) +
                      ' | fields=' + str(fa.get('fields_present', '-')) + '/12' +
                      ' | verdict=' + str(rec.get('verdict')) +
                      ' | conf=' + str(rec.get('confidence')))
                print('  tokens p/c/r=' + str(rec['usage']['prompt']) + '/' +
                      str(rec['usage']['completion']) + '/' +
                      str(rec['usage']['reasoning']) +
                      ' | reasoning_chars=' + str(rec['reasoning_chars']) +
                      ' | ' + str(rec['latency_s']) + 's')
            else:
                print('  ERROR: ' + rec.get('error', '?'))
            if t < args.trials:
                time.sleep(args.gap)

    ok = [r for r in rows if r.get('ok')]
    parsed = [r for r in ok if r.get('parse', {}).get('parse_ok')]
    full12 = [r for r in parsed
              if r.get('field_audit', {}).get('fields_present') == 12]
    trunc = [r for r in ok if r.get('finish_reason') == 'length']
    print('=== SUMMARY: ' + args.model + ' @ max_tokens=' + str(args.max_tokens) + ' ===')
    print('calls ok        : ' + str(len(ok)) + '/' + str(len(rows)))
    print('json parsed     : ' + str(len(parsed)) + '/' + str(len(ok) or 1))
    print('all 12 fields   : ' + str(len(full12)) + '/' + str(len(parsed) or 1))
    print('finish==length  : ' + str(len(trunc)) + '  <-- truncation = P5 threat signal')
    if ok:
        comp = [r['usage']['completion'] for r in ok if r['usage']['completion']]
        rsn = [r['usage']['reasoning'] for r in ok if r['usage']['reasoning']]
        if comp:
            print('completion tok  : min ' + str(min(comp)) + ' / max ' + str(max(comp)))
        print('reasoning tok   : ' + (str(rsn) if rsn else 'none reported'))
    print('raw dumps -> ' + args.out)
    print('=== DONE U3 PROBE ===')


if __name__ == '__main__':
    main()
