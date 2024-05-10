"""
Author: NetHyTech (Anubhav Chaturvedi)
Project: Speech to Text Listener
Description: A Python script that uses Selenium to interact with a website and listen to user input.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class SpeechToTextListener:
    """
    Class responsible for listening to user input on a website using Selenium.
    """

    def __init__(self):
        """
        Initializes the SpeechToTextListener instance with Chrome options and driver.
        """
        self.chrome_options = self.configure_chrome_options()
        self.driver = self.configure_chrome_driver(self.chrome_options)
        self.website_url = self.get_website_url()
        print("Made with ❤️ @DevsDoCode")

    def configure_chrome_options(self):
        """
        Configures Chrome options for headless mode and fake UI for media stream.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        chrome_options.add_argument("--headless=new")
        return chrome_options

    def configure_chrome_driver(self, chrome_options):
        """
        Configures the Chrome driver with the specified options.
        """
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def get_website_url(self):
        """
        Returns the URL of the website to interact with.
        """
        return "https://allorizenproject1.netlify.app/"

    def listen(self, prints: bool=False):
        """
        Listens to user input on the website and prints the output.
        """
        try:
            self.driver.get(self.website_url)
            start_button = self.wait_for_element_to_be_clickable(By.ID,'startButton')
            start_button.click()
            print("Listening...")
            output_text = ""
            is_second_click = False
            while True:
                output_element = self.wait_for_element_to_be_present(By.ID, 'output')
                current_text = output_element.text.strip()
                if "Start Listening" in start_button.text and is_second_click:
                    if output_text:
                        is_second_click = False
                elif "Listening..." in start_button.text:
                    is_second_click = True
                if current_text!= output_text:
                    output_text = current_text
                    if prints: print("User:", output_text)
                    return output_text

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print("An error occurred:", e)

    def wait_for_element_to_be_clickable(self, by, identifier):
        """
        Waits for an element to be clickable.
        """
        return WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((by, identifier)))

    def wait_for_element_to_be_present(self, by, identifier):
        """
        Waits for an element to be present.
        """
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, identifier)))


# Usage example
if __name__ == "__main__":
    listener = SpeechToTextListener()
    listener.listen()   