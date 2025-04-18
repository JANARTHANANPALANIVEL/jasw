import uuid
import re

def parse_test_output(raw_output, start_time, end_time, url):
    lines = raw_output.strip().split("\n")
    steps = []
    passed = 0
    failed = 0
    errors = 0

    for line in lines:
        status = "info"
        if "PASS" in line:
            status = "pass"
            passed += 1
        elif "FAIL" in line:
            status = "fail"
            failed += 1
        elif "ERROR" in line:
            status = "error"
            errors += 1

        steps.append({
            "description": line.strip(),
            "status": status
        })

    total = passed + failed + errors
    score = round((passed / total) * 100, 2) if total > 0 else 0
    status = "Passed" if failed == 0 and errors == 0 else "Failed"
    runtime = end_time - start_time
    summary = f"Total: {total}, Passed: {passed}, Failed: {failed}, Errors: {errors}"

    return {
        "filename": str(uuid.uuid4()),
        "url": url,
        "status": status,
        "score": score,
        "runtime": runtime,
        "summary": summary,
        "steps": steps
    }
