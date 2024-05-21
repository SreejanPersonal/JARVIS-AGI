import json
import os

class ConversationHistoryManager:
    def __init__(self, conversation_file="ASSETS/conversation_history.json", history_offset=400):
        self.history_offset = history_offset
        self.conversation_file = conversation_file
        if os.path.exists(conversation_file):
            # If conversation file exists, check if it's empty
            if os.stat(conversation_file).st_size == 0:
                # If file is empty, initialize self.history to an empty list
                self.history = []
            else:
                # If file is not empty, load the list from the file
                with open(conversation_file, "r") as file:
                    self.history = json.load(file)
                
                # Check if the last entry in history is a user entry
                if self.history and self.history[-1].get("role") == "user":
                    print("Deleted")
                    # If the last entry is a user entry, pop it out from both history and file
                    self.history.pop()
                    with open(conversation_file, "w") as file:
                        json.dump(self.history, file, indent=4)
        else:
            # If conversation file doesn't exist, initialize self.history to an empty list
            self.history = []

    def count_words(self):
        return sum(len(entry["content"].split()) for entry in self.history)

    def strip_history(self):
        total_words = self.count_words()
        while total_words > self.history_offset and self.history:
            total_words -= len(self.history.pop(0)["content"].split())
        return self.history

    def store_history(self, history):
        self.history = history
        self.strip_history()

    def update_file(self, user_query, assistant_response):
        conversation_json = [{"role": "user", "content": user_query}, {"role": "assistant", "content": assistant_response}]
        data = []
        if os.path.exists(self.conversation_file) and os.path.getsize(self.conversation_file) > 0:
            with open(self.conversation_file, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    pass

        for entry in conversation_json:
            if isinstance(entry, dict):
                data.append(entry)

        with open(self.conversation_file, "w") as file:
            json.dump(data, file, indent=4)

        self.store_history(self.history + [{"role": "assistant", "content": assistant_response}])

    def load_history(self):
        with open(self.conversation_file, "r") as file:
            self.history = json.load(file)

    def strip_history_by_word_limit(self, word_limit):
        total_words = 0
        trimmed_history = []

        # Traverse the history from the end to the beginning
        for entry in reversed(self.history):
            entry_words = len(entry["content"].split())
            if total_words + entry_words > word_limit:
                break
            trimmed_history.insert(0, entry)
            total_words += entry_words

        self.history = trimmed_history



if __name__ == "__main__":

    history_manager = ConversationHistoryManager()

    while True:
        user_query = input("You: ")
        if user_query.lower() == '/bye':
            print("Exiting chat...")
            break

        history_manager.store_history(history_manager.history + [{"role": "user", "content": user_query}])
        print("\n\n\033[93m" + str(history_manager.history) + "\033[0m\n\n")
        history_manager.update_file(user_query, "THIS IS THE ASSISTANT RESPONSE")
