from BRAIN.AI.TEXT.API import Le_Chat

chat_session = Le_Chat.LeChat()
while True:
        print("\n\n\033[93mYou:\033[0m ", end="", flush=True)
        message: str = input()
        if message.lower() == "/exit":
            break
        print("\033[92mAI: \033[0m", end="", flush=True)
        output: str = chat_session.generate(message)
        print("\n\n\n" + output)

