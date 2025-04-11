import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def generate_testcase(url):
    prompt = f"""
You are an expert QA engineer. Generate a robust Selenium test script in Python to test the website: {url}.

Requirements:
1. Check page load and all functionality by analyzing the website
2. Highlight each element tested with a 1px red border.
3. Wait 0.8 seconds after interacting with each element.
4. Scroll the page to ensure all elements are tested.
5. check all the pages and elements fucntionality 
6. Test in multiple screen sizes (desktop, tablet, mobile).
7. Print a report with:
   - PASS/FAIL/ERROR for each step,
   - execution time,
   - overall test score in percentage,
   - summary at the end.

Output only the full Python code with proper indentation. No explanations.
"""

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text
