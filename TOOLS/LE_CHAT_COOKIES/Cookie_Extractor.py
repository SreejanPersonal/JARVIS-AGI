from selenium import webdriver
import posixpath
import os
from typing import Optional, Dict

# print(os.path.join(os.getcwd(), "ASSETS/USERDATA/LE CHAT").replace(os.sep, '/'))
# print(posixpath.normpath(os.path.join(os.getcwd(), "ASSETS/USERDATA/LE CHAT").replace(os.sep, '/')))

def get_ory_session_cookie(profile_path: str = posixpath.normpath(os.path.join(os.getcwd(), "ASSETS/USERDATA/LE CHAT").replace(os.sep, '/')), 
                           verbose: bool = True) -> Optional[Dict[str, str]]:
    """
    Opens a Chrome webdriver with the specified profile and retrieves the 'ory_session_coolcurranf83m3srkfl' cookie.

    Args:
        profile_path (str): The path to the Chrome profile directory.
        verbose (bool): Whether to print verbose output during execution. Defaults to True.

    Returns:
        Optional[Dict[str, str]]: The 'ory_session_coolcurranf83m3srkfl' cookie as a dictionary, or None if not found.
    """
    if verbose:
        print(f"\033[94mInitializing Chrome webdriver with profile: {profile_path}\033[0m") 

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_path}")
    options.add_argument('--profile-directory=Default')
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    if verbose:
        print("\033[94mNavigating to https://chat.mistral.ai/\033[0m")
    
    driver.get("https://chat.mistral.ai/")

    if verbose:
        print("\033[94mRetrieving cookies...\033[0m")
    
    cookies = driver.get_cookies()
    driver.quit()

    for cookie in cookies:
        if verbose:
            print(f"\033[94mChecking cookie: {cookie['name']}\033[0m") 
        if cookie['name'] == 'ory_session_coolcurranf83m3srkfl':
            if verbose:
                print(f"\033[92mFound 'ory_session_coolcurranf83m3srkfl' cookie:\033[0m\n\033[93m{cookie}\033[0m")
            if verbose:
                print("\033[94mCookie found successfully!\033[0m")
            return cookie
    
    if verbose:
        print("\033[94mCookie 'ory_session_coolcurranf83m3srkfl' not found.\033[0m")
    
    return None

if __name__ == "__main__":
    ory_session_cookie = get_ory_session_cookie()