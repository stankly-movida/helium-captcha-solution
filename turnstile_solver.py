import time
from helium import *
from selenium.webdriver import ChromeOptions
from src.core_solver import solve_captcha, human_delay

# --- Specific Turnstile Solver Logic ---

def solve_turnstile(site_key: str, page_url: str) -> str:
    """
    Solves Cloudflare Turnstile using CapSolver API.
    
    Args:
        site_key: The site key of the Turnstile challenge.
        page_url: The URL where the CAPTCHA appears.
        
    Returns:
        The Turnstile token.
    """
    task_payload = {
        "type": "AntiTurnstileTaskProxyLess",
        "websiteURL": page_url,
        "websiteKey": site_key,
    }
    
    print("  Submitting Turnstile task to CapSolver...")
    solution = solve_captcha(task_payload)
    return solution["token"]


def main():
    # NOTE: Replace with a real target URL and site key for testing
    target_url = "https://your-target-site-with-turnstile.com"
    turnstile_site_key = "0x4XXXXXXXXXXXXXXXXX"  # Find this in the page source

    # Configure browser
    options = ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')

    start_chrome(target_url, options=options)
    driver = get_driver()

    try:
        # Wait for Turnstile to load
        human_delay(3, 5)

        # 1. Solve the CAPTCHA
        print("Solving Turnstile...")
        token = solve_turnstile(turnstile_site_key, target_url)
        print(f"Got token: {token[:50]}...")

        # 2. Inject the token
        driver.execute_script(f'''
            document.querySelector('input[name="cf-turnstile-response"]').value = "{token}";

            // Trigger callback if present
            const callback = document.querySelector('[data-callback]');
            if (callback) {{
                const callbackName = callback.getAttribute('data-callback');
                if (window[callbackName]) {{
                    window[callbackName]('{token}');
                }}
            }}
        ''')
        human_delay()

        # 3. Submit the form using Helium
        if Button("Submit").exists():
            click("Submit")

        print("Turnstile bypassed!")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

    finally:
        kill_browser()


if __name__ == "__main__":
    main()
