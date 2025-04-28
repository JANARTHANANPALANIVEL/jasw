import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def get_prompt_template(website_type):
    templates = {
        'ecommerce': """
                                    You are an expert QA engineer. Generate a robust Selenium test script in Python to test the e-commerce website: {url}.

                        Requirements:
                        1. Check if the home page loads correctly and displays featured products.
                        2. Test the search functionality by searching for a sample product.
                        3. Visit product detail pages, verify product images, descriptions, and prices.
                        4. Test "Add to Cart" functionality, check cart updates, and verify correct pricing.
                        5. Simulate removing a product from the cart and updating quantity.
                        6. Test the checkout flow up to the payment page (no actual payment needed).
                        7. Fill and submit user forms like Login, Signup, and Contact forms.
                        8. Test navigation across all major categories and apply filters/sorting.
                        9. Check responsive behavior on screen sizes: Desktop (1920x1080), Tablet (768x1024), and Mobile (375x667).
                        10. Highlight each tested element with a 1px solid red border 
                        11. Wait for 0.5 seconds after interacting with each element to mimic real user interaction.
                        12. Smoothly scroll through the entire page to ensure lazy-loaded elements are captured.
                        13. Visit and test all internal links and important pages linked from the given URL.
                        14. At the end, print a detailed report including:
                            - PASS/FAIL/ERROR status for each tested functionality and element,
                            - Total execution time,
                            - Overall test score as a percentage,
                            - A concise summary.
                       

                        Output only the complete and properly indented Python code. Do not include any explanations or extra text.
                        """,
    
        'static': """
            You are an expert QA engineer. Generate a robust Selenium test script in Python to test the static website: {url}.

                Requirements:
                1. Check that the home page loads correctly and displays all key sections.
                2. Verify that all navigation links (menu, header, footer) work properly.
                3. Check for broken images or missing resources across all pages.
                4. Fill and submit all available forms (e.g., Contact Us) and validate success messages.
                5. Test internal links and ensure all pages are accessible from the home page.
                6. Test responsive behavior by simulating screen sizes: Desktop (1920x1080), Tablet (768x1024), and Mobile (375x667).
                7. Highlight each tested element with a 1px solid red border to improve visibility.
                8. Wait for 0.5 seconds after each interaction to simulate real user experience.
                9. Smoothly scroll through pages to ensure lazy-loaded sections are fully tested.
                10. Visit and test all important linked pages from the given URL.
                11. At the end, print a detailed report including:
                    - PASS/FAIL/ERROR status for each tested element or action,
                    - Total execution time,
                    - Overall test score as a percentage,
                    - A concise summary.
               

                Output only the complete and properly indented Python code. Do not include any explanations or extra text
        """,
        'dynamic': """
            You are an expert QA engineer. Generate a robust Selenium test script in Python to test the dynamic website: {url}.

            Requirements:
            1. Verify that dynamically loaded content is displayed correctly after page interactions.
            2. Test that form submissions update the page content without requiring a full page reload.
            3. Validate that any loading indicators (e.g., spinners, progress bars) appear and disappear properly.
            4. Simulate infinite scrolling if available, ensuring additional content loads successfully.
            5. Test real-time notifications, pop-ups, or UI messages that update without refreshing the page.
            6. Simulate screen sizes: Desktop (1920x1080), Tablet (768x1024), and Mobile (375x667) to verify responsive behavior.
            7. Highlight each tested element with a 1px solid red border for easy identification.
            8. Wait 0.5 seconds after each action to simulate real user behavior.
            9. Smoothly scroll through the page to ensure all elements (including dynamically loaded ones) are covered.
            10. Visit and interact with all major sections of the website that rely on dynamic behavior.
            11. At the end, print a detailed report including:
                - PASS/FAIL/ERROR status for each tested action or element,
                - Total execution time,
                - Overall test score as a percentage,
                - A concise summary.

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