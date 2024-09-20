from TOOLS.TXT_DS_Converser import ConversationHistoryManager
from BRAIN.AI.TEXT.API import Hugging_Face_TEXT

history_manager = ConversationHistoryManager()


while True:
        user_query = input("\033[1;36m\nYou: \033[0m")
        if user_query.lower() == '/bye':
            print("Exiting chat...")
            break

        # print(history_manager.history)
        print("\033[1;36mAssistant: \033[0m", end="", flush=True)
        assistant_response = Hugging_Face_TEXT.generate(history_manager.get_formatted_history(user_query), model="mistralai/Mixtral-8x7B-Instruct-v0.1", verbose=True)
        # print(assistant_response)
        history_manager.update_history(user_query, assistant_response)