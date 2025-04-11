import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_test_case(url):
    prompt = f"""
    write a selinium testcase for given websit link {url}


            1) check all the functionality
            2) highlight the checking element in 1px red borderbox
            3) take 0.8sec for checking all the elements and functionality
            4) autoscroll while checking
            5) give me a report like passed, failed, error, run time and website best in percentage
            6) check all the pages and also use wrong password also to check the functionality also
            7) check in different screen sizes also
    """
    model = genai.GenerativeModel('models/gemini-1.5-pro')
    response = model.generate_content(prompt)
    return response.text
