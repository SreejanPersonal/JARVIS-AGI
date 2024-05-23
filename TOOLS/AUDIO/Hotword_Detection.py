import pvporcupine
import pyaudio
import struct
from playsound import playsound
from typing import List, Optional 

class HotwordDetector:
    """
    A class to detect hotwords using the Porcupine library.

    Attributes:
        keywords (List[str]): A list of keywords to detect.
        activation_sound_path (Optional[str]): The path to the activation sound file.
        deactivation_sound_path (Optional[str]): The path to the deactivation sound file.
        prints (bool): A flag to print debug messages.

    Methods:
        listen_for_hotwords (stop_event: Optional[threading.Event] = None) -> bool:
            Listens for hotwords and returns True if a hotword is detected, False otherwise.
        stop () -> None:
            Stops the hotword detection process.
    """
    def __init__(self, keywords: List[str] = ['picovoice', 'grasshopper', 'americano', 'hey siri', 'bumblebee', 'ok google', 'blueberry', 'jarvis', 'pico clock', 'terminator', 'computer', 'porcupine', 'grapefruit', 'hey google', 'alexa'], 
                 activation_sound_path: Optional[str] = r"ASSETS\SOUNDS\activation_sound.wav",
                 deactivation_sound_path: Optional[str] = None, # r"ASSETS\SOUNDS\deactivation_sound.wav",
                 prints: bool = False) -> None:
        self.keywords = keywords
        self.activation_sound_path = activation_sound_path
        self.deactivation_sound_path = deactivation_sound_path
        self.prints = prints

        self.porcupine = pvporcupine.create(keywords=self.keywords)
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
        )

        self._stop_requested = False

    def stop(self) -> None:
        """Stops the hotword detection process."""
        self._stop_requested = True
        if self.prints: print("Hotword detection has been stopped.")

    def listen_for_hotwords(self, stop_event: Optional[object] = None) -> bool:
        """
        Listens for hotwords and returns True if a hotword is detected, False otherwise.
        If an activation or deactivation sound path is provided, the corresponding sound will be played.
        :param stop_event: An optional threading.Event() to stop listening externally.
        :return: True if a hotword is detected, False otherwise.
        """
        try:
            if self.deactivation_sound_path:
                self._play_sound(self.deactivation_sound_path)
            if self.prints: print("Listening for hotwords...")
            while not self._stop_requested and (stop_event is None or not stop_event.is_set()):
                audio_data = self.audio_stream.read(self.porcupine.frame_length)
                audio_data = struct.unpack_from("h" * self.porcupine.frame_length, audio_data)
                keyword_index = self.porcupine.process(audio_data)
                if keyword_index >= 0:
                    detected_keyword = self.keywords[keyword_index]
                    if self.prints: print(f"Hotword detected: {detected_keyword}")
                    if self.activation_sound_path:
                        self._play_sound(self.activation_sound_path)
                    return True  # Return True if a hotword is detected

        finally:
            self._cleanup()

    def _play_sound(self, sound_path: Optional[str]) -> None:
        """Plays a sound file if a path is provided."""
        if sound_path: playsound(sound_path)
        if self.prints: print(f"Playing sound: {sound_path}")
            

    def _cleanup(self) -> None:
        """Releases resources."""
        if self.prints: print("Cleaning up resources...")
        if self.porcupine is not None:
            self.porcupine.delete()
        if self.audio_stream is not None:
            self.audio_stream.close()
        if self.audio_interface is not None:
            self.audio_interface.terminate()
        if self.prints: print("Resources have been cleaned up.")

if __name__ == "__main__":
    detector = HotwordDetector(prints=True)
    hotword_detected = detector.listen_for_hotwords()

    # Actions based on hotword detection
    if hotword_detected:
        print("Executing actions for detected hotword.........")
        # Insert actions to be executed when a hotword is detected






































# import pvporcupine
# import pyaudio
# import struct
# from playsound import playsound
# from typing import List, Optional

# class HotwordDetector:
#     def __init__(self, keywords: List[str] = ["jarvis", "alexa", "ok google"], 
#                  activation_sound_path: str = r"ASSETS\SOUNDS\activation_sound.wav",
#                  deactivation_sound_path: str = r"ASSETS\SOUNDS\deactivation_sound.wav",
#                  prints: bool = False) -> None:
#         self.keywords = keywords
#         self.activation_sound_path = activation_sound_path
#         self.deactivation_sound_path = deactivation_sound_path
#         self.prints = prints

#         self.porcupine = pvporcupine.create(keywords=self.keywords)
#         self.audio_interface = pyaudio.PyAudio()
#         self.audio_stream = self.audio_interface.open(
#             rate=self.porcupine.sample_rate,
#             channels=1,
#             format=pyaudio.paInt16,
#             input=True,
#             frames_per_buffer=self.porcupine.frame_length,
#         )

#         self._stop_requested = False

#     def stop(self) -> None:
#         """Stops the hotword detection process."""
#         self._stop_requested = True
#         if self.prints: print("Hotword detection has been stopped.")

#     def listen_for_hotwords(self, stop_event: Optional[object] = None) -> bool:
#         """
#         Listens for hotwords and returns True if a hotword is detected, False otherwise.
#         """
#         try:
#             self._play_sound(self.deactivation_sound_path)
#             if self.prints: print("Listening for hotwords...")
#             while not self._stop_requested and (stop_event is None or not stop_event.is_set()):
#                 audio_data = self.audio_stream.read(self.porcupine.frame_length)
#                 audio_data = struct.unpack_from("h" * self.porcupine.frame_length, audio_data)
#                 keyword_index = self.porcupine.process(audio_data)
#                 if keyword_index >= 0:
#                     detected_keyword = self.keywords[keyword_index]
#                     print(f"Hotword detected: {detected_keyword}")
#                     self._play_sound(self.activation_sound_path)
#                     return True  # Return True if a hotword is detected

#         finally:
#             self._cleanup()

#     def _play_sound(self, sound_path: str) -> None:
#         """Plays a sound file."""
#         if self.prints: print(f"Playing sound: {sound_path}")
#         playsound(sound_path)

#     def _cleanup(self) -> None:
#         """Releases resources."""
#         if self.prints: print("Cleaning up resources...")
#         if self.porcupine is not None:
#             self.porcupine.delete()
#         if self.audio_stream is not None:
#             self.audio_stream.close()
#         if self.audio_interface is not None:
#             self.audio_interface.terminate()
#         if self.prints: print("Resources have been cleaned up.")

# if __name__ == "__main__":
#     detector = HotwordDetector(prints=False)
#     hotword_detected = detector.listen_for_hotwords()

#     # Actions based on hotword detection
#     if hotword_detected:
#         print("Executing actions for detected hotword.........")
#         # Insert actions to be executed when a hotword is detected

