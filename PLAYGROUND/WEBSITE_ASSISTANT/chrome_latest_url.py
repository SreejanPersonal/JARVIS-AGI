import sqlite3
import os
import shutil

def get_latest_chrome_url() -> str:
    """
    Retrieves the URL of the most recent webpage visited in Google Chrome.

    Returns:
        str: The URL of the most recent webpage visited in Google Chrome.
    """
    chrome_history_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\History"
    
    # Destination path for the copy of the history file
    history_db_path = os.path.join(os.getcwd(), "ChromeHistoryCopy.txt")

    # Copy the Chrome history database to a new location
    shutil.copy2(chrome_history_path, history_db_path)

    # Connect to the Chrome history database
    conn = sqlite3.connect(history_db_path)
    cursor = conn.cursor()

    # Execute a query to retrieve the latest URL from the history
    cursor.execute("SELECT url FROM urls ORDER BY last_visit_time DESC LIMIT 1")
    latest_url = cursor.fetchone()[0]

    # Close the connection
    conn.close()
    os.remove(history_db_path)

    print("Latest URL:", latest_url)
    return latest_url


if __name__ == "__main__":
    latest_url = get_latest_chrome_url()
