import os
import re

pages = [
    'brief','debate','comparison','scenarios','stocks','map','pillars','alerts',
    'history','research','correlations','weekly-digest','methodology',
    'developer','transparency','autonomy','health','security','source-health',
    'adaptive-log','quota','mission-control',
    'predictions','validation-log','model-learning','pattern-library'
]

valid_pages = ['/','/researcher','/developer-hub','/reports','/about',
               '/brief','/debate','/comparison','/scenarios','/stocks',
               '/map','/pillars','/alerts','/history','/research',
               '/correlations','/weekly-digest','/methodology',
               '/developer','/transparency','/autonomy','/health',
               '/security','/source-health','/adaptive-log','/quota',
               '/mission-control','/predictions','/validation-log',
               '/model-learning','/pattern-library']

print('=== ADDITIONAL WEAKNESS SCAN ===')
print()

for page in pages:
    path = f'src/app/{page}/page.tsx'
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []

    # Check 1: Broken internal links
    internal_links = re.findall(r'href=\"(/[^\"#]*)\"', content)
    for link in internal_links:
        if link.startswith('/api'): continue
        base = link.split('?')[0]
        if base not in valid_pages:
            issues.append(f'BROKEN LINK: href={link}')

    # Check 2: Empty href
    if 'href=\"#\"' in content:
        issues.append('EMPTY LINK: href=# found')

    # Check 3: localhost
    if 'localhost' in content:
        issues.append('DEV: localhost reference')

    # Check 4: Stale branding
    if 'GNI_Autonomous Sprint' in content:
        issues.append('STALE: GNI_Autonomous Sprint reference')

    # Check 5: Stale year 2025
    count_2025 = len(re.findall(r'2025', content))
    if count_2025 > 0:
        issues.append(f'STALE YEAR: 2025 found {count_2025} times')

    # Check 6: External links without target blank
    ext_links = re.findall(r'href=\"(https?://[^\"]+)\"', content)
    for link in ext_links:
        link_idx = content.find(link)
        surrounding = content[link_idx:link_idx+200]
        if 'target' not in surrounding:
            issues.append(f'UX: External link missing target=_blank: {link[:50]}')

    # Check 7: Hardcoded GNI_Autonomous Sprint days
    if 'Sprint days' in content:
        issues.append('STALE: Sprint days counter (static number)')

    if issues:
        print(f'*** [{page}]')
        for issue in issues:
            print(f'  ! {issue}')
    else:
        print(f'[{page}] clean')

print()
print('=== HUB PAGES ===')
for (fname, name) in [('page','dashboard'),('researcher/page','researcher'),('developer-hub/page','developer-hub'),('reports/page','reports'),('about/page','about')]:
    path = f'src/app/{fname}.tsx'
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    issues = []
    count_2025 = len(re.findall(r'2025', content))
    if count_2025 > 0:
        issues.append(f'STALE YEAR: 2025 found {count_2025} times')
    if 'GNI_Autonomous Sprint' in content:
        issues.append('STALE: GNI_Autonomous Sprint reference')
    if 'Sprint days' in content:
        issues.append('STALE: Sprint days counter')
    ext_links = re.findall(r'href=\"(https?://[^\"]+)\"', content)
    for link in ext_links:
        link_idx = content.find(link)
        surrounding = content[link_idx:link_idx+200]
        if 'target' not in surrounding:
            issues.append(f'UX: External link missing target=_blank: {link[:50]}')
    if issues:
        print(f'*** [{name}]')
        for issue in issues: print(f'  ! {issue}')
    else:
        print(f'[{name}] clean')

print()
print('Scan complete.')