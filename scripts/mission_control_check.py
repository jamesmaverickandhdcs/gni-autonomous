import sys, json

try:
    with open('/tmp/mc_response.json') as f:
        data = json.load(f)
    status = data.get('overall_status', 'UNKNOWN')
    issues = data.get('issues_found', 0)
    print(f'Mission Control Status: {status}')
    print(f'Issues Found: {issues}')
    if status == 'CRITICAL':
        print('CRITICAL issues detected -- check Telegram for details')
        sys.exit(1)
    elif status == 'WARNING':
        print('WARNING issues detected -- monitor closely')
    else:
        print('All systems healthy')
except Exception as e:
    print(f'Mission Control check failed: {e}')
    sys.exit(1)