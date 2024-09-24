import requests
from typing import Union, Dict

def generate(
    prompt: str,
    model: str = "mistrallarge",
    timeout: int = 30,
    proxies: Dict[str, str] = {},
    stream: bool = True
) -> Union[str, None]:
    """
    Generates text based on the given prompt and model.

    Args:
    - prompt (str): The input prompt to generate text from.
    - model (str): The model to use for text generation. Defaults to "mistrallarge".
    - max_tokens (int): The maximum number of tokens to generate. Defaults to 600.
    - timeout (int): The timeout in seconds for the API request. Defaults to 30.
    - proxies (Dict[str, str]): A dictionary of proxies to use for the API request. Defaults to an empty dictionary.
    - temperature (float): The temperature to use for text generation. Defaults to 1.
    - top_p (float): The top-p to use for text generation. Defaults to 1.
    - stream (bool): Whether to stream the response or not. Defaults to True.

    Returns:
    - Union[str, None]: The generated text or None if an error occurs.
    """

    # Define the available models
    available_models = [
        "gemini",  # Gemini 1.5pro
        "claude",  # Claude 3.5
        "gpt4",  # GPT4o
        "mistrallarge"  # Mistral Large2
    ]

    # Check if the model is valid
    if model not in available_models:
        raise ValueError(f"Invalid model: {model}. Choose from: {available_models}")

    # Define the API endpoint and headers
    api_endpoint = "https://editee.com/submit/chatgptfree"
    headers = {
        "Authority": "editee.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://editee.com",
        "Referer": "https://editee.com/chat-gpt",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    # Define the payload
    payload = {
        "context": " ",
        "selected_model": model,
        "template_id": "",
        "user_input": prompt
    }

    try:
        # Make the API request
        response = requests.post(
            api_endpoint,
            json=payload,
            headers=headers,
            timeout=timeout,
            proxies=proxies
        )

        # Check if the response was successful
        response.raise_for_status()

        # Get the response JSON
        resp = response.json()

        # Get the full response text
        full_response = resp.get('text', '')

        # If streaming is enabled, print the response
        if stream:
            print(full_response, end="", flush=True)

        # Return the full response text
        return full_response.strip()

    except requests.RequestException as e:
        # Print the error message
        print(f"Error occurred during API request: {e}")

        # If the response is not None, print the response content
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")

        # Return None
        return None

# Example usage:
if __name__ == '__main__':
    while True:
        response = generate(prompt="Who are you. Explain in Short", stream=True, model="claude")
        print("\033[92m\n\nGenerated response:", response, "\033[0m")
