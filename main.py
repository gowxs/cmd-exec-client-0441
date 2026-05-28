import os
import requests
import json
import sys

def execute_command(command: str, api_base_url: str, bearer_token: str) -> dict:
    """
    Sends a command to the command execution bridge API.

    Args:
        command: The command string to execute.
        api_base_url: The base URL of the API (e.g., "http://localhost:8000").
        bearer_token: The Bearer token for authentication.

    Returns:
        A dictionary representing the JSON response from the API.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails or
                                             returns a non-2xx status code.
    """
    execute_url = f"{api_base_url}/api/execute"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }
    payload = {"command": command}

    print(f"[INFO] Attempting to send command: '{command}' to {execute_url}")

    try:
        response = requests.post(execute_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP Error: {e}", file=sys.stderr)
        print(f"[ERROR] Response status: {e.response.status_code}", file=sys.stderr)
        print(f"[ERROR] Response body: {e.response.text}", file=sys.stderr)
        raise
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Connection Error: Could not connect to {execute_url}. Is the API running and accessible?", file=sys.stderr)
        raise
    except requests.exceptions.Timeout as e:
        print(f"[ERROR] Timeout Error: The request to {execute_url} timed out.", file=sys.stderr)
        raise
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An unexpected request error occurred: {e}", file=sys.stderr)
        raise

def main():
    api_base_url = os.environ.get("API_BASE_URL")
    bearer_token = os.environ.get("BEARER_TOKEN")

    if not api_base_url:
        print("\n[ERROR] API_BASE_URL environment variable not set.", file=sys.stderr)
        print("        Please set it to the base URL of your API (e.g., http://localhost:8000).", file=sys.stderr)
        sys.exit(1)

    if not bearer_token:
        print("\n[ERROR] BEARER_TOKEN environment variable not set.", file=sys.stderr)
        print("        Please set it to the Bearer token used for /api/autonomous/build.", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Using API Base URL: {api_base_url}")

    # Verify connection by executing 'whoami' as requested
    print("\n--- Verifying connection with 'whoami' ---")
    try:
        whoami_result = execute_command("whoami", api_base_url, bearer_token)
        print("\n[SUCCESS] 'whoami' command executed successfully!")
        print("API Response:")
        print(json.dumps(whoami_result, indent=2))
        print("\n--- Connection verification complete ---")
    except requests.exceptions.RequestException:
        print("\n[FATAL] Failed to execute 'whoami' command. Please check your API_BASE_URL, BEARER_TOKEN, and API server status.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
