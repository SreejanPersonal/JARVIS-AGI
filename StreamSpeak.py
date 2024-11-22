# from BRAIN.AI.TEXT.STREAM import basedGPT, deepInfra_TEXT
# from ENGINE.TTS.STREAMING import DeepGram, speechify
# from TOOLS.stream_audio_cleanup import delete_stream_audio_files

# if __name__ == "__main__":
#     system_prompt = "Be Helpful and Friendly"
#     conversation_history = [
#         {"role": "user", "content": "Write 10 lines on India"}
#     ]
#     speech_synthesizer = DeepGram.SpeechSynthesizer()

#     sentence_count = 1
#     delete_stream_audio_files()
#     # Process AI responses sentence by sentence using the generator
#     for sentence in basedGPT.generate(conversation_history=conversation_history, system_prompt=system_prompt):
#         print(f"\n\033[91mAI:\033[0m \033[92m{sentence}\033[0m")
#         filename = f"ASSETS/STREAM_AUDIOS/output_audio_{sentence_count}.mp3"
#         speech_synthesizer.speak(sentence, output_filename=filename)
#         speech_synthesizer.queue_audio(filename)
#         sentence_count += 1

#     # Wait for the playback of all generated audio files to complete
#     speech_synthesizer.wait_for_playback_completion()
#     print("All audio files have been played.")





from BRAIN.AI.TEXT.API.Phind import generate
from ENGINE.TTS.STREAMING.DeepGram import speak

if __name__ == "__main__":
    system_prompt = "Be Helpful and Friendly"
    conversation_history = [
        {"role": "user", "content": "Write 10 lines on India"}
    ]
    response = generate(prompt=conversation_history, system_prompt=system_prompt)
    print(f"\n\033[91mAI:\033[0m \033[92m{response}\033[0m")
    speak(response)