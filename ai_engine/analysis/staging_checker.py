# ============================================================
# GNI Staging Checker
# Lightweight HTTP regression check for staging deployment
# Runs after pipeline — catches broken pages before production
# ============================================================

import os
import requests
from dotenv import load_dotenv
load_dotenv()

STAGING_URL = os.getenv(
    'STAGING_URL',
    'https://gni-autonomous-git-staging-jamesmaverickandhdcs-projects.vercel.app'
)
VERCEL_BYPASS_SECRET = os.getenv('VERCEL_BYPASS_SECRET', '')

# Pages to check with their required content signatures
PAGES = [
    ('/',               'Global Nexus Insights', 'Homepage'),
    ('/history',        'Intelligence',          'History page'),
    ('/health',         'Health',                'Health page'),
    ('/debate',         'Debate',                'Debate page'),
    ('/autonomy',       'Autonomous',            'Autonomy page'),
    ('/transparency',   'Transparency',          'Transparency page'),
    ('/security',       'Security',              'Security page'),
    ('/api/reports',    'created_at',            'Reports API'),
    ('/api/health',     'status',                'Health API'),
]
# Note: /keywords, /source-health, /correlations exist on main branch only.
# Staging branch does not receive these pages -- verified by npm run build instead.


def check_page(path, signature, label):
    """
    Check a single page. Returns (passed, message).
    """
    url = STAGING_URL.rstrip('/') + path
    try:
        headers = {}
        if VERCEL_BYPASS_SECRET:
            headers['x-vercel-protection-bypass'] = VERCEL_BYPASS_SECRET
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return False, f'HTTP {response.status_code}'
        if signature.lower() not in response.text.lower():
            return False, f'Content signature not found: {signature!r}'
        return True, f'OK ({response.status_code}, {len(response.text)} chars)'
    except requests.Timeout:
        return False, 'Timeout after 15s'
    except Exception as e:
        return False, f'Error: {e}'


def run_staging_checks():
    """
    Run all staging page checks.
    Returns dict with passed, failed, results.
    """
    print(f'  📸 Staging regression check: {STAGING_URL}')
    results = []
    passed = 0
    failed = 0

    for path, signature, label in PAGES:
        ok, msg = check_page(path, signature, label)
        results.append({
            'path': path,
            'label': label,
            'passed': ok,
            'message': msg,
        })
        if ok:
            passed += 1
            print(f'    ✅ {label}: {msg}')
        else:
            failed += 1
            print(f'    ❌ {label}: {msg}')

    status = 'passed' if failed == 0 else 'failed'
    print(f'  📊 Staging: {passed}/{len(PAGES)} checks passed')

    return {
        'status': status,
        'passed': passed,
        'failed': failed,
        'total': len(PAGES),
        'results': results,
        'staging_url': STAGING_URL,
    }


if __name__ == '__main__':
    print('\n📸 GNI Staging Checker — Manual Run\n')
    result = run_staging_checks()
    print(f'\n  Status: {result["status"].upper()}')
    print(f'  Passed: {result["passed"]}/{result["total"]}')
    if result['failed'] > 0:
        print('  Failed pages:')
        for r in result['results']:
            if not r['passed']:
                print(f'    - {r["label"]} ({r["path"]}): {r["message"]}')
