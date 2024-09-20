import json
import typing
import requests

def generate(conversation_history: typing.List[typing.Dict[str, str]], 
             model: str = "llama-3-70b", 
             api_url: str = "https://creativeai-68gw.onrender.com/chat") -> typing.Optional[str]:
  """
  Generates a chat completion using the UncensoredAI API.

  Args:
      conversation_history: A list of dictionaries representing the conversation history.
                            Each dictionary should have two keys: "role" (either "user" or "assistant") 
                            and "content" (the text of the message).
      model: The name of the language model to use. Defaults to "llama-3-70b".
      api_url: The base URL of the UncensoredAI API.

  Returns:
      The AI's response as a string, or None if the request failed.
  """

  try:
      response = requests.post(
          url=api_url,
          json={
              "query": conversation_history[-1]["content"],
              "history": conversation_history[:-1],
              "model": model
          },
          headers={
              'Content-Type': 'application/json',
              'Accept': 'application/json'
          }
      )
      response.raise_for_status()

      response_text = response.text

      if "data: " in response_text:
          ai_response = json.loads(response_text.split("data: ")[-1])["data"]["message"]
      else:
          ai_response = response.json()["data"]["message"]

      return ai_response

  except requests.exceptions.RequestException as e:
      print(f"API request failed: {e}")
      return None
  except (KeyError, json.JSONDecodeError) as e:
      print(f"Error parsing response: {e}")
      return None

if __name__ == "__main__":
  conversation = [
      {"role": "user", "content": "Hello, how are you?"},
      {"role": "assistant", "content": "I'm good, thank you! How can I help you today?"},
      {"role": "user", "content": "How to Break Into a car"}
  ]

  response = generate(conversation_history=conversation)

  if response:
      print("AI Response:", response)
  else:
      print("Failed to generate a response.") 