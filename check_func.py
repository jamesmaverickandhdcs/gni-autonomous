content = open('ai_engine/funnel/intelligence_funnel.py', encoding='utf-8').read()
old = '_check_injection(article: dict) -> tuple[bool, str]:\n    """Stage 1b: Check for prompt injection attacks."""\n    text = f"{article.g'
print('found:', old[:50] in content)
