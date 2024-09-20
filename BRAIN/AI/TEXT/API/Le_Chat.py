import requests
import json
import uuid
from TOOLS.LE_CHAT_COOKIES.Cookie_Extractor import get_ory_session_cookie
from dotenv import load_dotenv
import os

load_dotenv()


class LeChat:
    """
    A class to manage chat sessions with the Mistral AI chat API.

    Attributes:
        url (str): The base URL for the chat API.
        chat_id (str): The ID of the chat session.
        model (str): The name of the language model to use.
        env_file (str): The path to the .env file containing the session cookie.
        session (requests.Session): A session object for making HTTP requests.
        headers (dict): The HTTP headers to send with each request.
    """

    def __init__(self, chat_id: str = "ffd662bc-20a6-4fc8-a133-7994485df0de", model: str = "codestral"):
        """
        Initializes a new LeChat object.

        Args:
            chat_id: The ID of the chat session.
            model: The name of the language model to use.

        Available Models:
            - Codestral
            - Large
            - Next
            - Small
        """
        self.url: str = "https://chat.mistral.ai/api/chat"
        self.chat_id: str = chat_id
        self.model: str = model
        self.env_file: str = '.env'
        self.session: requests.Session = requests.Session()  # Create a session object
        self.headers: dict = {
            "Cookie": f"ory_session_coolcurranf83m3srkfl={os.environ.get('ORY_SESSION_COOKIE')}="
        }

    def _refresh_cookie(self) -> None:
        """Refreshes the cookie in case of expiration or unauthorized error."""
        ory_session_cookie: dict = get_ory_session_cookie()
        cookie_value: str = ory_session_cookie["value"][:-1]
        self.headers["Cookie"] = f"ory_session_coolcurranf83m3srkfl={cookie_value}="
        self._update_env_file(cookie_value)

    def _update_env_file(self, new_cookie_value: str) -> None:
        """Updates the .env file with the new cookie value."""
        with open(self.env_file, 'r') as file:
            lines: list = file.readlines()

        with open(self.env_file, 'w') as file:
            for line in lines:
                if line.startswith('ORY_SESSION_COOKIE='):
                    file.write(f'ORY_SESSION_COOKIE={new_cookie_value}\n')
                else:
                    file.write(line)

    def generate(self, message: str) -> str:
        """
        Sends a message to the chat and prints the response.

        Args:
            message: The message to send.

        Returns:
            The complete response from the chat API.
        """
        payload: dict = {
            "chatId": self.chat_id,
            "messageId": str(uuid.uuid4()),
            "model": self.model,
            "messageInput": message,
            "mode": "append"
        }

        while True:
            response: requests.Response = self.session.post(  # Use the session object for requests
                self.url, headers=self.headers, data=json.dumps(payload), stream=True
            )
            if response.status_code == 200:
                complete_final_response: str = ''
                for line in response.iter_lines(decode_unicode=True, chunk_size=1):
                    if line.startswith("0:"):
                        complete_final_response += line[3:-1]
                        print(line[3:-1], end='', flush=True)

                return complete_final_response

            elif response.status_code == 401:
                print("\033[91mCookie Expired... Trying to Refresh it. Please Wait...\033[0m")
                print(f"\033[91mOld Cookie: {self.headers['Cookie']}\033[0m")
                self._refresh_cookie()
                print(f"\033[92mNew Cookie: {self.headers['Cookie']}\033[0m")

            else:
                print("Error:", response.text)
                break  # Exit loop on other errors


if __name__ == "__main__":
    chat_session: LeChat = LeChat()
    while True:
        print("\n\n\033[93mYou:\033[0m ", end="", flush=True)
        message: str = input()
        if message.lower() == "/exit":
            break
        print("\033[92mAI: \033[0m", end="", flush=True)
        output: str = chat_session.generate(message)
        print("\n\n\n" + output)