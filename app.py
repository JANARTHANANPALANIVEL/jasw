from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from services.gemini_testcase_generator import generate_test_case
from services.selenium_runner import run_test_case
from services.report_generator import generate_pdf_report
from services.result_parser import parse_results
from utils.url_validator import validate_url
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-testcase', methods=['POST'])
def generate_testcase():
    url = request.form['url']
    if not validate_url(url):
        return jsonify({'error': 'Invalid URL'}), 400

    generated_code = generate_test_case(url).strip()
    # Remove '''python and '''
    if generated_code.startswith("```python"):
        generated_code = generated_code.replace("```python", "").replace("```", "").strip()

    return jsonify({'code': generated_code})

@app.route('/run-testcase', methods=['POST'])
def run_testcase():
    test_code = request.form['testCode']
    url = request.form['url']
    
    result_data = run_test_case(test_code, url)
    parsed_result = parse_results(result_data)

    with open("results/latest_result.json", "w") as f:
        json.dump(parsed_result, f)

    generate_pdf_report(parsed_result)

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if not os.path.exists("results/latest_result.json"):
        return "No results found. Please run a test case first."
    
    with open("results/latest_result.json", "r") as f:
        result_data = json.load(f)
    return render_template("dashboard.html", result=result_data)

@app.route('/download-report')
def download_report():
    return send_file("results/report.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
