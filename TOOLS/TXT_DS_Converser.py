import os

class ConversationHistoryManager:
    def __init__(self, conversation_file="ASSETS/conversation_history.txt", max_lines=50):
        self.conversation_file = conversation_file
        self.max_lines = max_lines
        self.load_history()

    def load_history(self):
        """Loads conversation history from file, if it exists."""
        self.history = []
        if os.path.exists(self.conversation_file):
            with open(self.conversation_file, 'r') as f:
                self.history = f.readlines()

    def save_history(self):
        """Saves conversation history to file, truncating if necessary."""
        with open(self.conversation_file, 'w') as f:
            f.writelines(self.history[-self.max_lines:])

    def update_history(self, user_input, assistant_response):
        """Adds an entry to the history with the specified role and content."""
        self.history.append(f"User : {user_input}\n")
        self.history.append(f"Assistant : {assistant_response}\n")
        self.save_history()

    def get_formatted_history(self, user_input):
        """Returns the history formatted as a single string."""
        return "".join(self.history) + f"User : {user_input}\nAssistant :" 

# Example usage:
if __name__ == "__main__":
    history_manager = ConversationHistoryManager()

    while True:
        user_query = input("You: ")
        if user_query.lower() == '/bye':
            print("Exiting chat...")
            break

        print(history_manager.history)
        # Here you would call your AI model, passing the formatted history
        # assistant_response = your_ai_model.generate(history_manager.get_formatted_history())
        
        # For demonstration purposes, let's simulate an assistant response:
        assistant_response = "This is a simulated response based on your input." 

        history_manager.update_history(user_query, assistant_response)
        print(f"Assistant: {assistant_response}") 