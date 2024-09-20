import requests
import base64
from playsound import playsound
import os
import threading
import queue
import time

class SpeechSynthesizer:
    """
    Provides text-to-speech functionality using the Deepgram API, with support for asynchronous 
    speech synthesis and queued audio playback to ensure a seamless user experience. 
    """

    def __init__(self):
        """
        Initializes the SpeechSynthesizer with a dedicated audio queue and a background thread 
        for managing audio playback.
        """
        self.audio_queue = queue.Queue()
        threading.Thread(target=self._audio_playback_handler, args=(self.audio_queue,), daemon=True).start()

    def generate_speech(self, text: str, voice_model: str = "aura-arcas-en", output_filename: str = "ASSETS/STREAM_AUDIOS/output_audio.mp3"):
        """
        Sends a text string to the Deepgram API for speech synthesis and saves the resulting audio to a file.

        Args:
            text (str): The text content to be converted into speech.
            voice_model (str, optional): The identifier of the desired Deepgram voice model to use for synthesis. 
                                          Defaults to "aura-arcas-en".
            output_filename (str, optional): The path to the file where the synthesized audio will be saved. 
                                             Defaults to "ASSETS/STREAM_AUDIOS/output_audio.mp3".
        """
        api_endpoint = "https://deepgram.com/api/ttsAudioGeneration"
        request_payload = {"text": text, "model": voice_model}
        api_response = requests.post(api_endpoint, json=request_payload)
        api_response.raise_for_status()  # Raise an exception for unsuccessful API requests

        # Create the directory if it doesn't exist
        if not os.path.exists("ASSETS/STREAM_AUDIOS"):
            os.makedirs("ASSETS/STREAM_AUDIOS")

        with open(output_filename, 'wb') as audio_file:
            audio_file.write(base64.b64decode(api_response.json()['data']))

    def speak(self, text: str, voice_model: str = "aura-arcas-en", output_filename: str = "ASSETS/STREAM_AUDIOS/output_audio.mp3"):
        """
        Initiates asynchronous text-to-speech conversion using a separate thread, allowing other processes 
        to continue without blocking.

        Args:
            text (str): The text to convert to speech.
            voice_model (str, optional): The Deepgram voice model for speech generation. 
                                          Defaults to "aura-arcas-en".
            output_filename (str, optional): The temporary file to store the generated audio. 
                                             Defaults to "ASSETS/STREAM_AUDIOS/output_audio.mp3".

        Returns:
            threading.Thread:  The thread handling the asynchronous speech generation.
        """
        thread = threading.Thread(target=self.generate_speech, args=(text, voice_model, output_filename))
        thread.start()
        return thread

    def _audio_playback_handler(self, audio_queue: queue.Queue):
        """
        Continuously monitors the audio queue for new files and plays them back sequentially.

        Args:
            audio_queue (queue.Queue): The queue containing filenames of audio files to be played.
        """
        while True:
            filename = audio_queue.get()
            if filename is None:  # Sentinel value to signal thread termination
                break
            # Wait for the audio file to become available 
            while not os.path.exists(filename):
                time.sleep(0.1) 
            playsound(filename)
            os.remove(filename)  # Remove temporary audio file after playback
            audio_queue.task_done()

    def queue_audio(self, filename: str):
        """
        Adds an audio file to the playback queue.

        Args:
            filename (str): The path to the audio file to be queued for playback. 
        """
        self.audio_queue.put(filename)
    
    def wait_for_playback_completion(self):
        """
        Blocks the calling thread until all queued audio files have been played back.
        """
        self.audio_queue.join()

if __name__ == "__main__":
    audio_queue = queue.Queue()
    speech_synthesizer = SpeechSynthesizer()
    threading.Thread(target=speech_synthesizer._audio_playback_handler, args=(audio_queue,), daemon=True).start()

    speech_synthesizer.speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this")