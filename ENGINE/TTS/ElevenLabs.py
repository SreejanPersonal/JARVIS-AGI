import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Any

import playsound
import requests

from TOOLS.ProxyAPI import get_proxies


class ElevenLabsAPI:
    """
    A class to interact with the ElevenLabs Text-to-Speech API.

    This class provides functionalities to synthesize speech from text using various voices
    provided by ElevenLabs, utilizing a pool of proxy servers for enhanced reliability.

    Voices: 
            "charlottee": "XB0fDUnXU5powFXDhCwa",
            "daniel": "onwK4e9ZLuTAKqWW03F9",
            "callum": "N2lVS1w4EtoT3dr4eOWO",
            "charlie": "IKne3meq5aSn9XLyUdCD",
            "clyde": "2EiwWnXFnvU5JabPnv8n",
            "dave": "CYw3kZ02Hs0563khs1Fj",
            "emily": "LcfcDJNUP1GQjkzn1xUU",
            "ethan": "g5CIjZEefAph4nQFvHAz",
            "fin": "D38z5RcWu1voky8WS1ja",
            "freya": "jsCqWAovK2LkecY7zXl4",
            "gigi": "jBpfuIE2acCO8z3wKNLl",
            "giovanni": "zcAOhNBS3c14rBihAFp1",
            "glinda": "z9fAnlkpzviPz146aGWa",
            "grace": "oWAxZDx7w5VEj9dCyTzz",
            "harry": "SOYHLrjzK2X1ezoPC6cr",
            "james": "ZQe5CZNOzWyzPSCn5a3c",
            "jeremy": "bVMeCyTHy58xNoL34h3p"

    """

    def __init__(self, model_id: str = "eleven_multilingual_v2") -> None:
        """
        Initializes the ElevenLabsAPI with provided parameters.

        Args:
            model_id (str, optional): The ID of the ElevenLabs speech synthesis model.
                Defaults to "eleven_multilingual_v2".
        """
        self.filename: str = "ASSETS/available_working_proxies.txt"
        self.model_id: str = model_id
        self.base_url: str = "https://api.elevenlabs.io/v1/text-to-speech"
        self.headers: Dict[str, str] = {
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            'Content-Type': 'application/json',
            'Dnt': '1',
            'Origin': 'https://elevenlabs.io',
            'Priority': 'u=1, i',
            'Referer': 'https://elevenlabs.io/',
            'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
        self.voice_ids: Dict[str, str] = {
            "charlottee": "XB0fDUnXU5powFXDhCwa",
            "daniel": "onwK4e9ZLuTAKqWW03F9",
            "callum": "N2lVS1w4EtoT3dr4eOWO",
            "charlie": "IKne3meq5aSn9XLyUdCD",
            "clyde": "2EiwWnXFnvU5JabPnv8n",
            "dave": "CYw3kZ02Hs0563khs1Fj",
            "emily": "LcfcDJNUP1GQjkzn1xUU",
            "ethan": "g5CIjZEefAph4nQFvHAz",
            "fin": "D38z5RcWu1voky8WS1ja",
            "freya": "jsCqWAovK2LkecY7zXl4",
            "gigi": "jBpfuIE2acCO8z3wKNLl",
            "giovanni": "zcAOhNBS3c14rBihAFp1",
            "glinda": "z9fAnlkpzviPz146aGWa",
            "grace": "oWAxZDx7w5VEj9dCyTzz",
            "harry": "SOYHLrjzK2X1ezoPC6cr",
            "james": "ZQe5CZNOzWyzPSCn5a3c",
            "jeremy": "bVMeCyTHy58xNoL34h3p"
        }
        self.session: requests.Session = requests.Session()  # Create a session

    def get_proxies_list(self) -> List[str]:
        """
        Reads and returns a list of proxy servers from a file.

        Returns:
            List[str]: A list of proxy server addresses.
        """
        with open(self.filename, 'r') as f:
            proxies = f.read().split("\n")[:-1]
        return proxies

    def make_request(self, proxy: str, payload: Dict[str, str], voice_id: str) -> Optional[requests.Response]:
        """
        Makes a request to the ElevenLabs API using a specific proxy server.

        Args:
            proxy (str): The address of the proxy server.
            payload (Dict[str, str]): The request payload containing text and model information.
            voice_id (str): The ID of the desired voice.

        Returns:
            Optional[requests.Response]: The API response if successful, otherwise None.
        """
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        url = f"{self.base_url}/{voice_id}/stream"
        try:
            response = self.session.post(url, headers=self.headers, json=payload, proxies=proxies, timeout=7)
            if response.status_code == 200:
                return response
            else:
                print(f"Proxy {proxy} failed with status code {response.status_code}.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Proxy {proxy} failed with error: {e}.")
            return None

    def fetch_response_with_proxies(self, payload: Dict[str, str],
                                    voice_id: str) -> Optional[requests.Response]:
        """
        Fetches the API response by iterating through a list of proxy servers.

        Args:
            payload (Dict[str, str]): The request payload.
            voice_id (str): The ID of the desired voice.

        Returns:
            Optional[requests.Response]: The API response if successful, otherwise None.
        """
        proxies = self.get_proxies_list()
        while True:  # Retry loop
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_proxy = {executor.submit(self.make_request, proxy, payload, voice_id): proxy for proxy in
                                   proxies}
                for future in as_completed(future_to_proxy):
                    response = future.result()
                    if response:
                        return response
            print("\033[91mNo response obtained from API. Retrying with a new set of proxies...\033[0m")
            get_proxies()
            proxies = self.get_proxies_list()  # Update proxies for the retry

    def speak(self, text: str, voice_name: Optional[str] = None, voice_id: Optional[str] = None,
              filename: Optional[str] = "ASSETS/ElevenLabs_response.mp3") -> None:
        """
        Synthesizes speech from text using the specified voice and plays it aloud.

        Args:
            text (str): The text to be converted into speech.
            voice_name (Optional[str], optional): The name of the desired voice.
                Defaults to None.
            voice_id (Optional[str], optional): The ID of the desired voice.
                Defaults to None.
        """
        if voice_name:
            voice_id = self.voice_ids.get(voice_name.lower())
            if not voice_id:
                print(
                    f"Invalid voice name: {voice_name}. Please choose from: {', '.join(self.voice_ids.keys())}")
                return

        if not voice_id:
            print("Please specify either a voice name or a voice ID.")
            return

        payload: Dict[str, str] = {
            "text": text,
            "model_id": self.model_id
        }
        response: Optional[requests.Response] = self.fetch_response_with_proxies(payload, voice_id)

        if response:
            print("\033[92m" + "Successfully obtained response from API." + "\033[0m")
            if os.path.exists(filename):
                os.remove(filename)
            with open(filename, "wb") as file:
                file.write(response.content)
            playsound.playsound(filename)




"****************************************************"

# This Code will not Run in this File Due to Circular Imports

"****************************************************"



if __name__ == "__main__":
    import time
    api = ElevenLabsAPI()
    if True:
        start_time = time.time()
        api.speak(text="""तूफ़ानों से आँख मिलाओ, सैलाबों पर वार करो
मल्लाहों का चक्कर छोड़ो, तैर के दरिया पार करो

ऐसी सर्दी है कि सूरज भी दुहाई मांगे
जो हो परदेस में वो किससे रज़ाई मांगे
...फकीरी पे तरस आता है
अपने हाकिम की फकीरी पे तरस आता है
जो गरीबों से पसीने की कमाई मांगे

जुबां तो खोल, नजर तो मिला, जवाब तो दे
मैं कितनी बार लुटा हूँ, हिसाब तो दे""",
                  voice_name="callum")

        response_time = time.time() - start_time
        print("\033[91m" + f"Response time: {response_time:.2f} seconds" + "\033[0m")