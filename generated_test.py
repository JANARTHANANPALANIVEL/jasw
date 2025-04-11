import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import datetime

class WebsiteFunctionalityTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # Or whichever browser you prefer
        self.driver.maximize_window() # Start maximized to minimize initial resizing
        self.start_time = datetime.datetime.now()
        self.passed_tests = 0
        self.failed_tests = 0
        self.errors = 0

    def highlight_element(self, element):
        self.driver.execute_script("arguments[0].style.border='1px solid red';", element)
        time.sleep(0.4)  # Adjust highlight duration if needed
        self.driver.execute_script("arguments[0].style.border='';", element)  # Remove highlight


    def test_website_functionality(self):
        try:
            self.driver.get("https://janarthananpalanivel.vercel.app/")
            time.sleep(0.8) # Initial page load

            # Example: Check Navigation Links (Adapt as needed for your site)
            nav_links = self.driver.find_elements(By.CSS_SELECTOR, "nav a") # Adjust CSS selector
            for link in nav_links:
                self.highlight_element(link)  # Highlight
                link_text = link.text
                try:
                    link.click()
                    time.sleep(0.8)
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll
                    time.sleep(0.4)
                    self.driver.back() # Return to home
                    self.passed_tests += 1
                    print(f"PASSED: Navigation to {link_text}")
                except Exception as e:
                    self.errors += 1
                    print(f"ERROR: Navigation to {link_text}: {e}")


            # Example: Form Submission (adjust selectors for your form)
            try:
                self.driver.find_element(By.ID, "name").send_keys("Test User")  # Adjust ID
                self.driver.find_element(By.ID, "email").send_keys("test@example.com") # Adjust
                self.driver.find_element(By.ID, "message").send_keys("Test message") # Adjust
                # ... other form fields
                submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']") # Adjust
                self.highlight_element(submit_button)
                submit_button.click()
                time.sleep(0.8)
                # Add assertions to check for successful form submission
                self.passed_tests += 1
                print("PASSED: Form submission") 
            except Exception as e:
                self.failed_tests += 1
                print(f"FAILED: Form submission: {e}")

            # ... (Add more tests for other functionalities, pages, responsive design) ...

            # Example Responsive Design Test:
            self.driver.set_window_size(375, 812) # Example: iPhone X size
            time.sleep(0.8)
            # Add assertions to check layout or element visibility at this size

            self.driver.set_window_size(1920, 1080) # Back to larger size

            # Test wrong password (if applicable):
            # ...locate login elements, enter incorrect password, assert error message...


        except Exception as e:
            self.errors += 1
            print(f"Unexpected Error: {e}")


    def tearDown(self):
        self.end_time = datetime.datetime.now()
        runtime = (self.end_time - self.start_time).total_seconds()

        total_tests = self.passed_tests + self.failed_tests + self.errors
        if total_tests > 0:
            pass_percentage = (self.passed_tests / total_tests) * 100
        else:
            pass_percentage = 0  # Avoid division by zero if no tests run

        print("\nTest Report:")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Errors: {self.errors}")
        print(f"Runtime: {runtime:.2f} seconds")
        print(f"Website Quality (Estimated): {pass_percentage:.2f}%") 

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()