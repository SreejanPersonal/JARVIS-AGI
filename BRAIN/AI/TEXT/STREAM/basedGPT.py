import requests
import re
from typing import Optional, Dict, List, Generator

def generate(conversation_history: List[Dict[str, str]], system_prompt: Optional[str] = "Be Helpful and Friendly") -> Generator[str, None, None]:
    """
    Connects with the BasedGPT API to generate a contextually relevant response based on the provided 
    conversation history. Yields sentences from the AI's response as they are generated, creating a 
    dynamic and engaging conversational experience.

    Args:
        conversation_history (List[Dict[str, str]]): A chronological record of the conversation represented as 
                                                    a list of dictionaries. Each dictionary should contain the keys 
                                                    "role" and "content" indicating the speaker (either "user" or "system") 
                                                    and their corresponding message.
        system_prompt (str, optional):  A guiding statement to set the AI's initial behavior and personality. 
                                            Defaults to "Be Helpful and Friendly".

    Yields:
        Generator[str, None, None]:  A generator that yields individual sentences from the AI's response as 
                                    they are constructed, simulating a natural conversational flow.
    """

    api_endpoint = "https://www.basedgpt.chat/api/chat"

    if system_prompt:
        conversation_history.insert(0, {"role": "system", "content": system_prompt})

    request_data = {"messages": conversation_history}

    api_response = requests.post(api_endpoint, json=request_data, stream=True)
    partial_sentence = ""

    for data_chunk in api_response.iter_content(decode_unicode=True, chunk_size=1):
        if isinstance(data_chunk, bytes):
            data_chunk = data_chunk.decode("utf-8")
        partial_sentence += data_chunk
        print(data_chunk, end="", flush=True)
        # Enhanced sentence boundary detection accommodating multi-digit numbers
        sentences = re.split(r'(?<!\b\w\.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', partial_sentence)
        for complete_sentence in sentences[:-1]:
            yield complete_sentence.strip()
        partial_sentence = sentences[-1] 

    # Yield any remaining portion of the incomplete sentence
    if partial_sentence:
        yield partial_sentence.strip()

if __name__ == "__main__":
    # Illustrative Example
    conversation_log = [{"role": "user", "content": "Write 10 lines about India. Also Give Number to Each Line"}]
    for statement in generate(conversation_log, "Be Helpful and Friendly"):
        print(f"\n\033[91mAI:\033[0m \033[92m{statement}\033[0m")