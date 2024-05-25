import requests
import re
import json

def generate(prompt: dict, system_prompt: str = "Be Helpful and Friendly", model: str = "Phind Instant", stream_chunk_size: int = 12, stream: bool = True) -> str:
    """
    Generates a response from the Phind Instant model based on the given prompt.

    Parameters:
    - prompt (dict): The input text to which the model will respond in a dictionary format.
    - system_prompt (str, optional): The system prompt to use for the model. Defaults to "Be Helpful and Friendly".    
    - model (str, optional): The model to use for generating the response. 
                                        Available Models: 
                                            - "Phind-34B"
                                            - "Phind Instant"
    - stream_chunk_size (int, optional): The number of bytes to read from the response stream. Defaults to 64.
    - stream (bool, optional): Whether to stream the response. Defaults to True.
                                            
    Returns:
    - str: The generated text response from the model.

    This function initializes a session with the Phind Instant API, sets the necessary headers,
    and constructs the payload with the user's prompt. It then sends a POST request to the API
    endpoint and streams the response. The function collects the text content from the streamed
    response and returns it as a single string.
    """

    headers = {"User-Agent": ""}
    # Insert the system prompt at the beginning of the conversation history
    prompt.insert(0, {"content": system_prompt, "role": "system"})
    payload = {
        "additional_extension_context": "",
        "allow_magic_buttons": True,
        "is_vscode_extension": True,
        "message_history": prompt,
        "requested_model": model,
        "user_input": prompt[-1]["content"],
    }

    # Send POST request and stream response
    chat_endpoint = "https://https.extension.phind.com/agent/"
    response = requests.post(chat_endpoint, headers=headers, json=payload, stream=True)

    # Collect streamed text content
    streaming_text = ""
    for value in response.iter_lines(decode_unicode=True, chunk_size=stream_chunk_size):
        modified_value = re.sub("data:", "", value)
        if modified_value:
            json_modified_value = json.loads(modified_value)
            try:
                if stream: print(json_modified_value["choices"][0]["delta"]["content"], end="")
                streaming_text += json_modified_value["choices"][0]["delta"]["content"]
            except: continue

    return streaming_text


if __name__ == "__main__":
    # Predefined system prompt
    system_prompt = "Be Helpful and Friendly. Keep your response straightforward, short and concise"
    # system_prompt = "Be Helpful and Friendly. Keep your response straightforward, long and detailed"
    # system_prompt = "Talk like Shakespeare"

    # Predefined conversational history that includes providing a name and then asking the AI to recall it
    prompt = [
        {"role": "user", "content": "My name is Sreejan."},
        {"role": "assistant", "content": "Nice to meet you, Sreejan."},
        {"role": "user", "content": "What is my name?"}
    ]

    # Call the generate function with the predefined conversational history
    api_response = generate(prompt=prompt, system_prompt=system_prompt, model="Phind-34B", stream=True)
    # print("Response content:", api_response) 




"**************************************************************************"

"""DEPRECATED: This API is no longer Used. Please use the 'Latest' API instead."""

"**************************************************************************"


# import requests
# import re
# import json

# def generate(prompt: str, system_prompt: str = "Be Helpful and Friendly", model: str = "Phind Instant", stream_chunk_size: int = 12, stream: bool = True) -> str:
#     """
#     Generates a response from the Phind Instant model based on the given prompt.

#     Parameters:
#     - prompt (str): The input text to which the model will respond.
#     - system_prompt (str, optional): The system prompt to use for the model. Defaults to "Be Helpful and Friendly".    
#     - model (str, optional): The model to use for generating the response. 
#                                         Available Models: 
#                                             - "Phind-34B"
#                                             - "Phind Instant"
#     - stream_chunk_size (int, optional): The number of bytes to read from the response stream. Defaults to 64.
#     - stream (bool, optional): Whether to stream the response. Defaults to True.
                                            
#     Returns:
#     - str: The generated text response from the model.

#     This function initializes a session with the Phind Instant API, sets the necessary headers,
#     and constructs the payload with the user's prompt. It then sends a POST request to the API
#     endpoint and streams the response. The function collects the text content from the streamed
#     response and returns it as a single string.
#     """

#     headers = {"User-Agent": ""}
#     payload = {
#         "additional_extension_context": "",
#         "allow_magic_buttons": True,
#         "is_vscode_extension": True,
#         "message_history": [
#             {"content": system_prompt, "role": "system"},
#             {"content": prompt, "role": "user"}],
#         "requested_model": model,
#         "user_input": prompt,
#     }

#     # Send POST request and stream response
#     chat_endpoint = "https://https.extension.phind.com/agent/"
#     response = requests.post(chat_endpoint, headers=headers, json=payload, stream=True)

#     # Collect streamed text content
#     streaming_text = ""
#     for value in response.iter_lines(decode_unicode=True, chunk_size=stream_chunk_size):
#         modified_value = re.sub("data:", "", value)
#         if modified_value:
#             json_modified_value = json.loads(modified_value)
#             try:
#                 if stream: print(json_modified_value["choices"][0]["delta"]["content"], end="")
#                 streaming_text += json_modified_value["choices"][0]["delta"]["content"]
#             except: continue

#     return streaming_text


# if __name__ == "__main__":
#     prompt = "Write 20 lines about India"
#     prompt = "When is IPL 2024 starting"
#     prompt = "क्या आप मुझे बता सकते हैं कि भारत में सबसे ऊँचा पर्वत कौन सा है?"
#     # system_prompt = "Talk Like Shakesphere"
#     api_response = generate(prompt, model="Phind-34B", stream=True)
#     # print("Response content:", api_response) 




