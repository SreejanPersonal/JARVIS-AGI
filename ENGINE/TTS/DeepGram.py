import requests
import base64
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
    payload = {"text": text, "model": model}
       

    response = requests.post(url, json=payload)
    response.raise_for_status()  # Ensure the request was successful

    with open(filename, 'wb') as audio_file:
        audio_file.write(base64.b64decode(response.json()['data']))
    
    playsound(filename)
    os.remove(filename)

if __name__ == "__main__":
    speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this")
