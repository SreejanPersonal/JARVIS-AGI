import json
import requests
from typing import Union
import os
from dotenv import load_dotenv; load_dotenv() # Load environment variables from .env file

def generate(message: str, model: str='meta-llama/Meta-Llama-3-70B-Instruct', system_prompt: str = "Be Helpful and Friendly. Keep your response straightfoward, short and concise", max_tokens: int = 512, temperature: float = 0.7) -> Union[str, None]:
    """
    Utilizes a variety of large language models (LLMs) to engage in conversational interactions.
    
    Parameters:
        - model (str): The name or identifier of the LLM to be used for conversation. Available models include:
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
        - message (str): The message to be sent to the LLM to initiate or continue the conversation.
        - system_prompt (str): Optional. The initial system message to start the conversation. Defaults to "Talk Like Shakespeare".

    Returns:
        - Union[str, None]: The response message from the LLM if successful, otherwise None.
    """
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers ={
        "Authorization" : f"Bearer {os.environ.get('DEEPINFRA')}"
    }
    data = json.dumps(
        {
            'model': model,
            'messages': [{"role": "system", "content": system_prompt}] + [{"role": "user", "content": message}] ,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'stop': [],
            'stream': False
        }, separators=(',', ':')
    )
    
    try:
        result = requests.post(url=url, headers=headers, data=data)
        return result.json()['choices'][0]['message']['content']
    except Exception as e:
        print("Error:", e)
        return "Response content: " + result.text

if __name__ == "__main__":

    model_names = [
        "meta-llama/Meta-Llama-3-70B-Instruct",
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "mistralai/Mixtral-8x22B-Instruct-v0.1",
        "mistralai/Mixtral-8x22B-v0.1",
        "microsoft/WizardLM-2-8x22B",
        "microsoft/WizardLM-2-7B",
        "HuggingFaceH4/zephyr-orpo-141b-A35b-v0.1",
        "google/gemma-1.1-7b-it",
        "databricks/dbrx-instruct",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "mistralai/Mistral-7B-Instruct-v0.2",
        "meta-llama/Llama-2-70b-chat-hf",
        "cognitivecomputations/dolphin-2.6-mixtral-8x7b"
    ]

    for name in model_names:
        messages =  "Introduce yourself and tell who made you and about your owner company" # Add more messages as needed
        response = generate(messages, model=name, system_prompt="Respond very concisely and shortly")

        print(f"• Model: {name} -", response)