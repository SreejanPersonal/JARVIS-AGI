import json
import requests
from typing import Union, List, Dict

def generate(
    conversation: Union[str, List[Dict[str, str]]],
    model: str = 'meta-llama/Meta-Llama-3.1-405B-Instruct',
    system_prompt: str = "Be helpful and friendly. Keep your response straightforward, short, and concise.",
    max_tokens: int = 512,
    temperature: float = 0.7,
    stream: bool = True,
    chunk_size: int = 1
) -> Union[str, None]:
    """
    Generates responses using various large language models (LLMs) for conversational interactions.
    
    Args:
        conversation (Union[str, List[Dict[str, str]]]): A single user query or conversation history.
        model (str): The identifier of the LLM to be used.
        system_prompt (str): The initial system message to guide the conversation.
        max_tokens (int): The maximum number of tokens to be generated.
        temperature (float): The randomness of the LLM's output.
        stream (bool): Whether to stream the response from the LLM.
        chunk_size (int): The size of chunks to be streamed from the LLM.

    Models:
            - "meta-llama/Meta-Llama-3.1-405B-Instruct"
            - "meta-llama/Meta-Llama-3.1-70B-Instruct"
            - "meta-llama/Meta-Llama-3.1-8B-Instruct"
            - "nvidia/Nemotron-4-340B-Instruct"
            - "meta-llama/Meta-Llama-3-70B-Instruct"
            - "meta-llama/Meta-Llama-3-8B-Instruct" 
            - "mistralai/Mixtral-8x22B-Instruct-v0.1"
            - "mistralai/Mixtral-8x22B-v0.1"
            - "microsoft/WizardLM-2-8x22B"
            - "microsoft/WizardLM-2-7B"
            - "HuggingFaceH4/zephyr-orpo-141b-A35b-v0.1"
            - "google/gemma-1.1-7b-it"
            - "databricks/dbrx-instruct"
            - "mistralai/Mixtral-8x7B-Instruct-v0.1"
            - "mistralai/Mistral-7B-Instruct-v0.2"
            - "meta-llama/Llama-2-70b-chat-hf"
            - "cognitivecomputations/dolphin-2.6-mixtral-8x7b"

    Returns:
        Union[str, None]: The LLM's response if successful, otherwise None.
    """
    API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
    
    headers = {
        "Accept": "text/event-stream",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Dnt": "1",
        "Host": "api.deepinfra.com",
        "Origin": "https://deepinfra.com",
        "Referer": "https://deepinfra.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "X-Deepinfra-Source": "web-page",
    }

    if isinstance(conversation, str):
        conversation = [{"role": "user", "content": conversation}]
    elif not isinstance(conversation, list):
        raise ValueError("Conversation must be either a string or a list of dictionaries")

    conversation.insert(0, {"role": "system", "content": system_prompt})

    payload = {
        "model": model,
        "messages": conversation,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stop": [],
        "stream": True
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, stream=True)
        response.raise_for_status()
        
        full_response = ""
        for line in response.iter_lines(decode_unicode=True, chunk_size=chunk_size):
            if line.startswith("data:"):
                try:
                    content = json.loads(line[5:])
                    if content != "[DONE]":
                        delta_content = content.get("choices", [{}])[0].get("delta", {}).get("content")
                        if delta_content:
                            if stream:
                                print(delta_content, end="", flush=True)
                            full_response += delta_content

                except:
                    continue
        
        return full_response.strip()
    
    except requests.RequestException as e:
        print(f"Error occurred during API request: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    # Example usage with a single query
    single_query = "What is the capital of France?"
    response = generate(conversation=single_query, system_prompt="Be detailed", stream=True)
    # print(f"\nGenerated Response: {response}")




    # Example usage with a conversation history
    conversation_history = [
        {"role": "user", "content": "My name is Sreejan."},
        {"role": "assistant", "content": "Nice to meet you, Sreejan."},
        {"role": "user", "content": "What is my name?"}
    ]
    response = generate(conversation=conversation_history, system_prompt="Talk like Shakespeare", stream=True)
    # print(f"\nGenerated Response: {response}")








"""DEPRECATED v1.2"""


# import json
# import requests
# from typing import Union
# import os
# import re
# from dotenv import load_dotenv; load_dotenv() # Load environment variables from .env file

# def generate(conversation_history: list, model: str='meta-llama/Meta-Llama-3.1-405B-Instruct', system_prompt: str = "Be Helpful and Friendly. Keep your response straightforward, short and concise", max_tokens: int = 512, temperature: float = 0.7, stream: bool = True, chunk_size: int = 1) -> Union[str, None]:
#     """
#     Utilizes a variety of large language models (LLMs) to engage in conversational interactions.
    
#     Parameters:
#         - conversation_history (list): A list of dictionaries representing the conversation history including the system prompt.
#         - model (str): The name or identifier of the LLM to be used for conversation. Available models include various options.
#         - system_prompt (str): The initial system message to start the conversation.
#         - max_tokens (int): Optional. The maximum number of tokens to be generated by the LLM. Defaults to 512.
#         - temperature (float): Optional. The temperature of the LLM. Defaults to 0.7.
#         - stream (bool): Optional. Whether to stream the response from the LLM. Defaults to False.
#         - chunk_size (int): Optional. The size of the chunks to be streamed from the LLM. Defaults to 24.

#     Models:
#             - "meta-llama/Meta-Llama-3-70B-Instruct"
#             - "meta-llama/Meta-Llama-3-8B-Instruct" 
#             - "mistralai/Mixtral-8x22B-Instruct-v0.1"
#             - "mistralai/Mixtral-8x22B-v0.1"
#             - "microsoft/WizardLM-2-8x22B"
#             - "microsoft/WizardLM-2-7B"
#             - "HuggingFaceH4/zephyr-orpo-141b-A35b-v0.1"
#             - "google/gemma-1.1-7b-it"
#             - "databricks/dbrx-instruct"
#             - "mistralai/Mixtral-8x7B-Instruct-v0.1"
#             - "mistralai/Mistral-7B-Instruct-v0.2"
#             - "meta-llama/Llama-2-70b-chat-hf"
#             - "cognitivecomputations/dolphin-2.6-mixtral-8x7b"

#     Returns:
#         - Union[str, None]: The response message from the LLM if successful, otherwise None.
#     """
#     api_url = "https://api.deepinfra.com/v1/openai/chat/completions"
    
#     headers = {
#     "Accept": "text/event-stream",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
#     "Connection": "keep-alive",
#     "Content-Type": "application/json",
#     "Dnt": "1",
#     "Host": "api.deepinfra.com",
#     "Origin": "https://deepinfra.com",
#     "Referer": "https://deepinfra.com/",
#     "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "\"Windows\"",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-site",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
#     "X-Deepinfra-Source": "web-page",
# }
#     # Insert the system prompt at the beginning of the conversation history
#     conversation_history.insert(0, {"role": "system", "content": system_prompt})

#     payload = {
#         "model": model,
#         "messages": conversation_history,
#         "temperature": temperature,
#         "max_tokens": max_tokens,
#         "stop": [],
#         "stream": True
#     }

#     try:
#         response = requests.post(api_url, headers=headers, json=payload, stream=True)
#         streaming_text = ""
#         for value in response.iter_lines(decode_unicode=True, chunk_size=chunk_size):
#             modified_value = re.sub("data:", "", value)
#             if modified_value and "[DONE]" not in modified_value:
#                 json_modified_value = json.loads(modified_value)
#                 try:
#                     if json_modified_value["choices"][0]["delta"]["content"] != None:
#                         if stream: print(json_modified_value["choices"][0]["delta"]["content"], end="")
#                         streaming_text += json_modified_value["choices"][0]["delta"]["content"]
#                 except: continue
#         return streaming_text
    
#     except Exception as e:
#         print("Error:", e)
#         return "Response content: " + response.text


# if __name__ == "__main__":
#     # Predefined system prompt
#     system_prompt = "Be Helpful and Friendly. Keep your response straightforward, short and concise"
#     system_prompt = "Be Helpful and Friendly. Keep your response straightforward, long and detailed"
#     system_prompt = "Talk like Shakespeare"

#     # Predefined conversational history that includes providing a name and then asking the AI to recall it
#     conversation_history = [
#         {"role": "user", "content": "My name is Sreejan."},
#         {"role": "assistant", "content": "Nice to meet you, Sreejan."},
#         {"role": "user", "content": "What is my name?"}
#     ]

#     # Call the generate function with the predefined conversational history
#     response = generate(conversation_history=conversation_history, system_prompt=system_prompt, stream=True)
#     print("\n\nGenerated Response:", response)







"""DEPRECATED v1.1"""

# import json
# import requests
# from typing import Union
# import os
# import re
# from dotenv import load_dotenv; load_dotenv() # Load environment variables from .env file

# def generate(conversation_history: list, model: str='meta-llama/Meta-Llama-3-70B-Instruct', system_prompt: str = "Be Helpful and Friendly. Keep your response straightforward, short and concise", max_tokens: int = 512, temperature: float = 0.7, stream: bool = True, chunk_size: int = 24) -> Union[str, None]:
#     """
#     Utilizes a variety of large language models (LLMs) to engage in conversational interactions.
    
#     Parameters:
#         - conversation_history (list): A list of dictionaries representing the conversation history including the system prompt.
#         - model (str): The name or identifier of the LLM to be used for conversation. Available models include various options.
#         - system_prompt (str): The initial system message to start the conversation.
#         - max_tokens (int): Optional. The maximum number of tokens to be generated by the LLM. Defaults to 512.
#         - temperature (float): Optional. The temperature of the LLM. Defaults to 0.7.
#         - stream (bool): Optional. Whether to stream the response from the LLM. Defaults to False.
#         - chunk_size (int): Optional. The size of the chunks to be streamed from the LLM. Defaults to 24.

#     Returns:
#         - Union[str, None]: The response message from the LLM if successful, otherwise None.
#     """
#     api_url = "https://api.deepinfra.com/v1/openai/chat/completions"
#     headers ={
#         "Authorization" : f"Bearer {os.environ.get('DEEPINFRA')}"
#     }
    
#     # Insert the system prompt at the beginning of the conversation history
#     conversation_history.insert(0, {"role": "system", "content": system_prompt})

#     payload = {
#         "model": model,
#         "messages": conversation_history,
#         "temperature": temperature,
#         "max_tokens": max_tokens,
#         "stop": [],
#         "stream": True
#     }

#     try:
#         response = requests.post(api_url, headers=headers, json=payload, stream=True)
#         streaming_text = ""
#         for value in response.iter_lines(decode_unicode=True, chunk_size=chunk_size):
#             modified_value = re.sub("data:", "", value)
#             if modified_value and "[DONE]" not in modified_value:
#                 json_modified_value = json.loads(modified_value)
#                 try:
#                     if json_modified_value["choices"][0]["delta"]["content"] != None:
#                         if stream: print(json_modified_value["choices"][0]["delta"]["content"], end="")
#                         streaming_text += json_modified_value["choices"][0]["delta"]["content"]
#                 except: continue
#         return streaming_text
    
#     except Exception as e:
#         print("Error:", e)
#         return "Response content: " + response.text


# if __name__ == "__main__":
#     # Predefined system prompt
#     system_prompt = "Be Helpful and Friendly. Keep your response straightforward, short and concise"
#     system_prompt = "Be Helpful and Friendly. Keep your response straightforward, long and detailed"
#     system_prompt = "Talk like Shakespeare"

#     # Predefined conversational history that includes providing a name and then asking the AI to recall it
#     conversation_history = [
#         {"role": "user", "content": "My name is Sreejan."},
#         {"role": "assistant", "content": "Nice to meet you, Sreejan."},
#         {"role": "user", "content": "What is my name?"}
#     ]

#     # Call the generate function with the predefined conversational history
#     response = generate(conversation_history=conversation_history, system_prompt=system_prompt)
#     print("\n\nGenerated Response:", response)







"""DEPRECATED v1.0"""

# import json
# import requests
# from typing import Union
# import os
# import re
# from dotenv import load_dotenv; load_dotenv() # Load environment variables from .env file

# def generate(message: str, model: str='meta-llama/Meta-Llama-3-70B-Instruct', system_prompt: str = "Be Helpful and Friendly. Keep your response straightfoward, short and concise", max_tokens: int = 512, temperature: float = 0.7, stream: bool = False, chunk_size: int = 24) -> Union[str, None]:
#     """
#     Utilizes a variety of large language models (LLMs) to engage in conversational interactions.
    
#     Parameters:
#         - model (str): The name or identifier of the LLM to be used for conversation. Available models include:
#             - "meta-llama/Meta-Llama-3-70B-Instruct"
#             - "meta-llama/Meta-Llama-3-8B-Instruct" 
#             - "mistralai/Mixtral-8x22B-Instruct-v0.1"
#             - "mistralai/Mixtral-8x22B-v0.1"
#             - "microsoft/WizardLM-2-8x22B"
#             - "microsoft/WizardLM-2-7B"
#             - "HuggingFaceH4/zephyr-orpo-141b-A35b-v0.1"
#             - "google/gemma-1.1-7b-it"
#             - "databricks/dbrx-instruct"
#             - "mistralai/Mixtral-8x7B-Instruct-v0.1"
#             - "mistralai/Mistral-7B-Instruct-v0.2"
#             - "meta-llama/Llama-2-70b-chat-hf"
#             - "cognitivecomputations/dolphin-2.6-mixtral-8x7b"
#         - message (str): The message to be sent to the LLM to initiate or continue the conversation.
#         - system_prompt (str): Optional. The initial system message to start the conversation. Defaults to "Talk Like Shakespeare".
#         - max_tokens (int): Optional. The maximum number of tokens to be generated by the LLM. Defaults to 512.
#         - temperature (float): Optional. The temperature of the LLM. Defaults to 0.7.
#         - stream (bool): Optional. Whether to stream the response from the LLM. Defaults to True.
#         - chunk_size (int): Optional. The size of the chunks to be streamed from the LLM. Defaults to 24.

#     Returns:
#         - Union[str, None]: The response message from the LLM if successful, otherwise None.
#     """
#     api_url = "https://api.deepinfra.com/v1/openai/chat/completions"
#     headers ={
#         "Authorization" : f"Bearer {os.environ.get('DEEPINFRA')}"
#     }
#     payload = {
#         "model": model,
#         "messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": message}
#         ],
#         "temperature": temperature,
#         "max_tokens": max_tokens,
#         "stop": [],
#         "stream": True
#     }

    
#     try:
#         response = requests.post(api_url, headers=headers, json=payload, stream=True)
#         streaming_text = ""
#         for value in response.iter_lines(decode_unicode=True, chunk_size=chunk_size):
#             modified_value = re.sub("data:", "", value)
#             if modified_value and "[DONE]" not in modified_value:
#                 json_modified_value = json.loads(modified_value)
#                 try:
#                     if json_modified_value["choices"][0]["delta"]["content"] != None:
#                         if stream: print(json_modified_value["choices"][0]["delta"]["content"], end="")
#                         streaming_text += json_modified_value["choices"][0]["delta"]["content"]
#                 except: continue
#         return streaming_text
    
#     except Exception as e:
#         print("Error:", e)
#         return "Response content: " + response.text
    

# if __name__ == "__main__":

#     model_names = [
#         "meta-llama/Meta-Llama-3-70B-Instruct",
#         "meta-llama/Meta-Llama-3-8B-Instruct",
#         "mistralai/Mixtral-8x22B-Instruct-v0.1",
#         "mistralai/Mixtral-8x22B-v0.1",
#         "microsoft/WizardLM-2-8x22B",
#         "microsoft/WizardLM-2-7B",
#         "HuggingFaceH4/zephyr-orpo-141b-A35b-v0.1",
#         "google/gemma-1.1-7b-it",
#         "databricks/dbrx-instruct",
#         "mistralai/Mixtral-8x7B-Instruct-v0.1",
#         "mistralai/Mistral-7B-Instruct-v0.2",
#         "meta-llama/Llama-2-70b-chat-hf",
#         "cognitivecomputations/dolphin-2.6-mixtral-8x7b"
#     ]

#     for name in model_names:
#         messages =  "Introduce yourself and tell who made you and about your owner company" # Add more messages as needed
#         print(f"\n• Model: {name} -")
#         response = generate(messages, model=name, system_prompt="Respond very detailed", stream=True)
