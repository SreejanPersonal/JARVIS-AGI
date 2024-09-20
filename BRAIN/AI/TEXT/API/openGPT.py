import json
import os
import re
import uuid
from typing import List, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class ConversationalAgent:
    """
    Provides a conversational interface to a GPT-based assistant.

    This class manages assistant and user IDs, constructs API requests,
    and handles streaming responses for a more interactive experience.
    """

    def __init__(
        self,
        api_endpoint: str = "https://opengpts-example-vz4y4ooboq-uc.a.run.app/runs/stream",
        generate_new_Agents: bool = False,
        assistant_name: str = "Author - Devs Do Code",
        agent_type: str = "GPT 3.5 Turbo",
        retrieval_description: str = (
            "Can be used to look up information that was uploaded to this assistant.\n"
            "If the user is referencing particular files, that is often a good hint that information may be here.\n"
            "If the user asks a vague question, they are likely meaning to look up info from this retriever, "
            "and you should call it!"
        ),
        agent_system_message: str = "You are a helpful assistant.",
        chat_retrieval_llm_type: str = "GPT 3.5 Turbo",
        chat_retrieval_system_message: str = "You are a helpful assistant.",
        chatbot_llm_type: str = "GPT 3.5 Turbo",
        chatbot_system_message: str = "You are a helpful assistant.",
        enable_action_server: bool = False,
        enable_ddg_search: bool = False,
        enable_arxiv: bool = False,
        enable_press_releases: bool = False,
        enable_pubmed: bool = False,
        enable_sec_filings: bool = False,
        enable_retrieval: bool = False,
        enable_search_tavily: bool = False,
        enable_search_short_answer_tavily: bool = False,
        enable_you_com_search: bool = False,
        enable_wikipedia: bool = False,
        is_public: bool = True,
    ):
        self.api_endpoint = api_endpoint
        self.session = requests.Session()
        self.ids_file = "ASSETS/openGPT_IDs.txt"
        (
            self.assistant_id,
            self.user_id,
        ) = self._manage_assistant_and_user_ids(
            generate_new_Agents,
            assistant_name,
            agent_type,
            retrieval_description,
            agent_system_message,
            chat_retrieval_llm_type,
            chat_retrieval_system_message,
            chatbot_llm_type,
            chatbot_system_message,
            enable_action_server,
            enable_ddg_search,
            enable_arxiv,
            enable_press_releases,
            enable_pubmed,
            enable_sec_filings,
            enable_retrieval,
            enable_search_tavily,
            enable_search_short_answer_tavily,
            enable_you_com_search,
            enable_wikipedia,
            is_public,
        )

    def _manage_assistant_and_user_ids(
        self,
        generate_new_Agents: bool = False,
        assistant_name: str = "New Assistant",
        agent_type: str = "GPT 3.5 Turbo",
        retrieval_description: str = (
            "Can be used to look up information that was uploaded to this assistant.\n"
            "If the user is referencing particular files, that is often a good hint that information may be here.\n"
            "If the user asks a vague question, they are likely meaning to look up info from this retriever, "
            "and you should call it!"
        ),
        agent_system_message: str = "You are a helpful assistant.",
        chat_retrieval_llm_type: str = "GPT 3.5 Turbo",
        chat_retrieval_system_message: str = "You are a helpful assistant.",
        chatbot_llm_type: str = "GPT 3.5 Turbo",
        chatbot_system_message: str = "You are a helpful assistant.",
        enable_action_server: bool = False,
        enable_ddg_search: bool = False,
        enable_arxiv: bool = False,
        enable_press_releases: bool = False,
        enable_pubmed: bool = False,
        enable_sec_filings: bool = False,
        enable_retrieval: bool = False,
        enable_search_tavily: bool = False,
        enable_search_short_answer_tavily: bool = False,
        enable_you_com_search: bool = False,
        enable_wikipedia: bool = False,
        is_public: bool = True,
    ) -> tuple[str, str]:
        """
        Generates or retrieves assistant and user IDs.

        If 'generate_new_Agents' is True, new IDs are created and saved to 'ids.txt' and the '.env' file.
        Otherwise, IDs are loaded from the environment.

        Args:
            generate_new_Agents: If True, generate new IDs; otherwise, load from the environment.
            assistant_name: The name of the assistant (used when generating new IDs).
            agent_type: The type of the agent.
            retrieval_description: Description for the retrieval tool.
            agent_system_message: The system message for the agent.
            chat_retrieval_llm_type: The LLM type for chat retrieval.
            chat_retrieval_system_message: The system message for chat retrieval.
            chatbot_llm_type: The LLM type for the chatbot.
            chatbot_system_message: The system message for the chatbot.
            enable_action_server: Whether to enable the "Action Server by Robocorp" tool.
            enable_ddg_search: Whether to enable the "Duck Duck Go Search" tool.
            enable_arxiv: Whether to enable the "Arxiv" tool.
            enable_press_releases: Whether to enable the "Press Releases (Kay.ai)" tool.
            enable_pubmed: Whether to enable the "PubMed" tool.
            enable_sec_filings: Whether to enable the "SEC Filings (Kay.ai)" tool.
            enable_retrieval: Whether to enable the "Retrieval" tool.
            enable_search_tavily: Whether to enable the "Search (Tavily)" tool.
            enable_search_short_answer_tavily: Whether to enable the "Search (short answer, Tavily)" tool.
            enable_you_com_search: Whether to enable the "You.com Search" tool.
            enable_wikipedia: Whether to enable the "Wikipedia" tool.
            is_public: Whether the assistant should be public.

        Returns:
            A tuple containing the assistant ID and user ID.
        """

        if generate_new_Agents:
            user_id = str(uuid.uuid4())
            assistant_url = f"https://opengpts-example-vz4y4ooboq-uc.a.run.app/assistants/{str(uuid.uuid4())}"

            headers = {"Cookie": f"opengpts_user_id={user_id}"}

            tools = []
            if enable_action_server:
                tools.append("Action Server by Robocorp")
            if enable_ddg_search:
                tools.append("DDG Search")
            if enable_arxiv:
                tools.append("Arxiv")
            if enable_press_releases:
                tools.append("Press Releases (Kay.ai)")
            if enable_pubmed:
                tools.append("PubMed")
            if enable_sec_filings:
                tools.append("SEC Filings (Kay.ai)")
            if enable_retrieval:
                tools.append("Retrieval")
            if enable_search_tavily:
                tools.append("Search (Tavily)")
            if enable_search_short_answer_tavily:
                tools.append("Search (short answer, Tavily)")
            if enable_you_com_search:
                tools.append("You.com Search")
            if enable_wikipedia:
                tools.append("Wikipedia")

            payload = {
                "name": assistant_name,
                "config": {
                    "configurable": {
                        "thread_id": "",
                        "type": "agent",
                        "type==agent/agent_type": agent_type,
                        "type==agent/retrieval_description": retrieval_description,
                        "type==agent/system_message": agent_system_message,
                        "type==agent/tools": tools,
                        "type==chat_retrieval/llm_type": chat_retrieval_llm_type,
                        "type==chat_retrieval/system_message": chat_retrieval_system_message,
                        "type==chatbot/llm_type": chatbot_llm_type,
                        "type==chatbot/system_message": chatbot_system_message,
                    },
                    "public": is_public,
                },
            }

            response = requests.put(assistant_url, headers=headers, json=payload)
            response.raise_for_status()

            json_data = response.json()
            assistant_id = json_data["assistant_id"]

            with open(self.ids_file, "a") as f:
                f.write(f"Assistant ID: {assistant_id}\nUser ID: {user_id}\n\n")

            self._update_environment_variable("OPENGPT_ASSISTANT_ID", assistant_id)
            self._update_environment_variable("OPENGPT_USER_ID", user_id)

            return assistant_id, user_id
        else:
            return os.environ.get("OPENGPT_ASSISTANT_ID"), os.environ.get("OPENGPT_USER_ID")

    def _update_environment_variable(self, key: str, value: str):
        """
        Updates the '.env' file with the given key-value pair.
        If the key exists, its value is updated; otherwise, a new line with the key-value pair is appended.

        Args:
            key: The environment variable key.
            value: The value for the environment variable.
        """
        with open(".env", "r") as f:
            lines = f.readlines()

        updated = False
        with open(".env", "w") as f:
            for line in lines:
                if line.startswith(f"{key}="):
                    f.write(f"{key}={value}\n")
                    updated = True
                else:
                    f.write(line)
            if not updated:
                f.write(f"{key}={value}\n")

    def generate(
        self,
        conversation_history: List[Dict[str, str]],
        system_message: Optional[str] = "Be helpful and friendly",
        stream_response: bool = True,
    ) -> str:
        """
        Streams a conversation with a GPT model.

        Args:
            conversation_history: A list of dictionaries representing the conversation history.
                                 Each dictionary should have 'content' and 'type' keys, where 'type'
                                 is either 'user' or 'assistant'.
            system_message: An optional system message to guide the AI's behavior.
            stream_response: Whether to stream the response or return it all at once.

        Returns:
            The complete response generated by the GPT model.
        """

        if system_message:
            conversation_history.insert(0, {"content": system_message, "type": "system"})

        headers = {"Cookie": f"opengpts_user_id={self.user_id}"}
        payload = {
            "input": conversation_history,
            "assistant_id": self.assistant_id,
            "thread_id": str(uuid.uuid4()),
        }

        response = self.session.post(
            self.api_endpoint, headers=headers, json=payload, stream=stream_response
        )
        complete_response = ""
        printed_length = 0
        initial_responses_to_ignore = 2

        for line in response.iter_lines(decode_unicode=True, chunk_size=1):
            if line:
                try:
                    content = json.loads(re.sub("data:", "", line))[-1]["content"]
                    if initial_responses_to_ignore > 0:
                        initial_responses_to_ignore -= 1
                    else:
                        if stream_response:
                            print(content[printed_length:], end="", flush=True)
                        printed_length = len(content)
                        complete_response = content
                except:
                    continue

        return complete_response


if __name__ == "__main__":
    conversation_history = [
        {"role": "user", "content": "My favorite color is blue."},
        {"role": "assistant", "content": "Nice! Blue is a calming and serene color. Is there something else you'd like to share?"},
        {"role": "user", "content": "What color did I mention just now?"},
        {"role": "assistant", "content": "Ah, you mentioned blue! It's a great color, isn't it?"},
        {"role": "user", "content": "Write 30 Lines about India"},
    ]

    system_message = "Talk Like Shakesphere"

    # Use existing IDs from environment variables:
    # agent = ConversationalAgent()

    # Generate new IDs with specific tools:
    agent = ConversationalAgent(
        generate_new_Agents=True,
        assistant_name="My Helpful Assistant",
        agent_system_message="You are my custom assistant",
        # enable_wikipedia=True,
    )
    final_response = agent.generate(
                conversation_history, system_message=system_message, stream_response=True
            )
    print("\n\nFinal Response:", final_response)





"******************************************************************"

"""Deprecated v1.0. Requires Manual Update of Assistant IDs & User IDs"""

"******************************************************************"

def generate(
    conversation_history: List[Dict[str, str]],
    system_prompt: Optional[str] = "Be helpful and friendly",
    assistant_id: Optional[str] = os.environ.get("OPENGPT_ASSISTANT_ID"),
    user_id: Optional[str] = os.environ.get("OPENGPT_USER_ID"),
    stream=True
) -> str:
    """
    Streams a conversation with a GPT model hosted on the specified endpoint.

    Args:
        conversation_history: A list of dictionaries representing the conversation history.
                             Each dictionary should have "content" and "type" keys,
                             where "type" is either "user" or "assistant".
        system_prompt: An optional system prompt to guide the AI's behavior.
                      This prompt is added at the beginning of the conversation history.
        assistant_id: The ID of the assistant to use for the conversation.
        user_id: The ID of the user engaging in the conversation.

    Returns:
        The final response generated by the GPT model.
    """

    # Add the system prompt to the beginning of the conversation history
    if system_prompt:
        conversation_history.insert(0, {"content": system_prompt, "type": "system"})

    # Define the API endpoint and headers
    api_endpoint = "https://opengpts-example-vz4y4ooboq-uc.a.run.app/runs/stream"
    headers = {"Cookie": F"opengpts_user_id={user_id}"}

    # Construct the request payload
    payload = {
        "input": conversation_history,
        "assistant_id": assistant_id,
        "thread_id": str(uuid.uuid4()),
    }

    # Send the POST request and stream the response
    response = requests.post(api_endpoint, headers=headers, json=payload, stream=True)
    complete_response, printed_length, initial_responses_to_ignore = "", 0, 2

    for line in response.iter_lines(decode_unicode=True, chunk_size=1):
        if line:
            try:
                content = json.loads(re.sub("data:", "", line))[-1]['content']
                if initial_responses_to_ignore > 0:
                    initial_responses_to_ignore -= 1
                else:
                    if stream:
                        print(content[printed_length:], end="", flush=True)
                    printed_length, complete_response = len(content), content
            except:
                continue

    return complete_response



if __name__ == "__main__":
    conversation = [
    {"role": "user", "content": "My favorite color is blue."},
    {"role": "assistant", "content": "Nice! Blue is a calming and serene color. Is there something else you'd like to share?"},
    {"role": "user", "content": "What color did I mention just now?"},
    {"role": "assistant", "content": "Ah, you mentioned blue! It's a great color, isn't it?"},
    {"role": "user", "content": "Write 10 Lines about India"}
]

    system_message = "Talk Like Shakesphere" 
    final_response = generate(conversation, system_prompt=system_message, stream=True)
    print("\n\nFinal Response:", final_response) 
