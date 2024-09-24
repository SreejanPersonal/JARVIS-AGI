import requests
import base64
# from TOOLS.AUDIO import Interrupted_Playsound
from playsound import playsound
import os

def speak(text: str, model: str = "aura-arcas-en", filename: str = "ASSETS/output_audio.mp3"):
    """
    Converts text to speech using the Deepgram API and plays the audio.

    Parameters:
        text (str): The text to convert to speech.
        model (str): The voice model to use for speech generation.
                            - aura-asteria-en
                            - aura-arcas-en
                            - aura-luna-en
                            - aura-zeus-en
        filename (str): The temporary file to save the audio output.
    """

    try: os.remove(filename)
    except: pass
    
    url = "https://deepgram.com/api/ttsAudioGeneration"

    headers = {
    "authority": "deepgram.com",
    "method": "POST",
    "path": "/api/ttsAudioGeneration",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,hi;q=0.8",
    "content-type": "application/json",
    "origin": "https://deepgram.com",
    "priority": "u=1, i",
    "referer": "https://deepgram.com/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "dnt": "1"
}
    payload = {"text": text, "model": model}
       

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Ensure the request was successful

    with open(filename, 'wb') as audio_file:
        audio_file.write(base64.b64decode(response.json()['data']))
    
    # Interrupted_Playsound.play_audio(filename)
    playsound(filename)
    os.remove(filename)

if __name__ == "__main__":
    speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this")
