"""
GNI MAD Protocol -- Pillar-specific Arbitrator weighting
TECH pillar dominant -> weight Black Swan agent (unknown tech threats)
FIN pillar dominant -> weight Bear agent (downside risks)
GEO pillar dominant -> balanced (current behavior)
GNI-R-037: Full file read done
GNI-R-062: py_compile check at end
Run from: C:\HDCS_Project\03\GNI_Autonomous
Usage: python add_mad_pillar_weights.py
"""

import os
import py_compile

file_path = os.path.join("ai_engine", "analysis", "mad_protocol.py")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# Fix 1: Add pillar detection helper after _build_news_context
old1 = "def _get_debate_history() -> dict:"
new1 = """def _detect_dominant_pillar(all_articles: list) -> str:
    \"\"\"Detect which pillar dominates this run's article set.\"\"\"
    counts = {'geo': 0, 'tech': 0, 'fin': 0}
    for art in all_articles:
        p = art.get('pillar', '').lower()
        if p in counts:
            counts[p] += 1
    if not any(counts.values()):
        return 'geo'
    return max(counts, key=counts.get)


def _get_pillar_arb_instruction(pillar: str) -> str:
    \"\"\"Return pillar-specific weighting instruction for Arbitrator.\"\"\"
    if pillar == 'tech':
        return (
            'PILLAR WEIGHTING -- TECHNOLOGY DOMINANT: '
            'Give extra weight to the Black Swan agent position. '
            'Technology threats are often unknown unknowns -- '
            'zero-day exploits, AI capability jumps, chip supply shocks. '
            'The Bear agent downside is important but Black Swan is highest value here. '
        )
    elif pillar == 'fin':
        return (
            'PILLAR WEIGHTING -- FINANCIAL DOMINANT: '
            'Give extra weight to the Bear agent position. '
            'Financial threats are typically known risks playing out -- '
            'rate shocks, sovereign defaults, currency crises, contagion. '
            'The Bear agent systematic risk analysis is highest value here. '
        )
    else:
        return (
            'PILLAR WEIGHTING -- GEOPOLITICAL DOMINANT: '
            'Balanced weighting across all 4 agents. '
            'Geopolitical threats span all quadrants equally -- '
            'known conflicts (Bear), missed opportunities (Bull), '
            'ignored realities (Ostrich), and unknown escalations (Black Swan). '
        )


def _get_debate_history() -> dict:"""

if old1 in content:
    content = content.replace(old1, new1)
    fixes += 1
    print("OK Fix 1: Added _detect_dominant_pillar() and _get_pillar_arb_instruction()")

# Fix 2: Use pillar detection in run_mad_protocol
old2 = "    news_ctx = _build_news_context(report, all_articles)\n    history = _get_debate_history()"
new2 = """    news_ctx = _build_news_context(report, all_articles)
    dominant_pillar = _detect_dominant_pillar(all_articles)
    pillar_instruction = _get_pillar_arb_instruction(dominant_pillar)
    print(f'   Dominant pillar: {dominant_pillar.upper()} -- {pillar_instruction[:60]}...')
    history = _get_debate_history()"""

if old2 in content:
    content = content.replace(old2, new2)
    fixes += 1
    print("OK Fix 2: Added pillar detection call in run_mad_protocol()")

# Fix 3: Inject pillar instruction into Arbitrator final synthesis prompt
old3 = "        'Deliver final synthesis as JSON only.'\n    )"
new3 = """        + 'PILLAR WEIGHTING: ' + pillar_instruction + '\\n\\n'
        + 'Deliver final synthesis as JSON only.'
    )"""

if old3 in content:
    content = content.replace(old3, new3)
    fixes += 1
    print("OK Fix 3: Pillar instruction injected into Arbitrator final synthesis")

if fixes == 0:
    print("ERROR: No target blocks found -- file may have changed.")
    exit(1)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print(f"OK Updated: {file_path} ({fixes} fixes applied)")

# GNI-R-062
py_compile.compile(file_path, doraise=True)
print("OK py_compile: syntax OK")
print("DONE. Now run: npm run build")
