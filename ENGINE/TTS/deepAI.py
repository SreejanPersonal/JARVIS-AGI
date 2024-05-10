import requests
import playsound
import os

def speak(text: str, model: str="aura-athena-en", filename: str="ASSETS/output.mp3"):
    """
    Sends a POST request to the DeepAI Speech API to generate speech response from text.

    Parameters:
        text (str): The text for which speech response is to be generated.
        model (str): The model to be used for generating speech response.
            Available models:
                - "aura-asteria-en": Sophia (Female US English)
                - "aura-luna-en": Emily (Female US English)
                - "aura-stella-en": Rachel (Female US English) - Good for conversation
                - "aura-athena-en": Eliza (Female UK English) - Good for conversation
                - "aura-hera-en": Pam (Female US English) - Good for conversation
                - "aura-orion-en": Kevin (Male US English)
                - "aura-arcas-en": Jeff (Male US English)
                - "aura-perseus-en": Alex (Male US English)
                - "aura-angus-en": Rory (Male Irish English)
                - "aura-orpheus-en": John (Male US English)
                - "aura-helios-en": Pete (Male UK English)
                - "aura-zeus-en": James (Male US English)

    Returns:
        requests.Response: The HTTP response object containing the speech response.
    """
    # Define the API endpoint URL
    url = "https://api.deepai.org/speech_response"

    # Define the payload
    payload = {
        "model": model,
        "text": text
    }

    # Send the POST request
    response = requests.post(url, json=payload)
    if response.status_code != 200: return f"Error: {response.status_code} - {response.text}"
    else:
        with open(filename, 'wb') as f:
            f.write(response.content)
        playsound.playsound(filename)
        os.remove(filename)

if __name__ == "__main__":

    speak("hello, this is my sample voice. i hope so you like it")

    available_models = {
    "Sophia (Female US English)": "aura-asteria-en",
    "Emily (Female US English)": "aura-luna-en",
    "Rachel (Female US English)": "aura-stella-en",
    "Eliza (Female UK English)": "aura-athena-en",
    "Pam (Female US English)": "aura-hera-en",
    "Kevin (Male US English)": "aura-orion-en",
    "Jeff (Male US English)": "aura-arcas-en",
    "Alex (Male US English)": "aura-perseus-en",
    "Rory (Male Irish English)": "aura-angus-en",
    "John (Male US English)": "aura-orpheus-en",
    "Pete (Male UK English)": "aura-helios-en",
    "James (Male US English)": "aura-zeus-en"
}
    # for model_name, model_key in available_models.items():
    #     print(f"Model Name: {model_name}, Model Key: {model_key}")
    #     response = speak("This is my sample voice", model_key)