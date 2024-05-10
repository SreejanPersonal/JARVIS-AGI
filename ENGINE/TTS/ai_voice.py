import requests
import threading
import os
from playsound import playsound
import time

filename = "ASSETS/available_working_proxies.txt"

def get_proxies(filename: str = filename, number_of_proxies: int = 100, prints: bool = False) -> None:
    """
    This function retrieves a list of proxies from a remote API, checks their validity asynchronously using threads, and stores the working proxies in a file.

    Parameters:
    - filename (str): The name of the file to store the working proxies. Defaults to "available_working_proxies.txt".
    - number_of_proxies (int): The number of proxies to retrieve from the API. Defaults to 100.
    - prints (bool): A flag indicating whether to print progress messages. Defaults to False.

    Returns:
    - None: The function does not return anything; it stores the working proxies in the specified file.
    """

    if prints: print("Sending Request to get the all proxies......")
    resp = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
    # proxies = resp.text.strip().split("\n")
    proxies = resp.text.strip().split("\n")[:number_of_proxies]
    if prints: print("Extracted 100 proxies out of the response")

    # Filter out empty or invalid proxies
    proxies = [proxy.strip() for proxy in proxies if proxy.strip()]

    # Initialize a list to store working proxies
    working_proxies = []

    # Define a function to check a single proxy
    def check_proxy(proxy):
        try:
            proxy_ = {'http': proxy, 'https': proxy}
            check_resp = requests.get("https://ttsmp3.com/", proxies=proxy_, timeout=5)
            if check_resp.status_code == 200:
                working_proxies.append(proxy)
                # print(f"{proxy} is working")
        except Exception as e:
            pass
            # print(f"Error checking {proxy}: {e}")

    if prints: print("Checking the working of all the proxies........")
    # Create a thread for each proxy and start them
    threads = [threading.Thread(target=check_proxy, args=(proxy,)) for proxy in proxies]
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Print the number of working proxies
    if prints: print(f"Found {len(working_proxies)} working proxies out of {len(proxies)}\nWorking Proxies Percentage : {round(len(working_proxies)/len(proxies)*100)}%")

    if prints: print(f"Storing the proxies in {filename}........")
    # Open the file and truncate its content
    open(filename, "w").close()
    for working_proxy in working_proxies:
        try:
            with open(filename, "a") as f:
                f.write(f"{working_proxy}\n")
              

        except:
            if prints: print("Waiting for the Threads to Complete.......")
            time.sleep(5) 
            with open(filename, "a") as f:
                f.write(f"{working_proxy}\n")
    print(f"Upladted all the proxies in {filename}")   

def generate_tts_url(query: str, voice: int = 0, filename: str = filename, prints: bool = False) -> None:
    """
    This function generates a Text-to-Speech (TTS) URL using a working proxy retrieved from a file.

    Parameters:
    - query (str): The text to be converted to speech.
    - voice (int): The index of the voice to be used for the TTS. Defaults to 0.
    - filename (str): The name of the file containing the working proxies. Defaults to "available_working_proxies.txt".
    - prints (bool): A flag indicating whether to print progress messages. Defaults to False.

    Returns:
    - None: The function does not return anything; it generates the TTS URL.
    """

    if prints: print(f"Getting the working proxies from {filename}......")
    with open(filename, 'r') as f:
        working_proxies = f.read().split("\n")[:-1]
    if prints: print("Scraped all the working proxies")

    # URL to request
    url = 'https://ttsmp3.com/makemp3_ai.php'
    voices = ["alloy", "echo", "fable", "oynx", "nova", "shimmer"]

    # Event to signal if a response has been received
    response_event = threading.Event()
    extracted_url_ = "None"

    # Lock to control access to response_received
    lock = threading.Lock()

    # Shared variable to indicate if a response has been received
    response_received = False


    # Function to make request with a given proxy
    def make_request(proxy):
        # global response_received, extracted_url_
        nonlocal response_received, extracted_url_
        start = time.time()
        payload = {
            "msg": query,
            "lang": voices[voice],
            "speed": "1.00",
            "source": "ttsmp3"
        }
        try:
            # Send the POST request with the specified proxy
            response = requests.post(url, data=payload, proxies={'http': proxy, 'https': proxy})
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse JSON response
                data = response.json()
                # Extract URL
                extracted_url = data["URL"]
                with lock:
                    if not response_received:
                        print(f"Proxy {proxy} ({round(time.time()-start, 2)} sec) finished first with URL: {extracted_url}")
                        extracted_url_ = extracted_url
                        response_received = True
                        # Set the event to indicate a response has been received
                        response_event.set()
        except:
            pass
        # print(f"Error with proxy {proxy}: {e}")

    # To randomly take out five elements from the list of proxies
    # random_proxies = random.sample(working_proxies, 5)
        
    # Otherwise with all threads
    random_proxies = working_proxies

    threads = []

    if prints: print(f"Requesting URL with {len(random_proxies)} proxies. Waiting for the first thread to complete.........")
    # Create and start a thread for each proxy
    for proxy in random_proxies:
        thread = threading.Thread(target=make_request, args=(proxy,))
        thread.start()
        threads.append(thread)

    # Wait for the event to be set or all threads to finish
    response_event.wait()

    # If the event is set, terminate all threads
    for thread in threads:
        if thread.is_alive():
            thread.join(timeout=0)
        
    if prints: print("All requests completed or terminated. and extracted URL is", extracted_url_)
    return extracted_url_

def download_audio_speech(extracted_url_: str, prints: bool = False) -> str:
    """
    This function downloads audio from the provided URL and saves it locally.

    Parameters:
    - extracted_url_ (str): The URL from which to download the audio file.
    - prints (bool): A flag indicating whether to print progress messages. Defaults to False.

    Returns:
    - str: The name of the downloaded audio file.
    """

    if prints: print("Requesting the audio url to download the audio")
    # Download file
    response = requests.get(extracted_url_)

    # Get file name from URL
    file_name = "ASSETS/" + os.path.basename(extracted_url_)

    # Save file to current folder
    with open(file_name, "wb") as file:
        file.write(response.content)

    if prints: print(f"File '{file_name}' downloaded successfully!")

    return file_name

def get_proxies_periodic(periodic_time: int = 30) -> None:
    """
    This function periodically retrieves proxies using the get_proxies() function at specified intervals.

    Parameters:
    - periodic_time (int): The time interval in seconds between each call to get_proxies(). Defaults to 30.

    Returns:
    - None: The function continuously retrieves proxies at regular intervals.
    """

    while True:
        get_proxies()  # Call the get_proxies() function
        time.sleep(periodic_time)  # Sleep for 30 seconds

def speak(query: str, voice: int = 0) -> None:
    """
    This function converts text to speech (TTS) for the given query using a specified voice, downloads the audio, and plays it.

    Parameters:
    - query (str): The text to be converted to speech.
    - voice (int): The index of the voice to be used for the TTS. Defaults to 0.

    Returns:
    - None: The function does not return anything; it plays the generated speech.
    """
    
    request_run = time.time()
    audio_url = generate_tts_url(query, voice=voice)
    filename = download_audio_speech(audio_url)
    final = time.time()

    print(f"Request TTS Time taken : {final-request_run}\n\n")

    playsound(filename)
    os.remove(filename)

def initiate_proxies() -> None:
    """
    This function initiates the speech synthesis engine.

    Returns:
    - None: The function does not return anything.
    """
    print("Initiating...")
    get_proxies()

    # Start a separate thread for running get_proxies() periodically
    proxies_thread = threading.Thread(target=lambda:get_proxies_periodic(periodic_time=30))
    proxies_thread.daemon = True  # Set the thread as a daemon so it stops when the main program exits
    proxies_thread.start()

if __name__ == "__main__":
    initiate_proxies()
    while True:
        input("Press Enter to continue...")
        speak("Wow! Did you see that? The magician pulled a rabbit out of an empty hat! How in the world did he do that? I'm totally blown away!")
    # speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this")
    # speak("Guess what? I just got the promotion I've been waiting for! I'm over the moon right now, and I can't wait to celebrate this weekend!")
    # speak("There's a storm coming, and the wind is howling like I've never heard before. I'm all alone at home, and every creak and groan of the house is making my heart race.")