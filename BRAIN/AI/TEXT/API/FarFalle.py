import requests
import json
import re
from typing import List, Dict, Optional

class FarFalle:
    """A class to interact with the FarFalle chat service.

    Attributes:
        session: A requests.Session object for making HTTP requests.
        url: The URL endpoint for the FarFalle chat service.
    """

    def __init__(self):
        """Initializes the FarFalle class with a session and the service URL."""
        self.session: requests.Session = requests.Session()
        self.url: str = "https://farfalle.onrender.com/chat"

    def generate(self, conversation_history: List[Dict[str, str]], model: Optional[str] = 'llama-3-70b', stream: Optional[bool] = False) -> tuple[str, dict]:
        """Generates a response from the FarFalle chat service.

        Args:
            conversation_history: A list of dictionaries containing the conversation history.
            model: The model name to use for generating the response. Defaults to 'llama-3-70b'.
            stream: If True, prints the content as it arrives. Defaults to False.

        Available models: 'llama-3-70b', 'gpt-3.5-turbo', 'gpt-4o'.

        Returns:
            A tuple containing the generated response as a string and the sources as a dictionary.
        """
        # Extract the last user query from the conversation_history and remove it from the conversation_history list
        # Extract the last user query and update conversation_history in one line
        query, conversation_history = next(((item['content'], conversation_history[:i] + conversation_history[i+1:]) for i, item in enumerate(reversed(conversation_history)) if item['role'] == 'user'), ('', conversation_history))

        # Prepare the payload with the extracted query and the updated conversation_history
        payload = {
            "query": query,
            "history": conversation_history,
            "model": model
        }

        content = ""
        sources = {}
        # Make the POST request and stream the response
        response = self.session.post(self.url, json=payload, stream=True)
        for line in response.iter_lines(decode_unicode=True, chunk_size=1):
            if line:
                modified_line = re.sub("data:", "", line)
                try:
                    json_data = json.loads(modified_line)
                    if not sources:
                        sources = json_data
                    content += json_data['data']['text']
                    if stream:
                        print(json_data['data']['text'], end="", flush=True)
                except: continue
        return content, sources

    def process_sources(self, sources: dict) -> tuple[List[Dict[str, str]], List[str]]:
        """Processes the sources dictionary to extract relevant information.

        Args:
            sources: A dictionary containing the sources data.

        Returns:
            A tuple containing a list of dictionaries with title, url, and content for each result,
            and a list of image URLs.
        """
        results = []
        images = []

        for result in sources['data']['results']:
            results.append({
                'title': result['title'],
                'url': result['url'],
                'content': result['content']
            })

        images = sources['data']['images']

        return results, images

if __name__ == "__main__":
    farfalle = FarFalle()

    conversation_history = [
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
        {"role": "user", "content": "And what is its population?"}
    ]

    # Example without streaming
    # response, sources = farfalle.generate(conversation_history, model='gpt-3.5-turbo')
    # print("Response:", response)
    # results, images = farfalle.process_sources(sources)
    # print("Results:", results)
    # print("Images:", images)

    # Example with streaming
    print("\nStreaming response:")
    response, sources = farfalle.generate(conversation_history, model='gpt-4o', stream=True)
    results, images = farfalle.process_sources(sources)
    print("\033[91m\nResults:", results , "\033[0m")
    print("\033[96mImages:", images, "\033[0m")
