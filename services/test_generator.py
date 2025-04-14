import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def generate_testcase(url):
    prompt = f"""
        You are an expert QA engineer. Generate a robust Selenium test script in Python to test the website: {url}.

        Requirements:
        1. Check page load and all functionality by analyzing the website.
        2. Highlight each tested element with a 1px solid red border.
        3. Wait 0.8 seconds after interacting with each element.
        4. Smoothly scroll through the entire page to ensure all elements are tested.
        5. Visit and test all internal pages linked from the given URL.
        6. Test the functionality of all interactive elements (e.g., buttons, forms, links,input forms).
        7. Simulate tests in multiple screen sizes: desktop (1920x1080), tablet (768x1024), and mobile (375x667).
        8. At the end, print a detailed report including:
        - PASS/FAIL/ERROR status for each step and element,
        - Total execution time,
        - Overall test score as a percentage,
        - A concise summary.
        9. Do not use the unittest module.
        

        Output only the complete and properly indented Python code. Do not include any explanations or extra text.
"""

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text

