import requests

def fetch_website_content(search_url: str) -> str:
    """Fetches the content of a webpage.

    Args:
        search_url: The URL of the webpage to fetch.

    Returns:
        The content of the webpage as a string.

    Raises:
        requests.exceptions.RequestException: If there is an error
            making the request.
    """

    jinna_url = "https://r.jina.ai"
    response = requests.get(f"{jinna_url}/{search_url}").text
    print("Fetched the Website content")
    return response

if __name__ == "__main__":
    search_url = "https://www.ndtv.com/india-news/several-maoists-killed-in-encounter-with-security-forces-in-chhattisgarh-5455181"
    response = fetch_website_content(search_url)
    print(response)

# write a code to add 2 numbers
