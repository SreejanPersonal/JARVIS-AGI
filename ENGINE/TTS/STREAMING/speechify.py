import requests
import base64
import os
import threading
import queue
import time
from playsound import playsound

class SpeechSynthesizer:
    """
    Provides text-to-speech functionality using the Speechify API, with support for asynchronous 
    speech synthesis and queued audio playback to ensure a seamless user experience. 
    """

    def __init__(self):
        """
        Initializes the SpeechSynthesizer with a dedicated audio queue and a background thread 
        for managing audio playback.
        """
        self.audio_queue = queue.Queue()
        self.playback_thread = threading.Thread(target=self._audio_playback_handler, args=(self.audio_queue,), daemon=True)
        self.playback_thread.start()

    def generate_speech(self, paragraph: str, voice_name: str = "mrbeast", output_filename: str = "ASSETS/output_audio.mp3"):
        """
        Sends a text string to the Speechify API for speech synthesis and saves the resulting audio to a file.

        Args:
            paragraph (str): The text content to be converted into speech.
            voice_name (str, optional): The identifier of the desired Speechify voice model to use for synthesis. 
                                        Defaults to "mrbeast".
            output_filename (str, optional): The path to the file where the synthesized audio will be saved. 
                                             Defaults to "ASSETS/output_audio.mp3".
        """
        try: 
            os.remove(output_filename)
        except: 
            pass
        
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
        with open(output_filename, 'wb') as audio_file:
            audio_file.write(audio_data)

    def speak(self, paragraph: str, voice_name: str = "mrbeast", output_filename: str = "ASSETS/output_audio.mp3"):
        """
        Initiates asynchronous text-to-speech conversion using a separate thread, allowing other processes 
        to continue without blocking.

        Args:
            paragraph (str): The text to convert to speech.
            voice_name (str, optional): The Speechify voice model for speech generation. 
                                        Defaults to "mrbeast".
            output_filename (str, optional): The temporary file to store the generated audio. 
                                             Defaults to "ASSETS/output_audio.mp3".

        Returns:
            threading.Thread:  The thread handling the asynchronous speech generation.
        """
        thread = threading.Thread(target=self._async_speech, args=(paragraph, voice_name, output_filename))
        thread.start()
        return thread

    def _async_speech(self, paragraph: str, voice_name: str, output_filename: str):
        """
        Generates speech and queues the audio file for playback.

        Args:
            paragraph (str): The text to convert to speech.
            voice_name (str): The Speechify voice model for speech generation.
            output_filename (str): The temporary file to store the generated audio.
        """
        try:
            self.generate_speech(paragraph, voice_name, output_filename)
            self.queue_audio(output_filename)
        except Exception as e:
            print(f"Error generating or queuing speech: {e}")

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
            try:
                playsound(filename)
                os.remove(filename)  # Remove temporary audio file after playback
            except Exception as e:
                print(f"Error playing or removing file: {e}")
            finally:
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
    speech_synthesizer = SpeechSynthesizer()
    
    # Example usage
    speech_thread = speech_synthesizer.speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this.", voice_name='jamie')
    
    # Wait for all audio to be played back before exiting
    speech_synthesizer.wait_for_playback_completion()