import time
from helium import *
from selenium.webdriver import ChromeOptions
from src.core_solver import solve_captcha, human_delay

# --- Specific reCAPTCHA v2 Solver Logic ---

def solve_recaptcha_v2(site_key: str, page_url: str) -> str:
    """
    Solves reCAPTCHA v2 using CapSolver API.
    
    Args:
        site_key: The site key of the reCAPTCHA.
        page_url: The URL where the CAPTCHA appears.
        
    Returns:
        The g-recaptcha-response token.
    """
    task_payload = {
        "type": "ReCaptchaV2TaskProxyLess",
        "websiteURL": page_url,
        "websiteKey": site_key,
    }
    
    print("  Submitting reCAPTCHA v2 task to CapSolver...")
    solution = solve_captcha(task_payload)
    return solution["gRecaptchaResponse"]


def main():
    target_url = "https://www.google.com/recaptcha/api2/demo"

    # Configure browser with anti-detection options (Best Practice)
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')

    print("Starting browser with anti-detection flags...")
    start_chrome(target_url, options=options)
    driver = get_driver() # Access the underlying Selenium driver

    try:
        human_delay()

        # 1. Auto-detect site key from page
        recaptcha_element = driver.find_element("css selector", ".g-recaptcha")
        site_key = recaptcha_element.get_attribute("data-sitekey")
        print(f"Detected site key: {site_key}")

        # 2. Solve the CAPTCHA
        print("\nSolving reCAPTCHA v2 with CapSolver...")
        token = solve_recaptcha_v2(site_key, target_url)
        print(f"Got token: {token[:50]}...")

        # 3. Inject the token
        print("\nInjecting token...")
        driver.execute_script(f'''
            var responseField = document.getElementById('g-recaptcha-response');
            responseField.style.display = 'block';
            responseField.value = '{token}';
        ''')
        print("Token injected!")
        human_delay()

        # 4. Submit using Helium's simple syntax
        print("\nSubmitting form...")
        click("Submit")
        human_delay(3, 5)

        # 5. Check for success
        if "Verification Success" in driver.page_source:
            print("\n=== SUCCESS! ===")
            print("reCAPTCHA was solved and form was submitted!")
        else:
            print("\n=== FAILURE! ===")
            print("Form submission failed or verification text not found.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

    finally:
        kill_browser()


if __name__ == "__main__":
    main()
