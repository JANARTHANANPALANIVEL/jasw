import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

def get_prompt_template(website_type):
    templates = {
        'ecommerce': """
           You are an expert QA engineer. Generate a robust Selenium test script in Python to test the website: {url}.

            Requirements:
            1. Verify basic page load performance and check for errors on load.
            2. Navigate through all available links and internal pages to confirm proper redirection.
            3. Highlight each tested element with a 1px solid red border for better visual debugging.
            4. Wait 0.5 seconds after interacting with each element to simulate natural user behavior.
            5. Smoothly scroll through the page to ensure all visible and hidden elements are tested.
            6. Check the functionality of basic interactive elements like buttons, dropdowns, and text inputs.
            7. Simulate tests on multiple screen sizes: Desktop (1920x1080), Tablet (768x1024), and Mobile (375x667).
            8. Ensure that page responsiveness and layout adapt correctly on different devices.
            9. At the end, print a detailed report including:
                - PASS/FAIL/ERROR status for each step and element,
                - Total execution time,
                - Overall test score as a percentage,
                - A concise summary.
                -show me the execution timing also in seconds
            10.when testing the browser will be open and show the testing using chromewebdriver

            Output only the complete and properly indented Python code. Do not include any explanations or extra text.
                        """,
    
        'static': """
           You are an expert QA engineer. Generate a robust Selenium test script in Python to test the website: {url}.

            Requirements:
            1. Verify basic page load performance and check for errors on load.
            2. Navigate through all available links and internal pages to confirm proper redirection.
            3. Highlight each tested element with a 1px solid red border for better visual debugging.
            4. Wait 0.5 seconds after interacting with each element to simulate natural user behavior.
            5. Smoothly scroll through the page to ensure all visible and hidden elements are tested.
            6. Check the functionality of basic interactive elements like buttons, dropdowns, and text inputs.
            7. Simulate tests on multiple screen sizes: Desktop (1920x1080), Tablet (768x1024), and Mobile (375x667).
            8. Ensure that page responsiveness and layout adapt correctly on different devices.
            9. At the end, print a detailed report including:
                - PASS/FAIL/ERROR status for each step and element,
                - Total execution time,
                - Overall test score as a percentage,
                - A concise summary.
                -show me the execution timing also in seconds
            10.when testing the browser will be open and show the testing using chromewebdriver

            Output only the complete and properly indented Python code. Do not include any explanations or extra text.
        """,
        'dynamic': """
           You are an expert QA engineer. Generate a robust Selenium test script in Python to test the website: {url}.

            Requirements:
            1. Verify basic page load performance and check for errors on load.
            2. Navigate through all available links and internal pages to confirm proper redirection.
            3. Highlight each tested element with a 1px solid red border for better visual debugging.
            4. Wait 0.5 seconds after interacting with each element to simulate natural user behavior.
            5. Smoothly scroll through the page to ensure all visible and hidden elements are tested.
            6. Check the functionality of basic interactive elements like buttons, dropdowns, and text inputs.
            7. Simulate tests on multiple screen sizes: Desktop (1920x1080), Tablet (768x1024), and Mobile (375x667).
            8. Ensure that page responsiveness and layout adapt correctly on different devices.
            9. At the end, print a detailed report including:
                - PASS/FAIL/ERROR status for each step and element,
                - Total execution time,
                - Overall test score as a percentage,
                - A concise summary.
                -show me the execution timing also in seconds
            10.when testing the browser will be open and show the testing using chromewebdriver

            Output only the complete and properly indented Python code. Do not include any explanations or extra text.

        """,
        'other': """
           You are an expert QA engineer. Generate a robust Selenium test script in Python to test the website: {url}.

            Requirements:
            1. Verify basic page load performance and check for errors on load.
            2. Navigate through all available links and internal pages to confirm proper redirection.
            3. Highlight each tested element with a 1px solid red border for better visual debugging.
            4. Wait 0.5 seconds after interacting with each element to simulate natural user behavior.
            5. Smoothly scroll through the page to ensure all visible and hidden elements are tested.
            6. Check the functionality of basic interactive elements like buttons, dropdowns, and text inputs.
            7. Simulate tests on multiple screen sizes: Desktop (1920x1080), Tablet (768x1024), and Mobile (375x667).
            8. Ensure that page responsiveness and layout adapt correctly on different devices.
            9. At the end, print a detailed report including:
                - PASS/FAIL/ERROR status for each step and element,
                - Total execution time,
                - Overall test score as a percentage,
                - A concise summary.
                -show me the execution timing also in seconds
            10.when testing the browser will be open and show the testing using chromewebdriver

            Output only the complete and properly indented Python code. Do not include any explanations or extra text.

        """
    }
    return templates.get(website_type, templates['other'])

def generate_test_case(url, website_type, custom_prompt=''):
    base_prompt = get_prompt_template(website_type).format(url=url)
    final_prompt = base_prompt + '\n' + custom_prompt if custom_prompt else base_prompt
    
    response = model.generate_content(final_prompt)
    test_code = response.text
    
    # Add imports and setup
    final_code = f"""
{test_code}
"""
    return final_code