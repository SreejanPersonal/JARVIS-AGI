import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_proxies(filename: str = "ASSETS/available_working_proxies.txt", number_of_proxies: int = 100, verbose: bool = False,
                max_workers: int = 100, timeout: int = 2,) -> None:
    """
    Fetches proxies, checks validity concurrently, and stores them sorted by response time.

    Args:
        filename (str, optional): File for storing proxies. Defaults to "available_working_proxies.txt".
        number_of_proxies (int, optional): Number of proxies to fetch. Defaults to 100.
        verbose (bool, optional): Verbosity flag. Defaults to False.
        max_workers (int, optional): Maximum concurrent worker threads. Defaults to 100.
        timeout (int, optional): Proxy check timeout in seconds. Defaults to 2.
    """
    start_time = time.perf_counter()

    if verbose:
        print("Fetching proxies...")

    # Fetch proxies only once
    resp = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
    proxies = [proxy.strip() for proxy in resp.text.strip().split("\n")[:number_of_proxies] if proxy.strip()]

    working_proxies = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_proxy, proxy, timeout): proxy for proxy in proxies}

        for future in as_completed(futures):
            result = future.result()
            if result:
                working_proxies.append(result)

    working_proxies.sort(key=lambda x: x[1])

    if verbose:
        print(f"Found {len(working_proxies)} working proxies out of {len(proxies)}")
        print(f"Working Proxies Percentage: {round(len(working_proxies) / len(proxies) * 100)}%")
        print(f"Storing proxies in {filename}...")

    with open(filename, "w") as f:
        f.writelines(f"{proxy}\n" for proxy, _ in working_proxies)

    total_time = time.perf_counter() - start_time

    if verbose:
        print(f"Updated all proxies in {filename}")
        print(f"Total execution time: {total_time:.2f} seconds")

def check_proxy(proxy, timeout):
    start_time = time.perf_counter()
    try:
        with requests.Session() as session:
            response = session.head("https://www.google.com/", proxies={'http': proxy, 'https': proxy}, timeout=timeout)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            if response.status_code == 200 and elapsed_time <= timeout:
                print(f"{proxy} - Time taken: {elapsed_time:.2f} seconds")
                return proxy, elapsed_time
    except Exception:
        return None

if __name__ == "__main__":
    start = time.perf_counter()
    get_proxies(verbose=True)
    print(f"Total time taken: {time.perf_counter() - start:.2f} seconds")