import re

content = open('ai_engine/funnel/intelligence_funnel.py', encoding='utf-8').read()

# Find and remove the inline INJECTION_PATTERNS block
# Find start of INJECTION_PATTERNS
start_marker = 'INJECTION_PATTERNS = ['
end_marker = '_check_injection'

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

print(f'INJECTION_PATTERNS starts at: {idx_start}')
print(f'_check_injection starts at: {idx_end}')
print(f'Block to replace: {repr(content[idx_start:idx_start+100])}')

# Replace the inline INJECTION_PATTERNS list with an import
# and replace _check_injection function with one that uses the detector

old_patterns_block = content[idx_start:idx_end]
print(f'Block length: {len(old_patterns_block)} chars')

new_import_line = '# Injection patterns moved to prompt_injection_detector.py (Day 11 — 70 patterns)\nfrom prompt_injection_detector import detect_injection\n\n\n'

# Replace the inline patterns block
content = content[:idx_start] + new_import_line + content[idx_end:]

# Now find and replace the _check_injection function body
old_func = '''def _check_injection(article: dict) -> tuple[bool, str]:
    """Stage 1b: Check for prompt injection attacks."""
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False, f"Injection pattern detected: {pattern[:40]}"
    return True, "Clean \xe2\x80\x94 no injection patterns"'''

new_func = '''def _check_injection(article: dict) -> tuple[bool, str]:
    """Stage 1b: Check for prompt injection attacks — uses 70-pattern detector."""
    article = detect_injection(article)
    scan = article.get("injection_scan", {})
    if not scan.get("is_clean", True):
        matched = scan.get("matched_patterns", [])
        pattern_str = matched[0][:40] if matched else "soft signal"
        return False, f"Injection detected [{scan.get('threat_level','HIGH')}]: {pattern_str}"
    return True, f"Clean \u2014 no injection patterns (70 patterns checked)"'''

if old_func in content:
    content = content.replace(old_func, new_func)
    print('_check_injection replaced successfully')
else:
    print('WARNING: _check_injection not found with exact match — trying partial')
    # Find it by searching for the def line
    idx_func = content.find('def _check_injection(article: dict)')
    if idx_func >= 0:
        idx_func_end = content.find('\ndef ', idx_func + 10)
        print(f'Function found at {idx_func}, ends at {idx_func_end}')
        print(repr(content[idx_func:idx_func+200]))

with open('ai_engine/funnel/intelligence_funnel.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print('Done')

# Verify
c2 = open('ai_engine/funnel/intelligence_funnel.py', encoding='utf-8').read()
print('Import present:', 'from prompt_injection_detector import' in c2)
print('Old patterns gone:', 'INJECTION_PATTERNS = [' not in c2)
print('New function present:', '70 patterns checked' in c2 or 'detect_injection' in c2)
