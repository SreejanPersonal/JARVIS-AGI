import requests
import json
import os
from dotenv import load_dotenv; load_dotenv() # Load environment variables from .env file


def generate(query: str, system_prompt: str = "keep your response short and concise" , model: str = "openchat/openchat-7b", max_tokens: int = 8096,  # For Simple Models
                                        temperature: float = 0.85, frequency_penalty: float = 0.34, presence_penalty: float = 0.06,
                                        repetition_penalty: float = 1.0, top_k: int = 0) -> str:
    """
    Sends a request to the OpenRouter API and returns the generated text using the specified model.

    Args:
        query (str): The input query or prompt.
        system_prompt (str, optional): A context or introduction to set the style or tone of the generated response.
                                       Defaults to "Talk Like Shakespeare".
        model (str, optional): The language model to use for generating the response.
                               Defaults to "openchat/openchat-7b".
        max_tokens (int, optional): The maximum number of tokens to generate in the response.
                                    Defaults to 8096.
        temperature (float, optional): A parameter controlling the diversity of the generated response.
                                        Higher values result in more diverse outputs. Defaults to 0.85.
        frequency_penalty (float, optional): A penalty applied to tokens with low frequency in the training data.
                                              Defaults to 0.34.
        presence_penalty (float, optional): A penalty applied to tokens based on their presence in the prompt.
                                             Defaults to 0.06.
        repetition_penalty (float, optional): A penalty applied to repeated tokens in the generated response.
                                               Defaults to 1.0.
        top_k (int, optional): The number of highest probability tokens to consider at each step of generation.
                                Defaults to 0, meaning no restriction.

    Returns:
        str: The generated text.

    Available models:
    - Free:
        - "openchat/openchat-7b"
        - "huggingfaceh4/zephyr-7b-beta"
        - "mistralai/mistral-7b-instruct:free"
    
    - Flagship Opensource:
        - "meta-llama/llama-3-8b-instruct:extended"
        - "lynn/soliloquy-l3"
        - "mistralai/mixtral-8x22b-instruct"
        - "meta-llama/llama-3-70b-instruct:nitro"

    - Premium:
        - "openai/gpt-4"
        - "openai/gpt-4-0314"
        - "anthropic/claude-3-opus"
        - "anthropic/claude-3-opus:beta"
        - "openai/gpt-4-turbo"
    """

    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {os.environ.get('OPENROUTER')}",
      },
      data=json.dumps({
          
        "messages": [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": query},
        ],
        
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "repetition_penalty": repetition_penalty,
        "top_k": top_k,

      }))

        

    try: return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e: return f"Failed to Get Response\nError: {e}\nResponse: {response.text}"


if __name__ == "__main__":
    response = generate("Introdue yourself and tell me your name and who made you", system_prompt="Talk Like Shakesphere")
    # response = generate("are you gpt 4 or not. do you have access to realtime data. if not then till which time you have data of")
    print(response)