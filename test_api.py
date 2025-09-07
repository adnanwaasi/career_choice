import requests
import logging
from typing import Dict, Any

API_URL = "http://127.0.0.1:8000/model-response"

payload = {
    "prompt": "What course should I take?"
}

def get_api_response(url: str, data: Dict[str, Any]) -> None:
    """Send a POST request to the FastAPI model endpoint and print the response."""
    try:
        response = requests.post(url, json=data, timeout=1000)
        response.raise_for_status()
        try:
            result = response.json()
            print("Success! Response from API:")
            print(result)
        except ValueError:
            logging.error("Response content is not valid JSON.")
            print("Error: Response is not valid JSON.")
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP error occurred: {errh}")
        print(f"HTTP error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Connection error occurred: {errc}")
        print(f"Connection error: {errc}")
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout error occurred: {errt}")
        print(f"Timeout error: {errt}")
    except requests.exceptions.RequestException as err:
        logging.error(f"An error occurred: {err}")
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    get_api_response(API_URL, payload)
