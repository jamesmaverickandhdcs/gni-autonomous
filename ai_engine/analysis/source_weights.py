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

# Default weights — fallback if Supabase unavailable
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
            # First run — seed defaults into Supabase
            print("  📥 Source weights: seeding defaults into Supabase...")
            _seed_defaults(client)
            _weight_cache = DEFAULT_WEIGHTS.copy()
        else:
            _weight_cache = {r['source'].lower(): r['weight'] for r in rows}
            print(f"  ✅ Source weights loaded: {len(_weight_cache)} sources")

        _cache_loaded_at = datetime.now(timezone.utc).isoformat()
        return _weight_cache

    except Exception as e:
        print(f"  ⚠️  Source weights fetch failed: {e} — using defaults")
        return DEFAULT_WEIGHTS.copy()


def _seed_defaults(client) -> None:
    """Seed default weights into Supabase source_weights table."""
    try:
        records = [
            {
                'source': source,
                'weight': weight,
                'gpvs_contribution': None,
                'last_updated': datetime.now(timezone.utc).isoformat(),
            }
            for source, weight in DEFAULT_WEIGHTS.items()
        ]
        client.table('source_weights').upsert(records).execute()
        print(f"  ✅ Seeded {len(records)} default weights")
    except Exception as e:
        print(f"  ⚠️  Seed failed: {e}")


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
        source_lower = source.lower()

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
            .eq('source', source_lower) \
            .execute()

        current = DEFAULT_WEIGHTS.get(source_lower, 1.0)
        if result.data:
            current = result.data[0]['weight']

        # Exponential moving average update
        new_weight = round(0.7 * current + 0.3 * gpvs_factor, 4)
        new_weight = max(0.5, min(new_weight, 2.0))  # Clamp 0.5–2.0

        client.table('source_weights').upsert({
            'source': source_lower,
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
    print("📊 GNI Source Weights\n")
    weights = get_source_weights(force_refresh=True)
    print(f"\nCurrent weights:")
    for source, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(weight * 5)
        print(f"  {source:20s}: {weight:.3f}  {bar}")

    print(f"\nTesting weight update...")
    update_source_weight("BBC", 1.0)
    update_source_weight("Fox News", 0.0)

    print(f"\nUpdated weights:")
    weights = get_source_weights(force_refresh=True)
    for source, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(weight * 5)
        print(f"  {source:20s}: {weight:.3f}  {bar}")
