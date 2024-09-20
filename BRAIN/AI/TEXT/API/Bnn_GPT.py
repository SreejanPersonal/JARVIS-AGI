import requests
import json
import os
from typing import Optional
from dotenv import load_dotenv; load_dotenv()

def generate_query(query: str, url: Optional[str] = "https://bnngpt.com/", verbose: Optional[bool] = True) -> str:
    """
    Sends a POST request to the specified URL with a query and processes the response in real-time.

    Args:
        query (str): The query string to be sent.
        url (Optional[str]): The URL to which the POST request will be sent. Defaults to "https://bnngpt.com/".
        verbose (Optional[bool]): If True, prints the content as it arrives. Defaults to True.

    Returns:
        str: The complete response from the server.

    Notes:
        This function sends a POST request to the specified URL with a query and processes the response in real-time.
        The response is processed in chunks, and each chunk is processed as it arrives.
        The function returns the complete response from the server.
    """

    # Define the headers
    request_headers = {
        "Accept": "text/x-component",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarycDuq4Qbo8Y2u0is9",
        "Next-Action": os.environ.get("BNN_GPT_ACTION_ID"),
    }

    # Define the payload
    payload = (
        "------WebKitFormBoundarycDuq4Qbo8Y2u0is9\r\n"
        "Content-Disposition: form-data; name=\"1\"\r\n\r\n"
        "{\"id\":\"6399a7e212fa477d1a783edade27c8354a64e1ab\",\"bound\":null}\r\n"
        "------WebKitFormBoundarycDuq4Qbo8Y2u0is9\r\n"
        "Content-Disposition: form-data; name=\"2\"\r\n\r\n"
        "{\"id\":\"9eed8f3e1c51044505fd5c0d73e8d2a92572691c\",\"bound\":null}\r\n"
        "------WebKitFormBoundarycDuq4Qbo8Y2u0is9\r\n"
        "Content-Disposition: form-data; name=\"3_input\"\r\n\r\n"
        f"{query}\r\n"
        "------WebKitFormBoundarycDuq4Qbo8Y2u0is9\r\n"
        "Content-Disposition: form-data; name=\"0\"\r\n\r\n"
        "[{\"action\":\"$F1\",\"options\":{\"onSetAIState\":\"$F2\"}},"
        "{\"chatId\":\"DevsDoCode\",\"messages\":[]},\"$K3\",\"gpt-4o\"]\r\n"
        "------WebKitFormBoundarycDuq4Qbo8Y2u0is9--"
    )

    # Initialize variables
    response_counter = 2
    complete_response = ""

    # Send the POST request
    response = requests.post(url, headers=request_headers, data=payload, stream=True)

    # Process the response stream
    for chunk in response.iter_lines(decode_unicode=True, chunk_size=1):
        try:
            chunk_ = chunk[2:]
            chunk_ = json.loads(chunk_)
        except json.JSONDecodeError:
            try:
                chunk_ = chunk[3:]
                chunk_ = json.loads(chunk_)
            except:
                continue
        except:
            continue

        try:
            if response_counter > 0:
                if chunk_['curr'] != True:
                    complete_response += str(chunk_['curr'])
                    if verbose:
                        print(str(chunk_['curr']), end="", flush=True)
                response_counter -= 1
        except:
            continue

        try:
            complete_response += str(chunk_['diff'][1])
            if verbose:
                print(chunk_['diff'][1], end="", flush=True)
        except:
            continue

    return complete_response

# Example usage
if __name__ == "__main__":
    response = generate_query("are you based on GPT 4 architecture?")
    print("\033[92m\n\nResponse:", response, "\033[0m")
