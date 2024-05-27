from typing import Dict, Any

from rich.console import Console
from rich.markdown import Markdown

import webscout
import webscout.AIutel

class TaskExecutor:
    """
    Manages an interactive chat session, handling user input, AI responses, 
    and optional features like web search, code execution, and text-to-speech.
    """

    def __init__(self) -> None:
        """Initializes the conversational assistant with default settings."""
        self._console: Console = Console()

        # Session configuration
        self._selected_provider: str = "phind"
        self._selected_model: str = "Phind Model"
        self._conversation_enabled: bool = True
        self._max_tokens: int = 600
        self._temperature: float = 0.2
        self._top_k: int = -1
        self._top_p: float = 0.999
        self._timeout: int = 30
        self._auth_token: str = None  

        # History Management
        self._history_filepath: str = None
        self._update_history_file: bool = True
        self._history_offset: int = 10250

        # Prompt Engineering
        self._initial_prompt: str = None
        self._awesome_prompt_content: str = None 

        # Optional Features
        self._web_search_enabled: bool = False
        self._rawdog_enabled: bool = True
        self._internal_script_execution_enabled: bool = False
        self._script_confirmation_required: bool = False
        self._selected_interpreter: str = "python"
        self._selected_optimizer: str = "code"
        self._suppress_output: bool = False  
        self._chat_completion_enabled: bool = False 
        self._ignore_working: bool = False 
        self._proxy_path: str = None 

        # AI provider mapping
        self._ai_provider_mapping: Dict[str, Any] = {
            "phind": webscout.PhindSearch,
            "opengpt": webscout.OPENGPT,
            "koboldai": webscout.KOBOLDAI,
            "blackboxai": webscout.BLACKBOXAI,
            "llama2": webscout.LLAMA2,
            "yepchat": webscout.YEPCHAT,
            "leo": webscout.LEO,
            "groq": webscout.GROQ,
            "openai": webscout.OPENAI,
            "perplexity": webscout.PERPLEXITY,
            "you": webscout.YouChat,
            "xjai": webscout.Xjai,
            "cohere": webscout.Cohere,
            "reka": webscout.REKA,
            "thinkany": webscout.ThinkAnyAI,
        }

        # Initialize Rawdog if enabled
        if self._rawdog_enabled:
            self._rawdog_instance: webscout.AIutel.RawDog = webscout.AIutel.RawDog(
                quiet=self._suppress_output,
                internal_exec=self._internal_script_execution_enabled,
                confirm_script=self._script_confirmation_required,
                interpreter=self._selected_interpreter,
            )

            self._initial_prompt = self._rawdog_instance.intro_prompt

        # Initialize the selected AI model 
        self._ai_model = self._ai_provider_mapping[self._selected_provider](
            is_conversation=self._conversation_enabled,
            max_tokens=self._max_tokens,
            timeout=self._timeout,
            intro=self._initial_prompt,
            filepath=self._history_filepath,
            update_file=self._update_history_file,
            proxies={}, 
            history_offset=self._history_offset,
            act=self._awesome_prompt_content, 
            model=self._selected_model,
            quiet=self._suppress_output,
        )

    def process_query(self, query: str) -> None:
        """
        Processes a user query, potentially enhancing it with web search results, 
        passing it to the AI model, and handling the response.

        Args:
            query: The user's text input.

        Returns:
            None
        """
        if self._web_search_enabled:
            query = self._augment_query_with_web_search(query)

        query = webscout.AIutel.Optimizers.code(query)

        try:
            response: str = self._ai_model.chat(query)
        except webscout.exceptions.FailedToGenerateResponseError as e:
            self._console.print(Markdown(f"LLM: [red]{e}[/red]"))
            return

        if self._rawdog_enabled:
            self._handle_rawdog_response(response)
        else:
            self._console.print(Markdown(f"LLM: {response}"))

    def _augment_query_with_web_search(self, query: str) -> str:
        """Performs a web search and appends the results to the query.

        Args:
            query: The user's text input.

        Returns:
            str: The augmented query with web search results.
        """
        web_search_results = webscout.WEBS().text(query, max_results=3)
        if web_search_results:
            formatted_results = "\n".join(
                f"{i+1}. {result['title']} - {result['href']}\n\nBody: {result['body']}"
                for i, result in enumerate(web_search_results)
            )
            query += f"\n\n## Web Search Results are:\n\n{formatted_results}"
        return query

    def _handle_rawdog_response(self, response: str) -> None:
        """Handles AI responses, potentially executing them as code with Rawdog.

        Args:
            response: The AI model's response.

        Returns:
            None
        """
        try:
            is_feedback = self._rawdog_instance.main(response)
        except Exception as e:
            self._console.print(Markdown(f"LLM: [red]Error: {e}[/red]"))
            return
        if is_feedback:
            self._console.print(Markdown(f"LLM: {is_feedback}"))
        else:
            self._console.print(Markdown("LLM: (Script executed successfully)"))

if __name__ == "__main__":
    assistant = TaskExecutor()
    while True:
        input_query = input("Enter your query: ")
        assistant.process_query(input_query)