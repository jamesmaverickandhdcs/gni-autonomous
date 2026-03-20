content = open('ai_engine/funnel/intelligence_funnel.py', encoding='utf-8').read()

# Find the exact INJECTION_PATTERNS block
start = content.find('INJECTION_PATTERNS = [')
end = content.find(']', content.find('__import__')) + 1  # find closing ] after last pattern

# Verify
print(f'Start: {start}')
print(f'End: {end}')
print(f'Current block: {repr(content[start:start+80])}')
print(f'Block ends: {repr(content[end-20:end+20])}')
