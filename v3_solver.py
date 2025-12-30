import time
from helium import *
from selenium.webdriver import ChromeOptions
from src.core_solver import solve_captcha, human_delay

# --- Specific reCAPTCHA v3 Solver Logic ---

def solve_recaptcha_v3(
    site_key: str,
    page_url: str,
    action: str = "verify",
    min_score: float = 0.7
) -> str:
    """
    Solves reCAPTCHA v3 using CapSolver API.
    
    Args:
        site_key: The site key of the reCAPTCHA.
        page_url: The URL where the CAPTCHA appears.
        action: The action parameter for v3.
        min_score: The minimum score required.
        
    Returns:
        The g-recaptcha-response token.
    """
    task_payload = {
        "type": "ReCaptchaV3TaskProxyLess",
        "websiteURL": page_url,
        "websiteKey": site_key,
        "pageAction": action,
        "minScore": min_score
    }
    
    print(f"  Submitting reCAPTCHA v3 task (Action: {action}, Min Score: {min_score}) to CapSolver...")
    solution = solve_captcha(task_payload)
    return solution["gRecaptchaResponse"]


def main():
    # NOTE: Replace with a real target URL and site key for testing
    target_url = "https://your-target-site-with-recaptcha-v3.com"
    recaptcha_v3_key = "6LcXXXXXXXXXXXXXXXXXXXXXXXXX"

    # Setup headless browser for v3 (Best Practice)
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    start_chrome(target_url, options=options)
    driver = get_driver()

    try:
        # 1. Solve reCAPTCHA v3 with "login" action
        print("Solving reCAPTCHA v3...")
        token = solve_recaptcha_v3(
            recaptcha_v3_key,
            target_url,
            action="login",
            min_score=0.9
        )
        print(f"Got token: {token[:50]}...")

        # 2. Inject the token
        driver.execute_script(f'''
            var responseField = document.querySelector('[name="g-recaptcha-response"]');
            if (responseField) {{
                responseField.value = '{token}';
            }}
            // Call callback if exists
            if (typeof onRecaptchaSuccess === 'function') {{
                onRecaptchaSuccess('{token}');
            }}
        ''')
        human_delay()

        print("reCAPTCHA v3 token injected!")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

    finally:
        kill_browser()


if __name__ == "__main__":
    main()
