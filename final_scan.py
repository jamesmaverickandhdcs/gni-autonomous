import os, re

pages = [
    'brief','debate','comparison','scenarios','stocks','map','pillars','alerts',
    'history','research','correlations','weekly-digest','methodology',
    'developer','transparency','autonomy','health','security','source-health',
    'adaptive-log','quota','mission-control',
    'predictions','validation-log','model-learning','pattern-library'
]

hub_pages = [('page','dashboard'),('researcher/page','researcher'),
             ('developer-hub/page','developer-hub'),('reports/page','reports'),('about/page','about')]

print('=== FINAL COMPREHENSIVE SCAN ===')
print()

all_issues = []

for page in pages:
    path = f'src/app/{page}/page.tsx'
    if not os.path.exists(path): continue
    content = open(path,'r',encoding='utf-8').read()
    issues = []

    # 1. Back button
    has_back = any(x in content for x in ['Quantum Strategist','Pattern Intelligence','Dev Console','Feedback Loop'])
    if not has_back:
        issues.append('MISSING back button')

    # 2. Disclaimer
    if 'financial advice' not in content and 'informational purposes' not in content:
        issues.append('MISSING disclaimer')

    # 3. Higher Diploma
    if 'Higher Diploma' not in content:
        issues.append('MISSING Higher Diploma in footer')

    # 4. SUM
    if 'Spring University Myanmar' not in content and 'SUM' not in content:
        issues.append('MISSING SUM in footer')

    # 5. Description after h1
    desc = re.search(r'<h1[^>]*>.*?</h1>\s*<p', content, re.DOTALL)
    if not desc:
        issues.append('MISSING page description')

    # 6. Cross-nav check
    total = (content.count('href="/"') + content.count('href="/researcher"') +
             content.count('href="/developer-hub"') + content.count('href="/reports"') +
             content.count('href="/about"'))
    if total > 1:
        issues.append('CROSS-NAV present: ' + str(total) + ' hub links')

    # 7. GNI_KEY in fetch
    if 'fetch(' in content and 'GNI_KEY' not in content:
        issues.append('MISSING GNI_KEY in fetch')

    # 8. Error state
    has_error = 'setError' in content or '{error &&' in content
    has_fetch = 'fetch(' in content
    if has_fetch and not has_error:
        issues.append('MISSING error state')

    if issues:
        all_issues.append((page, issues))
        print('*** [' + page + ']')
        for i in issues: print('  ! ' + i)
    else:
        print('OK  [' + page + ']')

print()
print('=== HUB PAGES ===')
for fname, name in hub_pages:
    path = f'src/app/{fname}.tsx'
    if not os.path.exists(path): continue
    content = open(path,'r',encoding='utf-8').read()
    issues = []
    if 'financial advice' not in content and 'informational purposes' not in content:
        issues.append('MISSING disclaimer')
    if 'Higher Diploma' not in content:
        issues.append('MISSING Higher Diploma')
    if 'SUM' not in content and 'Spring University' not in content:
        issues.append('MISSING SUM')
    if issues:
        print('*** [' + name + ']')
        for i in issues: print('  ! ' + i)
    else:
        print('OK  [' + name + ']')

print()
if all_issues:
    print('TOTAL ISSUES: ' + str(len(all_issues)) + ' pages need attention')
else:
    print('ALL PAGES CLEAN!')