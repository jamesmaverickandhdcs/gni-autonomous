import os
import re

pages = [
    'debate','comparison','scenarios','map','pillars','alerts',
    'history','research','correlations','weekly-digest',
    'transparency','autonomy','health','security','source-health',
    'adaptive-log','quota','predictions','validation-log',
    'model-learning','pattern-library','researcher','developer-hub','reports'
]

print('=== ERROR STATE AUDIT ===')
print()

for page in pages:
    path = f'src/app/{page}/page.tsx'
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    has_error_state = (
        '{error &&' in content or
        'error &&' in content or
        'setError' in content or
        '{error}' in content or
        'isError' in content
    )
    has_loading_state = (
        '{loading &&' in content or
        'loading &&' in content or
        'setLoading' in content or
        'isLoading' in content
    )
    is_static = 'useState' not in content
    has_fetch = 'fetch(' in content

    status = []
    if is_static:
        status.append('STATIC -- no async data')
    else:
        if not has_loading_state:
            status.append('MISSING loading state')
        if not has_error_state:
            status.append('MISSING error state')
        if not has_fetch:
            status.append('no fetch calls')

    tag = 'STATIC' if is_static else ('OK' if has_error_state and has_loading_state else 'NEEDS FIX')
    print(f'{tag:<10} [{page}] {\" | \".join(status)}')

print()
print('Scan complete.')