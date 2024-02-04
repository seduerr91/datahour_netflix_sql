import concurrent.futures
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client using API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY environment variable")
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_sql_query_from_prompt(prompt: str) -> str:
    """
    Generate a SQL query from a given prompt using the OpenAI API.
    
    Parameters:
    - prompt (str): The user prompt to be sent to OpenAI.
    
    Returns:
    - str: The generated SQL query, with some basic cleaning applied.
    """
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4-1106-preview",
        temperature=1.1
    )
    sql_query = chat_completion.choices[0].message.content
    cleaned_sql_query = sql_query.replace('`', '').replace('sql\n', '')
    return cleaned_sql_query


def generate_sql_queries_concurrently(prompt: str, num_concurrent_runs: int = 3):
    """
    Generate multiple SQL queries from the same prompt concurrently using OpenAI.
    
    Parameters:
    - prompt (str): The user prompt to be sent to the OpenAI API multiple times.
    - num_concurrent_runs (int): The number of concurrent runs.

    Returns:
    - list: A list containing the generated SQL queries.
    """
    queries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent_runs) as executor:
        future_queries = [executor.submit(generate_sql_query_from_prompt, prompt) for _ in range(num_concurrent_runs)]
        for future in concurrent.futures.as_completed(future_queries):
            try:
                queries.append(future.result())
            except Exception as exc:
                print(f'Exception: {exc} occurred for the current future task.')
    return queries


def get_unique_queries_sorted_by_frequency(queries: list) -> list:
    """
    Find unique SQL queries and sort them by their frequency, descending.

    Parameters:
    - queries (list): A list containing SQL queries.

    Returns:
    - list: A list of unique SQL queries sorted by their frequency and lexicographically.
    """
    query_frequency = {}
    for query in queries:
        normalized_query = " ".join(query.lower().split())
        query_frequency[normalized_query] = query_frequency.get(normalized_query, 0) + 1

    sorted_unique_queries = sorted(query_frequency.items(), key=lambda x: (-x[1], x[0]))
    return [query for query, frequency in sorted_unique_queries]


def get_most_common_ai_generated_sql_queries(prompt: str):
    """
    Generate SQL queries from a prompt and retrieve the most common unique queries.
    
    Parameters:
    - prompt (str): The prompt to generate SQL queries from using the OpenAI API.
    
    Returns:
    - list: The most common unique SQL queries generated from the prompt.
    """
    sql_queries = generate_sql_queries_concurrently(prompt)
    common_unique_sql_queries = get_unique_queries_sorted_by_frequency(sql_queries)
    return common_unique_sql_queries
