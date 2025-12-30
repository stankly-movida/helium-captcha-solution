import time
import requests
import os

# --- Configuration ---
CAPSOLVER_API = "https://api.capsolver.com"
# Read API key from environment variable for security
CAPSOLVER_API_KEY = os.environ.get("CAPSOLVER_API_KEY", "YOUR_API_KEY") 
# Fallback to "YOUR_API_KEY" if environment variable is not set (for demonstration)

def create_task(task_payload: dict) -> str:
    """
    Creates a CAPTCHA solving task with CapSolver and returns the task ID.
    
    Args:
        task_payload: Dictionary containing the specific CAPTCHA task details.
        
    Returns:
        The ID of the created task.
        
    Raises:
        Exception: If the API returns an error.
    """
    response = requests.post(
        f"{CAPSOLVER_API}/createTask",
        json={
            "clientKey": CAPSOLVER_API_KEY,
            "task": task_payload
        }
    )
    result = response.json()
    if result.get("errorId") != 0:
        raise Exception(f"CapSolver API Error: {result.get('errorDescription')}")
    return result["taskId"]


def get_task_result(task_id: str, max_attempts: int = 120) -> dict:
    """
    Polls for the task result until solved or timeout.
    
    Args:
        task_id: The ID of the task to poll.
        max_attempts: Maximum number of attempts before timing out.
        
    Returns:
        The solution dictionary from CapSolver.
        
    Raises:
        Exception: If the task fails.
        TimeoutError: If the task times out.
    """
    for _ in range(max_attempts):
        response = requests.post(
            f"{CAPSOLVER_API}/getTaskResult",
            json={
                "clientKey": CAPSOLVER_API_KEY,
                "taskId": task_id
            }
        )
        result = response.json()

        if result.get("status") == "ready":
            return result["solution"]
        elif result.get("status") == "failed":
            raise Exception(f"Task Failed: {result.get('errorDescription')}")

        time.sleep(1)

    raise TimeoutError("CAPTCHA solving timed out after max attempts.")


def solve_captcha(task_payload: dict) -> dict:
    """
    Complete CAPTCHA solving workflow: create task and poll for result.
    
    Args:
        task_payload: Dictionary containing the specific CAPTCHA task details.
        
    Returns:
        The solution dictionary.
    """
    task_id = create_task(task_payload)
    return get_task_result(task_id)

def human_delay(min_sec=1.0, max_sec=3.0):
    """Random delay to mimic human behavior."""
    import random
    time.sleep(random.uniform(min_sec, max_sec))

if __name__ == "__main__":
    # Example usage (requires a valid API key and task payload)
    print("Core solver functions loaded. Run specific examples in the 'src' directory.")
