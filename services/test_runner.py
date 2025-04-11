import os
import subprocess
import uuid

def run_generated_testcase(code):
    filename = f"generated_test_{uuid.uuid4().hex}.py"
    filepath = os.path.join("results", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    try:
        result = subprocess.run(
            ["python", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
            check=False,
            text=True
        )
        output = result.stdout
    except subprocess.TimeoutExpired:
        output = "ERROR: Test execution timed out."

    return output, filename
