import os
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.supabase_saver import get_client

# ============================================================
# GNI Dynamic Source Weighting — Day 1
# Weights stored in Supabase source_weights table
# Updated based on GPVS contribution per source
# ============================================================

# Default weights — fallback ONLY, for when Supabase is unreachable.
# Not a seed roster: seeding derives from the collector's canonical roster
# (see get_roster_sources / seed_roster_weights).
DEFAULT_WEIGHTS = {
    'al jazeera':  1.3,
    'bbc':         1.3,
    'dw news':     1.2,
    'reuters':     1.3,
    'cnn':         1.0,
    'fox news':    0.9,
}

_weight_cache: dict | None = None
_cache_loaded_at: str | None = None


def norm(source: str) -> str:
    """
    Canonical source key — one spelling per source, everywhere.
    Both writers and the funnel reader key on this. Case-dup rows ("BBC" vs
    "bbc") are what made the weight column nondeterministic (I-4).
    """
    return source.strip().lower()


def get_roster_sources() -> list:
    """
    The canonical live roster, imported from the collector — never copied.
    The collector is the single source of truth for who is on the roster;
    a second hand-maintained list is how the 13-source fossil drifted (I-6).
    """
    from collectors.rss_collector import SOURCES
    return [s["name"] for s in SOURCES]


def get_source_weights(force_refresh: bool = False) -> dict:
    """
    Load source weights from Supabase.
    Cached in memory for the session. Returns dict of {source: weight}.
    Falls back to DEFAULT_WEIGHTS if Supabase unavailable.
    """
    global _weight_cache, _cache_loaded_at

    if _weight_cache and not force_refresh:
        return _weight_cache

    client = get_client()
    if not client:
        print("  ⚠️  Source weights: using defaults (no Supabase)")
        return DEFAULT_WEIGHTS.copy()

    try:
        result = client.table('source_weights').select('*').execute()
        rows = result.data or []

        if not rows:
            # First run — seed the canonical roster into Supabase
            print("  📥 Source weights: seeding roster into Supabase...")
            seeded = seed_roster_weights(client)
            if seeded:
                _weight_cache = {norm(s): 1.0 for s in get_roster_sources()}
            else:
                _weight_cache = DEFAULT_WEIGHTS.copy()
        else:
            _weight_cache = {norm(r['source']): r['weight'] for r in rows}
            print(f"  ✅ Source weights loaded: {len(_weight_cache)} sources")

        _cache_loaded_at = datetime.now(timezone.utc).isoformat()
        return _weight_cache

    except Exception as e:
        print(f"  ⚠️  Source weights fetch failed: {e} — using defaults")
        return DEFAULT_WEIGHTS.copy()


def seed_roster_weights(client=None) -> int:
    """
    Insert-if-missing neutral (1.0) weight rows for every source on the
    canonical roster (I-6). Returns the number of rows seeded.

    INSERT-only by design: an existing row carries learned EMA history, and a
    seed pass must never reset it to neutral.

    This module owns the weight column (writer A / the GPVS EMA path).
    credibility_model delegates roster weight-seeding here rather than writing
    source_weights itself — single-writer principle, bridge (a).
    """
    client = client or get_client()
    if not client:
        return 0

    try:
        roster = {norm(s) for s in get_roster_sources()}
        existing = client.table('source_weights').select('source').execute()
        have = {norm(r['source']) for r in (existing.data or [])}
        missing = sorted(roster - have)

        if not missing:
            return 0

        now = datetime.now(timezone.utc).isoformat()
        client.table('source_weights').insert([
            {
                'source': source,
                'weight': 1.0,
                'gpvs_contribution': None,
                'last_updated': now,
            }
            for source in missing
        ]).execute()
        print(f"  ✅ Seeded {len(missing)} roster weights at neutral (1.0)")
        return len(missing)

    except Exception as e:
        print(f"  ⚠️  Roster weight seed failed: {e}")
        return 0


def update_source_weight(source: str, gpvs_score: float) -> None:
    """
    Update a source's weight based on its GPVS contribution.
    Called after outcome verification to reward accurate sources.
    Weight formula: new_weight = 0.7 * old_weight + 0.3 * gpvs_factor
    gpvs_factor: 1.5 for perfect (1.0), 1.0 for partial (0.5), 0.7 for wrong (0.0)
    """
    client = get_client()
    if not client:
        return

    try:
        source_key = norm(source)

        # Map gpvs_score to weight factor
        if gpvs_score >= 1.0:
            gpvs_factor = 1.5
        elif gpvs_score >= 0.5:
            gpvs_factor = 1.0
        else:
            gpvs_factor = 0.7

        # Get current weight
        result = client.table('source_weights') \
            .select('weight') \
            .eq('source', source_key) \
            .execute()

        current = DEFAULT_WEIGHTS.get(source_key, 1.0)
        if result.data:
            current = result.data[0]['weight']

        # Exponential moving average update
        new_weight = round(0.7 * current + 0.3 * gpvs_factor, 4)
        new_weight = max(0.5, min(new_weight, 2.0))  # Clamp 0.5–2.0

        client.table('source_weights').upsert({
            'source': source_key,
            'weight': new_weight,
            'gpvs_contribution': gpvs_score,
            'last_updated': datetime.now(timezone.utc).isoformat(),
        }).execute()

        # Invalidate cache
        global _weight_cache
        _weight_cache = None

        print(f"  📊 Weight updated: {source} {current:.3f} → {new_weight:.3f} (GPVS: {gpvs_score})")

    except Exception as e:
        print(f"  ⚠️  Weight update failed for {source}: {e}")


def get_weights_summary() -> list:
    """Return all source weights for dashboard display."""
    client = get_client()
    if not client:
        return []

    try:
        result = client.table('source_weights') \
            .select('*') \
            .order('weight', desc=True) \
            .execute()
        return result.data or []
    except Exception as e:
        print(f"  ⚠️  Weights summary failed: {e}")
        return []


if __name__ == "__main__":
    # READ-ONLY display (I-5). This block used to call update_source_weight()
    # on BBC and Fox News, mutating live production weights on every standalone
    # run — do not reintroduce writes here.
    print("📊 GNI Source Weights\n")
    weights = get_source_weights(force_refresh=True)
    print(f"\nCurrent weights:")
    for source, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(weight * 5)
        print(f"  {source:20s}: {weight:.3f}  {bar}")
