import requests
import os
from dotenv import load_dotenv; load_dotenv() # Load environment variables from .env file

def generate(prompt: str, model: str = "stability-ai/sdxl", negative_prompt: str = "", width: int = 512, height: int = 512, num_outputs: int = 4, prompt_strength: float = 0.8):
    """
    Initiates an API call to a deep infrastructure (DeepInfra) system, utilizing a language model to generate responses based on the provided prompt.

    Args:
        prompt (str): The input prompt or query to initiate the conversation.
        model (str, optional): The specific language model to use for response generation. Defaults to "stability-ai/sdxl".
                               Additional models may be specified based on availability within the DeepInfra system.
        negative_prompt (str, optional): An optional prompt to guide the generation of negative responses or counterarguments. Defaults to an empty string.
        width (int, optional): The desired width for generated images in pixels. Defaults to 512.
        height (int, optional): The desired height for generated images in pixels. Defaults to 512.
        num_outputs (int, optional): The number of output responses to generate. Defaults to 4.
        prompt_strength (float, optional): The strength of influence the prompt exerts on the generated response. Defaults to 0.8.

    Returns:
        list of str: A list of generated responses based on the provided prompt and settings.
    """

    url=f"https://api.deepinfra.com/v1/inference/{model}"
    headers = {
        "Authorization" : f"Bearer {os.environ.get('DEEPINFRA')}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }
    payload = {
        "input": {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "num_outputs": num_outputs,
            "prompt_strength": prompt_strength
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()['output']
        if data != None: return data
        else: return response.text

    except Exception as e: return f"ERROR --> {e}\n{response.text}"

if __name__ == "__main__":
    # Example usage:
    prompt = "A beautiful, young woman with long, curly brown hair and bright green eyes, wearing a flowing, emerald green dress with golden trim, standing in a lush, vibrant garden filled with blooming flowers and towering trees, surrounded by a warm, golden light, with a subtle smile on her face"
    result = generate(prompt)
    print(result)