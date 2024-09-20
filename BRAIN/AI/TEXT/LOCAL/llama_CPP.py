from typing import Optional
import os
from dotenv import load_dotenv; load_dotenv()

from webscout.Local.samplers import SamplerSettings as WebscoutSamplerSettings
from webscout.Local.utils import download_model
from webscout.Local.thread import Thread as WebscoutThread
from webscout.Local.model import Model as WebscoutModel
from webscout.Local import formats

class GGUFChatbot:
    """
    A class to interact with a large language model from Hugging Face,
    stored in the GGUF format, using the webscout library.
    """

    def __init__(self, 
                 system_prompt: str = "Be Helpful. Respond very short and concise", 
                 temperature: float = 0.7, 
                 top_p: float = 0.9,
                 n_gpu_layers: int = 20,
                 model_repo_id: str = "MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF",
                 model_filename: str = "Mistral-7B-Instruct-v0.3.Q8_0.gguf",
                 hf_token: str = os.environ.get("HUGGING_FACE_WRITE"), 
                 chatML: str = formats.mistral_instruct.copy()) -> None:
        """
        Initializes the GGUFChatbot.

        Args:
            system_prompt: The system prompt to use for the chatbot.
            temperature: The temperature to use for the sampler.
            top_p: The top_p value to use for the sampler.
            n_gpu_layers: Number of GPU layers to use.
            model_repo_id: The repository ID for the model on the Hugging Face Model Hub.
            model_filename: The filename of the model on the Hugging Face Model Hub.
            hf_token: Your Hugging Face API token.
            chatML: The chatML format to use.
        """

        self.model_repo_id = model_repo_id
        self.model_filename = model_filename
        self.hf_token = hf_token

        # Initialize self.chat_format here
        self.chat_format = chatML

        self.model = self._download_and_load_model(n_gpu_layers)
        self.chat_format = self._create_chat_format(system_prompt)
        self.sampler_settings = WebscoutSamplerSettings(temp=temperature, top_p=top_p)
        self.conversation_thread = self._create_conversation_thread()
        

    def _download_and_load_model(self, n_gpu_layers: int) -> WebscoutModel:
        """Downloads and loads the language model from the Hugging Face Hub."""
        model_path = download_model(self.model_repo_id, self.model_filename, self.hf_token)
        return WebscoutModel(model_path, n_gpu_layers=n_gpu_layers)

    def _create_chat_format(self, system_prompt: str) -> dict:
        """Creates a custom ChatML format with the given system prompt."""
        self.chat_format['system_content'] = system_prompt
        return self.chat_format

    def _create_conversation_thread(self) -> WebscoutThread:
        """Creates a new conversation thread with the model, format, and sampler."""
        return WebscoutThread(self.model, self.chat_format, sampler=self.sampler_settings)

    def send_message(self, message: str) -> Optional[str]:
        """
        Sends a message to the chatbot and returns the response.

        Args:
            message: The message to send to the chatbot.

        Returns:
            The chatbot's response, or None if an error occurred.
        """
        try:
            response = self.conversation_thread.send(message)
            return response
        except Exception as e:
            print(f"An error occurred while sending the message: {e}")
            return None
        
    def interact_with_model(self) -> None:
        """Start interacting with the model"""
        self.conversation_thread.interact(header="🌟 Welcome to the Jarvis-3B Prototype by Sree and OEvortex 🚀", color=True)
        # response = thread.send("Initiate system startup")

if __name__ == "__main__":
    chatbot = GGUFChatbot(system_prompt="Be Helpful", )
    chatbot.interact_with_model()

        
    response = chatbot.send_message("Hello, I am Jarvis!")
    print(response)
