import requests
import re
from typing import Tuple, Optional

def generate(prompt: str, system_prompt: str = " Don't Write Code unless Mentioned", web_access: bool = True, stream: bool = True) -> Tuple[Optional[str], str]:
    """
    Generates a response for the given prompt using the Blackbox.ai API.

    Parameters:
    - prompt (str): The prompt to generate a response for.
    - system_prompt (str): The system prompt to be used in the conversation. Defaults to "Don't Write Code unless Mentioned".
    - web_access (bool): A flag indicating whether to access web resources during the conversation. Defaults to True.
    - prints (bool): A flag indicating whether to print the conversation messages. Defaults to True.

    Returns:
    - Tuple[Optional[str], str]: A tuple containing the sources of the conversation (if available) and the complete response generated.
    """

    chat_endpoint = "https://www.blackbox.ai/api/chat"

    payload = {
        "messages": [{"content": system_prompt, "role": "system"}, {"content": prompt, "role": "user"}],
        "agentMode": {},
        "trendingAgentMode": {},
    }
    
    if web_access:
        payload["codeModelMode"] = web_access

    response = requests.post(chat_endpoint, json=payload, stream=True)

    sources = None
    resp = ""

    for text_stream in response.iter_lines(decode_unicode=True, delimiter="\n"):
        if text_stream:
            if sources is None: sources = text_stream
            else:
                if stream: print(text_stream)
                resp += text_stream + "\n"

    if sources: 
        if stream: print(re.sub(r'\$@\$\w+=v\d+\.\d+\$@\$', '', sources))
    return sources, resp


# Example usage:
if __name__ == "__main__":

    query = "When did IPL 2024 start and end? Please provide a detailed response."
    query = "Write 30 Lines on India."
    sources, resp = generate(query, web_access=False, stream=True)
