"""----------------------------------------------------------------------------------------------SYSTEM IMPORTS------------------------------------------------------------------"""

import concurrent.futures
import os

"""----------------------------------------------------------------------------------------------USER IMPORTS----------------------------------------------------------------------"""

# from ENGINE.STT.vosk_recog import speech_to_text
# from ENGINE.STT.NetHyTech import SpeechToTextListener
from ENGINE.STT.DevsDoCode import SpeechToTextListener

# from ENGINE.TTS.hearling import Partial_Async_HearlingAudioGenerator
from ENGINE.TTS.DeepGram import speak
# from ENGINE.TTS.edge_tts import speak
# from ENGINE.TTS.deepAI import speak
# from ENGINE.TTS.ai_voice import speak, initiate_proxies
# from ENGINE.TTS.stream_elements_api import speak

from BRAIN.AI.TEXT.API import openrouter
from BRAIN.AI.TEXT.API import deepInfra_TEXT
from BRAIN.AI.TEXT.API import Phind
from BRAIN.AI.TEXT.API import Pi_Ai
from BRAIN.AI.TEXT.API import deepseek_ai
# from BRAIN.AI.TEXT.API import liaobots
# from BRAIN.AI.TEXT.API import hugging_chat; hf_api = hugging_chat.HuggingChat_RE(model="microsoft/Phi-3-mini-4k-instruct")
# from BRAIN.AI.TEXT.API import Blackbox_ai

from BRAIN.AI.VISION import deepInfra_VISION

# from BRAIN.TOOLS import groq_web_access

# from BRAIN.AI.IMAGE import deepInfra_IMG

# from PLAYGROUND.ADB_CALL import make_call, android_device_connection_setup; android_device_connection_setup.initialise()
from PLAYGROUND.WEBSITE_ASSISTANT import jenna_reader, chrome_latest_url
from PLAYGROUND.CAMERA import camera_vision

from PROMPTS import INSTRUCTIONS, BISECTORS

from TOOLS import Alpaca_DS_Converser, RawDog

"""----------------------------------------------------------------------------------------------INITIALIZATION-------------------------------------------------------------------"""

listener = SpeechToTextListener(language="en-IN")
history_manager = Alpaca_DS_Converser.ConversationHistoryManager()
ai_model = deepseek_ai.DeepSeekAPI()
# taskExecutor = RawDog.TaskExecutor()
# engine = Partial_Async_HearlingAudioGenerator()