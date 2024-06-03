import json
import re
import requests
import os
from dotenv import load_dotenv; load_dotenv()

def generate(user_query: str, session_cookie: str = "Devs Do Code (Sree)", prints: bool = True) -> str:
    """
    Generates a response from the Pi AI chatbot.

    Args:
        user_query: The user's query for the chatbot.
        session_cookie: The current session cookie for authentication. Most Probably it will work without Providing. If it doesn't then leave it
                                            # cookie_value = "b2XpQkztQ3rPmEBmwTG0cC4NBNXMhn5mqAWWbaUwhvY-1715447379-1.0.1.1-ynhRE6bjmJzEc2mIbYU2c25x_EcEjFrPALAoCPODut8NQdwuICnyaN5Lr9ETY3N_qlRUiatFPeTTB3n.a3UeSA"

    Returns:
        The complete response from the chatbot as a single string.
    """

    API_ENDPOINT = "https://pi.ai/api/chat" 
    session_id = os.environ.get("PI_SESSION_ID")
    conversation_id = os.environ.get("PI_CONVERSATION_ID")
    headers = {
        "Accept": "text/event-stream",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Content-Type": "application/json",
        "Cookie": f"__Host-session={session_id}; __cf_bm={session_cookie}",
        "Dnt": "1",
        "Origin": "https://pi.ai",
        "Priority": "u=1, i",
        "Referer": "https://pi.ai/talk",
        "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Api-Version": "3"
    }

    payload = {"text": user_query, "conversation": conversation_id}
    response = requests.post(API_ENDPOINT, json=payload, headers=headers, stream=True)
    
    if response.status_code in (401, 403):
        print("Assuming the Cookie is Expired.... Generating New Cookie.....")
        cookie_value = list(requests.get("https://pi.ai").cookies)[0].value if requests.get("https://pi.ai").cookies else None
        print("New Cookie Generated: ", cookie_value)
        generate(user_query, cookie_value)
        # raise ValueError(f"Error: {response.text}, Status Code: {response.status_code}")

    complete_response = ""

    if response.status_code == 200:
        for line in response.iter_lines(decode_unicode=True, chunk_size=1):
            if line:
                modified_line = re.sub("data:", "", line)
                try:
                    json_data = json.loads(modified_line)
                    content = json_data['text']
                    with_emoji = content.encode('latin1').decode('utf-8')
                    if prints: print(with_emoji, end="", flush=True)
                    complete_response += with_emoji  
                except:  continue

    return complete_response

if __name__ == "__main__":
    
    while True:
        user_query = input("\033[0;31m\nUser: \033[0m")
        print("\033[0;32mPi AI: \033[0m", end="", flush=True)
        complete_response = generate(user_query)