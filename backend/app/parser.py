import re
from typing import List, Dict, Any

# Very simple parser for lines like:
# TEST tb_name ... PASS duration=12ms
# TEST tb_name ... FAIL duration=4ms
# If duration is absent, default 0.
line_re = re.compile(r"^\s*TEST\s+(?P<name>\S+)\s+.*?(?P<status>PASS|FAIL)(?:\s+duration=(?P<dur>\d+)ms)?", re.IGNORECASE)

def parse_log(text: str) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    passed = failed = 0
    for line in text.splitlines():
        m = line_re.match(line)
        if not m:
            continue
        name = m.group('name')
        status = m.group('status').upper()
        dur = int(m.group('dur') or 0)
        results.append({'name': name, 'status': status, 'duration_ms': dur, 'message': ''})
        if status == 'PASS':
            passed += 1
        else:
            failed += 1
    return {
        'tests': results,
        'passed': passed,
        'failed': failed,
        'total': passed + failed
    }
