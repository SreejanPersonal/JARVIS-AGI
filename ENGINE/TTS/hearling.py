import requests
import asyncio
import aiohttp
import aiofiles
import os
import random
import urllib.request
from TOOLS.AUDIO import Interrupted_Playsound
import concurrent.futures

class Async_HearlingAudioGenerator:
    """
    A class to generate and play audio using the Hearling API.

    This class handles account creation, audio generation, and playback.
    It provides an easy-to-use interface for converting text to speech.
    """

    def __init__(self, email_prefix="devsdocode"):
        """
        Initializes the HearlingAudioGenerator with an email prefix.

        Creates a requests session for faster requests. 

        Args:
            email_prefix (str): The prefix for generating random email addresses for account creation.
        """
        self.email_prefix = email_prefix
        self.url_accounts = "https://api.hearling.com/accounts"
        self.url_clips = "https://api.hearling.com/clips"
        self.session = requests.Session()  # Create a session for faster requests
        self.token = self.create_account()

    def create_account(self):
        """
        Creates a new account on the Hearling API.

        Generates a random email address using the email prefix and registers a new account with Hearling.

        Returns:
            str: The authentication token for the newly created account.
        """
        email = f"{self.email_prefix}{random.randint(1, 99999)}@gmail.com"
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"}
        payload = {"email": email, "password": "DevsDoCode"}
        response = self.session.post(self.url_accounts, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['token']

    async def download_audio(self, audio_url, filename):
        """
        Downloads audio from the given URL and saves it to a file asynchronously.

        Uses aiohttp to download the audio content and aiofiles to save it to the specified file.

        Args:
            audio_url (str): The URL of the audio file to download.
            filename (str): The name of the file to save the audio to.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(audio_url) as response:
                response.raise_for_status()
                f = await aiofiles.open(filename, mode='wb')
                await f.write(await response.read())
                await f.close()

    async def _generate_and_play_audio(self, text: str, voice: str, filename: str = "audio_file.mp3", prints: bool = False):
        """
        Generates and plays audio from text using the Hearling API.

        Sends a request to the Hearling API to generate speech from the given text and voice model.
        Downloads the generated audio file and plays it using Interrupted_Playsound.play_audio.

        Args:
            text (str): The text to convert to speech.
            voice (str): The voice model to use for speech generation.
            filename (str): The temporary file to save the audio output.
            prints (bool): Whether to print debugging information, such as the audio URL.
        """
        headers = {"Authorization": f"Bearer {self.token}", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"}
        payload = {"text": text, "voice": voice}
        response = self.session.post(self.url_clips, headers=headers, json=payload)
        response.raise_for_status()

        audio_url = response.json()['clip']['location']
        if prints: print(f"Audio URL: {audio_url}")

        await self.download_audio(audio_url, filename)

        # Interrupted_Playsound.play_audio(filename)
        os.remove(filename)

    def speak(self, text: str, voice: str = "hi-IN-Wavenet-A", filename: str = "audio_file.mp3", prints: bool = False):
        """
        Generates and plays audio from text using the Hearling API.
        This function handles the asyncio execution and account creation after playback.

        Args:
            text (str): The text to convert to speech.
            voice (str): The voice model to use for speech generation.
            filename (str): The temporary file to save the audio output.
            prints (bool): Whether to print debugging information, such as the audio URL.
        """
        asyncio.run(self._generate_and_play_audio(text, voice, filename, prints))
        self.token = self.create_account()  # Update token after audio playback





"************************************************************"

"""Deprecated Code - No Asyncio which make the response slower"""

"************************************************************"





class HearlingAudioGenerator:
    """
    A class to generate and play audio using the Hearling API.

    This class handles account creation, audio generation, and playback.
    It provides an easy-to-use interface for converting text to speech.
    """

    def __init__(self, email_prefix="devsdocode"):
        """
        Initializes the HearlingAudioGenerator with an email prefix.

        Creates a requests session for faster requests and prepares for account creation.

        Args:
            email_prefix (str): The prefix for generating random email addresses for account creation.
        """
        self.email_prefix = email_prefix
        self.url_accounts = "https://api.hearling.com/accounts"
        self.url_clips = "https://api.hearling.com/clips"
        self.session = requests.Session()  # Create a session for faster requests
        self.token = self.create_account()  # Create an account upon initialization

    def create_account(self):
        """
        Creates a new account on the Hearling API.

        Generates a random email address using the email prefix and registers a new account with Hearling.

        Returns:
            str: The authentication token for the newly created account.
        """
        email = f"{self.email_prefix}{random.randint(10000, 99999)}@gmail.com"
        payload = {"email": email, "password": "DevsDoCode"}
        response = self.session.post(self.url_accounts, json=payload)
        response.raise_for_status()
        return response.json()['token']

    def speak(self, text: str, voice: str = "hi-IN-Wavenet-D", filename: str = "audio_file.mp3", prints: bool = False):
        """
        Generates and plays audio from text using the Hearling API.

        Creates a new Hearling account, sends a request to generate speech from the given text and voice model,
        downloads the generated audio file, plays it using Interrupted_Playsound.play_audio, and then deletes the temporary audio file.

        Args:
            text (str): The text to convert to speech.
            voice (str): The voice model to use for speech generation.
            filename (str): The temporary file to save the audio output.
        """
        headers = {"Authorization": f"Bearer {self.token}"}

        payload = {"text": text, "voice": voice}
        response = self.session.post(self.url_clips, headers=headers, json=payload)
        response.raise_for_status()

        audio_url = response.json()['clip']['location']
        urllib.request.urlretrieve(audio_url, filename)
        if prints: print(f"Audio URL: {audio_url}")

        # Interrupted_Playsound.play_audio(filename)
        os.remove(filename)
        self.token = self.create_account()  # Create a new account after audio playback





"************************************************************"

"""Deprecated Code - No Asyncio which make the response slower"""

"************************************************************"




class Partial_Async_HearlingAudioGenerator:
    """
    A class to generate and play audio using the Hearling API.

    This class handles account creation, audio generation, and playback.
    It provides an easy-to-use interface for converting text to speech.
    """

    def __init__(self, email_prefix="devsdocode"):
        """
        Initializes the HearlingAudioGenerator with an email prefix.

        Creates a requests session for faster requests and prepares for account creation.

        Args:
            email_prefix (str): The prefix for generating random email addresses for account creation.
        """
        self.email_prefix = email_prefix
        self.url_accounts = "https://api.hearling.com/accounts"
        self.url_clips = "https://api.hearling.com/clips"
        self.session = requests.Session()  # Create a session for faster requests
        self.token = self.create_account()  # Create an account upon initialization
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def create_account(self):
        """
        Creates a new account on the Hearling API.

        Generates a random email address using the email prefix and registers a new account with Hearling.

        Returns:
            str: The authentication token for the newly created account.
        """
        email = f"{self.email_prefix}{random.randint(10000, 99999)}@gmail.com"
        payload = {"email": email, "password": "DevsDoCode"}
        response = self.session.post(self.url_accounts, json=payload)
        response.raise_for_status()
        return response.json()['token']

    def update_token_async(self):
        """
        Updates the authentication token asynchronously.
        """
        future = self.executor.submit(self.create_account)
        future.add_done_callback(self.set_token)

    def set_token(self, future):
        """
        Sets the token from the future result.

        Args:
            future (Future): The future object containing the token.
        """
        self.token = future.result()

    def speak(self, text: str, voice: str = "hi-IN-Wavenet-D", filename: str = "ASSETS/audio_file.mp3", prints: bool = False):
        """
        Generates and plays audio from text using the Hearling API.

        Creates a new Hearling account, sends a request to generate speech from the given text and voice model,
        downloads the generated audio file, plays it using Interrupted_Playsound.play_audio, and then deletes the temporary audio file.

        Args:
            text (str): The text to convert to speech.
            voice (str): The voice model to use for speech generation.
            filename (str): The temporary file to save the audio output.
        """
        headers = {"Authorization": f"Bearer {self.token}"}

        payload = {"text": text, "voice": voice}
        response = self.session.post(self.url_clips, headers=headers, json=payload)
        response.raise_for_status()

        audio_url = response.json()['clip']['location']
        urllib.request.urlretrieve(audio_url, filename)
        if prints: print(f"Audio URL: {audio_url}")

        # Interrupted_Playsound.play_audio(filename)
        os.remove(filename)

        self.update_token_async()  # Update the token asynchronously after generating the audio



# if __name__ == "__main__":
#     aysnc_generator = Async_HearlingAudioGenerator()  # Create an instance of the class
#     text_to_speak = "सूरज की किरणें धीरे-धीरे  पेड़ों के पत्तों के बीच से झाँक रही थीं"
#     aysnc_generator.speak(text_to_speak)


if __name__ == "__main__":
    generator = Partial_Async_HearlingAudioGenerator()  # Create an instance of the class
    text_to_speak = 'सूरज की किरणें धीरे-धीरे  पेड़ों के पत्तों के बीच से झाँक रही थीं'
    generator.speak(text_to_speak)


# if __name__ == "__main__":
#     generator = HearlingAudioGenerator()  # Create an instance of the class
#     text_to_speak = 'सूरज की किरणें धीरे-धीरे  पेड़ों के पत्तों के बीच से झाँक रही थीं'
#     generator.speak(text_to_speak)
