import os
import time
from collections import deque
from typing import Any

import numpy as np
import sounddevice as sd
import torch
from scipy.io.wavfile import write

try: from PLAYGROUND.CLAP_NN.audio_inference import AudioModelHandler
except ModuleNotFoundError: from audio_inference import AudioModelHandler
except: raise Exception("Error importing audio_inference.py")


class AudioProcessor:
    """
    Class for processing and detecting claps in audio input.
    """
    def __init__(self, device_index: int, model_path: str, 
                 chunk_duration: float = 0.5,  # in seconds
                 buffer_duration: float = 10,  # in seconds
                 sample_rate: int = 44100,  # in Hz
                 dtype: Any = np.int16,
                 directory: str = "./"):
        """
        Initializes the AudioProcessor.

        Args:
            device_index (int): Index of the input device to use.
            model_path (str): Path to the saved model file.
            chunk_duration (float, optional): Duration of each audio chunk. Defaults to 0.1 seconds.
            buffer_duration (float, optional): Duration of the audio buffer. Defaults to 10 seconds.
            sample_rate (int, optional): Sampling rate of the audio. Defaults to 44100 Hz.
            dtype (Any, optional): Data type of the audio samples. Defaults to np.int16.
            directory (str, optional): Directory to save temporary audio files. Defaults to "./".
        """
        self.chunk_duration = chunk_duration
        self.buffer_duration = buffer_duration
        self.sample_rate = sample_rate
        self.dtype = dtype
        self.directory = directory
        
        self.chunk_samples = int(chunk_duration * sample_rate)
        self.buffer_samples = int(buffer_duration * sample_rate)
        
        self.model_handler = AudioModelHandler(model_path)
        self.buffer = deque(maxlen=self.buffer_samples)
        self.stream = sd.InputStream(device=device_index, channels=1, samplerate=sample_rate, dtype=dtype)
    
    def save_buffer_to_wav(self, filename: str) -> None:
        """
        Saves the current buffer to a WAV file.

        Args:
            filename (str): Path to save the WAV file.
        """
        write(filename, self.sample_rate, np.array(self.buffer))
    
    def record_and_detect(self) -> None:
        """
        Records audio input and detects claps.
        """
        with self.stream:
            print("Recording...")
            while True:
                chunk, overflowed = self.stream.read(self.chunk_samples)
                self.buffer.extend(chunk)
                
                temp_filename = os.path.join(self.directory, "ASSETS/temp.wav")
                self.save_buffer_to_wav(temp_filename)
                
                prediction = self.model_handler.predict(temp_filename)
                probabilities = torch.softmax(self.model_handler.model(self.model_handler.transform_audio(temp_filename)), dim=1)
                predicted_prob = probabilities[0][prediction].item()

                if predicted_prob > 0.99 and prediction == 1:
                    print(f"👏 {predicted_prob * 100:.2f}%")
                    break
                else:
                    print("-")

                time.sleep(self.chunk_duration)
            print("Recording finished.")

def list_devices() -> None:
    """
    Lists available audio input devices.
    """
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']}")

def detect_claps(device_index: int, chunk_duration: float = 0.5) -> None:
    """
    Detects claps using audio input from the specified device.

    Args:
        device_index (int): Index of the input device to use.
    """
    
    model_path = r"ASSETS\CLAP_DETECTS\MODELS\Clap_Detect_Model.pth"
    
    audio_processor = AudioProcessor(
        device_index=device_index,
        model_path=model_path,
        chunk_duration=chunk_duration,
    )
    audio_processor.record_and_detect()

if __name__ == "__main__":

    # Example Usage
    list_devices()
    device_index = int(input("Enter the index of the device you want to use: "))
    detect_claps(device_index)

    # Loop Runner
    while True:
        detect_claps(device_index)
