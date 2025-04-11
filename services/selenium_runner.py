import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile

def run_test_case(code, url):
    result = {
        'url': url,
        'status': [],
        'start_time': time.time()
    }

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as f:
            f.write(code)
            filepath = f.name

        exec(open(filepath).read(), globals())

        result['status'].append({'step': 'Execution Complete', 'result': 'Pass'})
    except Exception as e:
        result['status'].append({'step': 'Execution Error', 'result': 'Fail', 'error': str(e), 'trace': traceback.format_exc()})
    finally:
        result['end_time'] = time.time()
        result['runtime'] = round(result['end_time'] - result['start_time'], 2)
        result['pass_count'] = len([s for s in result['status'] if s['result'] == 'Pass'])
        result['fail_count'] = len([s for s in result['status'] if s['result'] == 'Fail'])
        total = result['pass_count'] + result['fail_count']
        result['score'] = round((result['pass_count'] / total) * 100, 2) if total > 0 else 0

    return result
