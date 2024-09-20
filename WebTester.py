from TOOLS.Web_Results import fetch_search_results
from BRAIN.AI.TEXT.API.openGPT import generate

example_query: str = "When is IPL 2024 starting and ending. How much money is spent on the elections 2024 in India. What are the latest COVID-19 statistics in the United States. What is the current stock price of Tesla. What are the recent advancements in AI technology. What is the weather forecast for New York City tomorrow. Who won the Nobel Prize in Literature in 2023."

formatted_output = fetch_search_results(example_query, verbose=True, search_engine='duckduckgo', format_output=True)
print("\n\n")
response = generate([{"role": "user", "content": formatted_output}], stream=True)
