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
4. smooth Scroll the page to ensure all elements are tested.
5. the generated testcase aso check all the pages that contain in that given url and also check all the element functionality like btns
6. Test in multiple screen sizes (desktop, tablet, mobile).
7. Print a report with:
   - PASS/FAIL/ERROR for each elements and step,
   - execution time,
   - overall test score in percentage,
   - summary at the end.
8. dont use unittest module


Output only the full Python code with proper indentation. No explanations.
"""

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text

