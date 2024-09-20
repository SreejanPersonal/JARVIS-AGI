import requests
from typing import Optional, Dict, List
import time

def generate(
        conversation_history: List[Dict[str, str]],
        system_prompt: Optional[str] = "Be Helpful and Friendly"
    ) -> str:
    """
    Interacts with the BasedGPT API to generate a response based on a given conversation history.

    Args:
        conversation_history: A list of dictionaries representing the conversation history. Each dictionary should have
                    keys "role" and "content" indicating the speaker and their message.
        system_prompt: An optional system prompt to guide the AI's behavior.

    Returns:
        A string containing the complete AI-generated response.
    """

    url = "https://www.basedgpt.chat/api/chat"

    if system_prompt:
        conversation_history.insert(0, {"role": "system", "content": system_prompt})

    payload = {"messages": conversation_history}

    response = requests.post(url, json=payload, stream=True)
    complete_response = ""

    for chunk in response.iter_content(decode_unicode=True, chunk_size=1):
        if type(chunk) == bytes:
            chunk = chunk.decode("utf-8")  # Convert bytes to string
        complete_response += chunk
        print(chunk, end="", flush=True)

    return complete_response

if __name__ == "__main__":
    # Example usage
    conversation_history = [{"role": "user", "content": "write 10 lines on India"}]
    start_time = time.time()
    response = generate(conversation_history)
    end_time = time.time()
    print(f"\033[92m\n\nResponse took {end_time - start_time:.2f} seconds to generate.\033[0m")
