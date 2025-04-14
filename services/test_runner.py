import os
import subprocess
import uuid

def run_generated_testcase(code):
    # Generate a unique filename for the generated test script
    filename = f"generated_test_{uuid.uuid4().hex}.py"
    filepath = os.path.join("results", filename)

    # Write the generated test case code to a Python file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    try:
        # Run the generated test case script using subprocess
        result = subprocess.run(
            ["python", filepath],
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.STDOUT,  # Capture error output as well
            timeout=120,  # Timeout after 2 minutes
            check=False,  # Do not raise an exception on error
            text=True  # Capture output as string, not bytes
        )
        output = result.stdout  # Get the output of the script
    except subprocess.TimeoutExpired:
        # Handle test timeout scenario
        output = "ERROR: Test execution timed out."

    return output, filename
