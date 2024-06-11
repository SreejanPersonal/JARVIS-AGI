import requests
import base64
import time

def encode_image_to_base64(image_path: str) -> str:
    """
    Encodes the image file to a Base64 string.

    Parameters:
    image_path (str): The path to the image file.

    Returns:
    str: The Base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def generate(user_message: str, image_path: str, system_prompt: str="Be a helpful assistant", model: str="llava-hf/llava-1.5-7b-hf") -> str:
    """
    Sends a POST request to the specified API with the given payload.

    Parameters:
    user_message (str): The user message for the API payload.
    image_path (str): The Base64 encoded image string.
    system_prompt (str): The system message for the API payload.
    model (str): The model identifier for the API.

    Returns:
    dict: The JSON response from the API.
    """
    api_url = "https://api.deepinfra.com/v1/openai/chat/completions"
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

    image_base64 = encode_image_to_base64(image_path)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64, {image_base64}"}},
                {"type": "text", "text": user_message}
            ]}
        ],
        "stream": False
    }
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']


if __name__ == "__main__":
    start_time = time.time()
    user_message = "Describe the image"
    api_response = generate(user_message, image_path=r"C:\Users\sreej\Downloads\Reverse.png")
    print("Response content:", api_response)
    print("Time taken:", time.time() - start_time)




"*******************************************************"

"""Deprecated. Not Working with Auth. Use The Latest Code"""

"*******************************************************"

# import requests
# import base64
# import time
# import os
# from dotenv import load_dotenv
# load_dotenv()

# def encode_image_to_base64(image_path: str) -> str:
#     """
#     Encodes the image file to a Base64 string.

#     Parameters:
#     image_path (str): The path to the image file.

#     Returns:
#     str: The Base64 encoded string of the image.
#     """
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# def generate(user_message: str, image_path: str, system_prompt: str="Be a helpful assistant", model: str="llava-hf/llava-1.5-7b-hf") -> str:
#     """
#     Sends a POST request to the specified API with the given payload.

#     Parameters:
#     user_message (str): The user message for the API payload.
#     image_path (str): The Base64 encoded image string.
#     system_prompt (str): The system message for the API payload.
#     model (str): The model identifier for the API.

#     Returns:
#     dict: The JSON response from the API.
#     """
#     api_url = "https://api.deepinfra.com/v1/openai/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {os.environ.get('DEEPINFRA')}",
#     }
#     image_base64 = encode_image_to_base64(image_path)
#     payload = {
#         "model": model,
#         "messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": [
#                 {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64, {image_base64}"}},
#                 {"type": "text", "text": user_message}
#             ]}
#         ],
#         "stream": False
#     }
#     response = requests.post(api_url, headers=headers, json=payload)
#     return response.json()['choices'][0]['message']['content']


# if __name__ == "__main__":
#     start_time = time.time()
#     user_message = "Describe the image"
#     api_response = generate(user_message, image_path=r"C:\Users\sreej\Downloads\Reverse.png")
#     print("Response content:", api_response)
#     print("Time taken:", time.time() - start_time)
