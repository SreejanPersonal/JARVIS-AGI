from typing import Generator
import pyaudio
from vosk import Model, KaldiRecognizer
import ast

def speech_to_text(prints: bool = True, model_path: str = r"ASSETS\Vosk\vosk-model-small-en-us-0.15") -> Generator[str, None, None]:
    """
    Asynchronously transcribes continuous speech into text using the Vosk library and PyAudio.

    This function initializes a Vosk speech-to-text model and a PyAudio stream, and continuously listens to the
    user's speech using the microphone. It yields the transcribed text in lowercase as it becomes available.

    Args:
        prints (bool): If True, prints the transcription results.
        model_path (str): The path to the Vosk model file.

    Yields:
        str: The transcribed text in lowercase.

    Note:
        The function uses the Vosk library for speech recognition and the PyAudio library for audio input.
        Both libraries must be installed for this function to work properly.

    Example Usage:
        >>> for speech in speech_to_text():
        ...     print(speech)
    """
    # Initialize Vosk model
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    print("Model Initialized....")

    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(8192)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = ast.literal_eval(result)
            if 'text' in result_dict:
                if prints: print("\rTranscript: " + result_dict['text'])
                yield result_dict['text'].lower()
        else:
            if prints: print("\rSpeaking: " + recognizer.PartialResult().split('"')[-2], end='', flush=True)

if __name__ == "__main__":
    for speech in speech_to_text():
        if "stop" in speech:
            print("Speech: ", speech)  # The actual printing is handled within the function now
            print("Broken....")
            break