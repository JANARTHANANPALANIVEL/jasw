from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import time
import json

from services.test_generator import generate_testcase
from services.test_runner import run_generated_testcase
from services.result_parser import parse_test_output
from utils.url_validator import validate_url
from services.report_generator import generate_pdf_report

app = Flask(__name__)
app.secret_key = "jasw-secret"

os.makedirs("results", exist_ok=True)

# Store session-wise data temporarily
session_data = {}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", testcase_code="", show_result=False)

@app.route("/generate-testcase", methods=["POST"])
def generate_testcase_route():
    url = request.form.get("url")

    # Validate URL format and accessibility
    is_valid, msg = validate_url(url)
    if not is_valid:
        return render_template("index.html", error=msg, show_result=False)

    # Generate test case code using AI
    testcase_code = generate_testcase(url).strip("`python").strip("`").strip()
    session_data["url"] = url
    session_data["testcase_code"] = testcase_code

    return render_template("index.html", testcase_code=testcase_code, show_result=True)

@app.route("/start-test", methods=["POST"])
def start_test():
    code = request.form.get("testcase_code")
    url = session_data.get("url", "Unknown URL")
    start_time = time.time()

    # Run the generated test case
    raw_output, script_filename = run_generated_testcase(code)
    end_time = time.time()

    # Parse the result from the raw output of the test case
    parsed_result = parse_test_output(raw_output, start_time, end_time, url)
    result_filename = f"{parsed_result['filename']}.json"
    json_path = os.path.join("results", result_filename)

    # Save the parsed result in JSON format
    with open(json_path, "w") as f:
        json.dump(parsed_result, f, indent=2)

    # Generate a PDF report from the parsed result
    pdf_path = os.path.join("results", f"{parsed_result['filename']}.pdf")
    generate_pdf_report(parsed_result, pdf_path)

    session_data["latest_result"] = parsed_result

    # Return dashboard URL to redirect via JS
    return jsonify({"redirect_url": url_for("dashboard", result_file=result_filename)})

@app.route("/dashboard")
def dashboard():
    result_file = request.args.get("result_file")
    filepath = os.path.join("results", result_file)

    if not os.path.exists(filepath):
        return "Result not found", 404

    with open(filepath, "r") as f:
        result = json.load(f)

    # Calculate pass, fail, and error counts
    passed = sum(1 for step in result['steps'] if step['status'] == 'pass')
    failed = sum(1 for step in result['steps'] if step['status'] == 'fail')
    errors = sum(1 for step in result['steps'] if step['status'] == 'error')

    # Add the pass, fail, and error counts to the result object
    return render_template("dashboard.html", result=result, passed=passed, failed=failed, errors=errors)

@app.route("/download-report/<filename>")
def download_report(filename):
    path = os.path.join("results", filename)

    if not os.path.exists(path):
        return "File not found", 404

    return open(path, "rb").read(), 200, {
        "Content-Type": "application/pdf",
        "Content-Disposition": f"attachment; filename={filename}"
    }

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)  # Disable auto-reload to avoid duplicate execution
