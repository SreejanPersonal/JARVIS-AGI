import requests
import base64
from playsound import playsound
import re
import threading
import queue
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from TOOLS.AUDIO.Interrupted_Playsound import play_audio

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

# if __name__ == "__main__":
#     audio_queue = queue.Queue()
#     speech_synthesizer = SpeechSynthesizer()
#     threading.Thread(target=speech_synthesizer._audio_playback_handler, args=(audio_queue,), daemon=True).start()

#     speech_synthesizer.speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this")






def speak(text: str, voice_name: str = "Arcas", output_file: str = "ASSETS/STREAM_AUDIOS/output_audio.mp3", verbose: bool = True):
    """
    ## Best Jarvis Voices: 
        - Arcas, Zeus
    """
    available_voices = {
        "Asteria": "aura-asteria-en", "Arcas": "aura-arcas-en", "Luna": "aura-luna-en",
        "Zeus": "aura-zeus-en", "Orpheus": "aura-orpheus-en", "Angus": "aura-angus-en",
        "Athena": "aura-athena-en", "Helios": "aura-helios-en", "Hera": "aura-hera-en",
        "Orion": "aura-orion-en", "Perseus": "aura-perseus-en", "Stella": "aura-stella-en"
    }
    if voice_name not in available_voices:
        raise ValueError(f"Invalid voice name. Available voices are: {list(available_voices.keys())}")
    
    url = "https://deepgram.com/api/ttsAudioGeneration"
    headers = {
        "accept": "*/*", "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,hi;q=0.8", "content-type": "application/json",
        "origin": "https://deepgram.com", "priority": "u=1, i", "referer": "https://deepgram.com/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "dnt": "1"
    }

    # Split text into sentences
    sentences = re.split(r'(?<!\b\w\.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    # Function to request audio for each chunk
    def generate_audio_for_chunk(part_text: str, part_number: int):
        while True:
            try:
                payload = {"text": part_text, "model": available_voices[voice_name]}
                response = requests.post(url, headers=headers, json=payload, timeout=None)
                response.raise_for_status()
                response_data = response.json().get('data')
                if response_data:
                    audio_data = base64.b64decode(response_data)
                    if verbose:
                        print(f"Chunk {part_number} processed successfully.")
                    return part_number, audio_data
                else:
                    if verbose:
                        print(f"No data received for chunk {part_number}. Retrying...")
            except requests.RequestException as e:
                # if verbose:
                #     print(f"Error for chunk {part_number}: {e}. Retrying...")
                time.sleep(1)

    # Using ThreadPoolExecutor to handle requests concurrently
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(generate_audio_for_chunk, sentence.strip(), chunk_num): chunk_num 
                   for chunk_num, sentence in enumerate(sentences, start=1)}
        
        # Dictionary to store results with order preserved
        audio_chunks = {}

        for future in as_completed(futures):
            chunk_num = futures[future]
            try:
                part_number, audio_data = future.result()
                audio_chunks[part_number] = audio_data  # Store the audio data in correct sequence
            except Exception as e:
                if verbose:
                    print(f"Failed to generate audio for chunk {chunk_num}: {e}")

    # Combine audio chunks in the correct sequence
    combined_audio = BytesIO()
    for part_number in sorted(audio_chunks.keys()):
        combined_audio.write(audio_chunks[part_number])
        if verbose:
            print(f"Added chunk {part_number} to the combined file.")

    # Save the combined audio data to a single file
    with open(output_file, 'wb') as f:
        f.write(combined_audio.getvalue())
    print(f"\033[1;93mFinal Audio Saved as {output_file}.\033[0m")

    # playsound(output_file)

    play_audio(output_file)
    os.remove(output_file)

if __name__=="__main__":
    speak("A notification is a message or alert that informs someone about an event, status, or requirement, often to prompt action or attention. It can originate from various sources such as software applications, digital devices, or services. Notifications can be delivered through different channels like emails, push notifications, or pop-up messages on devices. They play a vital role in user experience by keeping users informed without the need for manual inquiry.")