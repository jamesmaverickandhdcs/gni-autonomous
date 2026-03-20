# ============================================================
# GNI Deception Detector — Day 15 v2
# Detects coordinated narratives across sources
# Uses centroid clustering: finds shared keyword core
# across all articles in a potential group
# ============================================================

import re
from collections import defaultdict, Counter


STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'has', 'have', 'had', 'will', 'would', 'could', 'should', 'may', 'might',
    'this', 'that', 'these', 'those', 'it', 'its', 'as', 'he', 'she', 'they',
    'we', 'you', 'i', 'his', 'her', 'their', 'our', 'your', 'my', 'news',
    'report', 'says', 'said', 'told', 'according', 'amid', 'after', 'over',
    'new', 'also', 'up', 'out', 'about', 'into', 'than', 'more', 'two',
}

MIN_WORD_LENGTH = 4
MIN_SOURCES_FOR_COORDINATION = 3
# A keyword must appear in this fraction of articles to be "shared"
SHARED_KEYWORD_THRESHOLD = 0.6  # 60% of articles must share the keyword


def _extract_keywords(text: str) -> set:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = text.split()
    return {w for w in words if len(w) >= MIN_WORD_LENGTH and w not in STOP_WORDS}


def _find_shared_core(keyword_sets: list[set], threshold: float) -> set:
    """Find keywords that appear in at least threshold fraction of articles."""
    if not keyword_sets:
        return set()
    n = len(keyword_sets)
    all_words = Counter()
    for kw_set in keyword_sets:
        for word in kw_set:
            all_words[word] += 1
    return {word for word, count in all_words.items() if count / n >= threshold}


def detect_coordination(articles: list[dict]) -> dict:
    """
    Detect coordinated narratives across sources using centroid clustering.
    Groups articles by topic first, then checks if 3+ different sources
    share a strong keyword core within each topic group.
    """
    if len(articles) < MIN_SOURCES_FOR_COORDINATION:
        return {
            'coordination_score': 0.0,
            'coordination_level': 'NONE',
            'flagged_clusters': [],
            'unique_narratives': len(articles),
            'dominant_narrative': '',
            'coordinated_article_count': 0,
            'total_articles_checked': len(articles),
        }

    # Extract keywords per article
    enriched = []
    for art in articles:
        text = f"{art.get('title', '')} {art.get('summary', '')}"
        enriched.append({
            'source': art.get('source', 'Unknown'),
            'bias': art.get('bias', ''),
            'title': art.get('title', '')[:80],
            'keywords': _extract_keywords(text),
        })

    # Step 1: Find the shared keyword core across ALL articles
    all_kw_sets = [e['keywords'] for e in enriched]
    global_core = _find_shared_core(all_kw_sets, SHARED_KEYWORD_THRESHOLD)

    clusters = []
    coordinated_indices = set()

    if len(global_core) >= 3:
        # There is a shared topic — check if 3+ sources are coordinating on it
        sources_on_topic = []
        for i, art in enumerate(enriched):
            # Article is "on topic" if it contains most of the core keywords
            overlap = len(art['keywords'] & global_core) / len(global_core) if global_core else 0
            if overlap >= 0.5:
                sources_on_topic.append(i)

        unique_sources = {enriched[i]['source'] for i in sources_on_topic}

        if len(unique_sources) >= MIN_SOURCES_FOR_COORDINATION:
            for idx in sources_on_topic:
                coordinated_indices.add(idx)

            clusters.append({
                'articles': [enriched[i] for i in sources_on_topic],
                'sources': list(unique_sources),
                'source_count': len(unique_sources),
                'common_keywords': sorted(global_core)[:10],
                'topic_coverage': round(len(sources_on_topic) / len(articles), 2),
            })

    # Step 2: Also check pairwise for any remaining strong overlaps
    checked = set()
    for i in range(len(enriched)):
        if i in coordinated_indices:
            continue
        cluster = [i]
        for j in range(i + 1, len(enriched)):
            if j in coordinated_indices:
                continue
            kw_i = enriched[i]['keywords']
            kw_j = enriched[j]['keywords']
            if not kw_i or not kw_j:
                continue
            overlap = len(kw_i & kw_j) / len(kw_i | kw_j)
            if overlap >= 0.55:
                cluster.append(j)

        if len(cluster) >= MIN_SOURCES_FOR_COORDINATION:
            sources = {enriched[k]['source'] for k in cluster}
            if len(sources) >= MIN_SOURCES_FOR_COORDINATION:
                for idx in cluster:
                    coordinated_indices.add(idx)
                shared = _find_shared_core([enriched[k]['keywords'] for k in cluster], 0.5)
                clusters.append({
                    'articles': [enriched[k] for k in cluster],
                    'sources': list(sources),
                    'source_count': len(sources),
                    'common_keywords': sorted(shared)[:10],
                    'topic_coverage': round(len(cluster) / len(articles), 2),
                })

    # Calculate score
    total = len(articles)
    coordinated = len(coordinated_indices)
    coordination_score = round(coordinated / total, 3) if total > 0 else 0.0

    if coordination_score >= 0.7:
        level = 'COORDINATED'
    elif coordination_score >= 0.5:
        level = 'HIGH'
    elif coordination_score >= 0.3:
        level = 'MEDIUM'
    elif coordination_score > 0.0:
        level = 'LOW'
    else:
        level = 'NONE'

    dominant_narrative = ''
    if clusters:
        largest = max(clusters, key=lambda c: c['source_count'])
        dominant_narrative = ' '.join(largest['common_keywords'][:5])

    unique_narratives = total - coordinated + len(clusters)

    return {
        'coordination_score': coordination_score,
        'coordination_level': level,
        'flagged_clusters': clusters,
        'unique_narratives': unique_narratives,
        'dominant_narrative': dominant_narrative,
        'coordinated_article_count': coordinated,
        'total_articles_checked': total,
    }


def enrich_report_with_deception(report: dict, articles: list[dict]) -> dict:
    """Add deception detection results to report."""
    result = detect_coordination(articles)

    report['deception_score'] = result['coordination_score']
    report['deception_level'] = result['coordination_level']

    if result['coordination_level'] in ('HIGH', 'COORDINATED', 'MEDIUM'):
        print(f"   ⚠️  Coordination [{result['coordination_level']}]: "
              f"{result['coordinated_article_count']}/{result['total_articles_checked']} articles — "
              f"dominant: {result['dominant_narrative'][:50]}")
        # Discount consensus if coordination detected
        original = report.get('source_consensus_score', 0.5)
        report['source_consensus_score'] = round(original * 0.75, 3)
        report['deception_note'] = f"{result['coordination_level']} coordination — consensus discounted"
    else:
        print(f"   ✅ Narrative diversity: {result['coordination_level']} "
              f"({result['unique_narratives']} unique angles)")

    return report


if __name__ == '__main__':
    print("\U0001f575  GNI Deception Detector — Test Run\n")

    test_articles = [
        {'source': 'CNN', 'bias': 'Western Liberal',
         'title': 'Iran threatens to close Strait of Hormuz amid US sanctions',
         'summary': 'Iran military forces moved toward Hormuz strait as tensions escalate with United States'},
        {'source': 'BBC', 'bias': 'Western Liberal',
         'title': 'Iran threatens closure of Hormuz strait after US sanctions',
         'summary': 'Iranian forces positioned near Hormuz strait following United States sanctions'},
        {'source': 'France 24', 'bias': 'Western Liberal',
         'title': 'Iran threatens Hormuz closure as United States sanctions bite',
         'summary': 'Iran military near Hormuz strait threatens closure amid US sanctions escalation'},
        {'source': 'Al Jazeera', 'bias': 'Non-Western',
         'title': 'Gulf states urge diplomacy as Hormuz tensions rise',
         'summary': 'Saudi Arabia and UAE call for negotiated solution to Iran sanctions dispute'},
        {'source': 'Nikkei Asia', 'bias': 'Asian Perspective',
         'title': 'Asian markets brace for oil price shock from Hormuz crisis',
         'summary': 'Japanese and Korean manufacturers warn of energy cost increases if Hormuz closes'},
    ]

    result = detect_coordination(test_articles)
    print(f"  Coordination Score: {result['coordination_score']:.2f}")
    print(f"  Level: {result['coordination_level']}")
    print(f"  Coordinated: {result['coordinated_article_count']}/{result['total_articles_checked']}")
    print(f"  Unique Narratives: {result['unique_narratives']}")
    print(f"  Dominant: {result['dominant_narrative']}")
    if result['flagged_clusters']:
        for c in result['flagged_clusters']:
            print(f"  Cluster sources: {c['sources']}")
            print(f"  Common keywords: {c['common_keywords'][:6]}")
