# ██████╗   ███████╗ ██╗    ██╗ ███████╗            ██████╗    ██████╗             ██████╗   ██████╗    ██████╗   ███████╗
# ██╔══██╗ ██╔════╝ ██║    ██║ ██╔════╝            ██╔══██╗ ██╔═══██╗          ██╔════╝ ██╔═══██╗ ██╔══██╗ ██╔════╝
# ██║    ██║ █████╗     ██║    ██║ ███████╗            ██║    ██║ ██║      ██║         ██║          ██║      ██║ ██║    ██║ █████╗  
# ██║    ██║ ██╔══╝    ╚██╗  ██╔╝ ╚════██║           ██║    ██║ ██║      ██║         ██║          ██║      ██║ ██║    ██║ ██╔══╝  
# ██████╔╝ ███████╗  ╚████╔╝  ███████║            ██████╔╝╚██████╔╝          ╚██████╗ ╚██████╔╝  ██████╔╝ ███████╗
# ╚═════╝  ╚══════╝    ╚═══╝     ╚══════╝            ╚═════╝    ╚═════╝             ╚═════╝   ╚═════╝    ╚═════╝   ╚══════╝

#  Made With 💓 By - Sree ( Devs Do Code )
#  YouTube Channel: https://www.youtube.com/@devsdocode

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

      - Support: https://buymeacoffee.com/devsdocode
      - Patreon: https://patreon.com/DevsDoCode

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#  For any questions or concerns, reach out to us via our social media handles.
#  Our top choice for contact is Telegram: https://t.me/devsdocode
#  You can also find us on other platforms listed above. We're here to help!

#  - YouTube Channel: https://www.youtube.com/@DevsDoCode
#  - Telegram Group: https://t.me/devsdocode
#  - Discord Server: https://discord.gg/ehwfVtsAts
#  - Instagram:
#    - Personal: https://www.instagram.com/sree.shades_/
#    - Channel: https://www.instagram.com/devsdocode_/

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    - Support: https://buymeacoffee.com/devsdocode
    - Patreon: https://patreon.com/DevsDoCode

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  ------------------------------------------------------------------------------
#  Dive into the world of coding with Devs Do Code - where passion meets programming!
#  Make sure to hit that Subscribe button to stay tuned for exciting content!

#  Pro Tip: For optimal performance and a seamless experience, we recommend using
#  the default library versions demonstrated in this demo. Your coding journey just
#  got even better! Happy coding!
#  ----------------------------------------------------------------------------


"""-------------------------------------------------------------------------------------------------IMPORTS-------------------------------------------------------------------------------------------------"""

# from ENGINE.STT.vosk_recog import speech_to_text
from ENGINE.STT.NetHyTech import SpeechToTextListener; listener = SpeechToTextListener()

# from ENGINE.TTS.edge_tts import speak
# from ENGINE.TTS.deepAI import speak
# from ENGINE.TTS.ai_voice import speak, initiate_proxies
from ENGINE.TTS.stream_elements_api import speak

# from BRAIN.AI.TEXT.API import deepInfra_TEXT
# from BRAIN.AI.TEXT.API import openrouter
# from BRAIN.AI.TEXT.API import liaobots
from BRAIN.AI.TEXT.API import hugging_chat


# from BRAIN.TOOLS import groq_web_access

"""-------------------------------------------------------------------------------------------------MAIN-----------------------------------------------------------------------------------------------------"""

# for speech in speech_to_text():
hf_api = hugging_chat.HuggingChat_RE(model="microsoft/Phi-3-mini-4k-instruct")
while True:
    speech = listener.listen()   
    print("Human >>", speech)

    ai_response = hf_api.generate(speech)
    print("AI >>", ai_response)
    print(ai_response)
    speak(ai_response)

