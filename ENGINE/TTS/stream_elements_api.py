import requests
import playsound
import os
from typing import Union

def generate_audio(message: str, voice: str = "Brian"):
    """
    Text to speech using StreamElements API

    Parameters:
        message (str): The text to convert to speech
        voice (str): The voice to use for speech synthesis. Default is "Brian".

    Returns:
        result (Union[str, None]): Temporary file path or None in failure
    """
    # Base URL for provider API
    url: str = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={{{message}}}"
    
    # Request headers
    headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

    # Try to send request or return None on failure
    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except:
        return None
    
def speak(message: str, voice: str = "Brian", folder: str = "", extension: str = ".mp3") -> Union[None, str]:
    """
    Save the result content to a file and play it using the playsound module.

    Args:
        result_content (bytes): The content to be saved and played.
        folder (str): The folder to save the file in. Default is "Voice Audio/".
        extension (str): The extension of the file. Default is ".mp3".

    Returns:
        None, String
    """
    try:
        result_content = generate_audio(message, voice)
        file_path = os.path.join(folder, f"{voice}{extension}")
        with open(file_path, "wb") as file:
            file.write(result_content)
        playsound.playsound(file_path, "wb")
        os.remove(file_path)
        return None
    except Exception as e:
        return "Error playing TTS: " + str(e)
    

if __name__ == "__main__": 
    speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this", voice="Salli")