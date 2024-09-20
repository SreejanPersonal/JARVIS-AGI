import requests
import base64
import os
from TOOLS.AUDIO import Interrupted_Playsound

def speak(paragraph: str, voice_name: str = "mrbeast", filename: str = "ASSETS/output_audio.mp3"):
    """
    Converts text to speech using the Speechify API and plays the audio.

    Parameters:
        paragraph (str): The text to convert to speech.
        voice_name (str): The voice model to use for speech generation.
                                    Available voices:
                                        - jamie
                                        - mrbeast
                                        - snoop
                                        - henry
                                        - gwyneth
                                        - cliff
                                        -narrator

        filename (str): The temporary file to save the audio output.
    """
    try: os.remove(filename)
    except: pass
    
    url = "https://audio.api.speechify.com/generateAudioFiles"
    payload = {
        "audioFormat": "mp3",
        "paragraphChunks": [paragraph],
        "voiceParams": {
            "name": voice_name,
            "engine": "speechify",
            "languageCode": "en-US"
        }
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    audio_data = base64.b64decode(response.json()['audioStream'])
    with open(filename, 'wb') as audio_file:
        audio_file.write(audio_data)
    
    # playsound.playsound(filename)
    Interrupted_Playsound.play_audio(filename)
    os.remove(filename)

if __name__ == "__main__":
    # speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this.", voice_name='jamie')
    # speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this.", voice_name='henry')
    # speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this.", voice_name='snoop')
    # speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this.", voice_name='gwyneth')
    # speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this.", voice_name='cliff')


    # speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this.", voice_name='narrator')
    speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this.")
