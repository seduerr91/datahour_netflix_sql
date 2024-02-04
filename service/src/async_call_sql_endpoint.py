import concurrent.futures
import sqlite3

DATABASE_URL = "data/databases/netflix.db"

def execute_sql_query(sql_query: str):
    """
    Executes a given SQL query on the SQLite database and returns the result.
    
    Parameters:
    - sql_query (str): The SQL query string to be executed.
    
    Returns:
    - tuple: A tuple of column names and the corresponding rows of the query result.
    
    Raises:
    - RuntimeError: If an unexpected database error occurs.
    """
    try:
        with sqlite3.connect(DATABASE_URL) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return columns, rows
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise RuntimeError("An unexpected error occurred. Please contact support if the problem persists.") from e

def execute_queries_concurrently(queries, num_threads=None):
    """
    Executes a list of SQL queries concurrently.
    
    Parameters:
    - queries (list): A list of SQL query strings to be executed.
    - num_threads (int, optional): The number of threads to be used for concurrent execution. Defaults to the number of queries.
    
    Returns:
    - list: A list of tuples containing the query string and its corresponding query result.
    """
    if num_threads is None:
        num_threads = len(queries)
    query_results_pairs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_query = {executor.submit(execute_sql_query, query): query for query in queries}
        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                query_results_pairs.append((query, future.result()))
            except Exception as exc:
                print(f'Exception: {exc} occurred for query: {query}')
                query_results_pairs.append((query, (None, None)))
    return query_results_pairs

def find_most_consistent_result(query_results_pairs):
    """
    Finds the most consistently occurring result across multiple queries.
    
    Parameters:
    - query_results_pairs (list): A list of tuples containing each query string and its corresponding result.
    
    Returns:
    - tuple: The query and its most consistent result represented as column names and corresponding rows.
    """
    result_frequency = {}
    for query, result_pair in query_results_pairs:
        if result_pair == (None, None):
            print(f"No results for query: {query}")
            continue
        columns, rows = result_pair
        tuple_key = (tuple(columns), tuple(map(tuple, rows)))
        result_frequency.setdefault(tuple_key, {'count': 0, 'query': query})
        result_frequency[tuple_key]['count'] += 1

    most_consistent = max(result_frequency.items(), key=lambda x: x[1]['count'], default=(None, {'query': None}))
    if most_consistent[0] is not None:
        most_consistent_columns, most_consistent_rows = most_consistent[0]
        most_consistent_query = result_frequency[most_consistent[0]]['query']
        return most_consistent_query, (list(most_consistent_columns), list(map(list, most_consistent_rows)))
    return (None, (None, None))

def get_most_consistent_query_result(sql_queries):
    """
    Performs concurrent SQL queries and identifies the most consistent result.
    
    Parameters:
    - sql_queries (list): A list of SQL query strings to be executed concurrently.
    
    Returns:
    - tuple: The most consistent SQL query and its result.
    """
    query_results_pairs = execute_queries_concurrently(sql_queries)
    most_consistent_query, most_consistent_result = find_most_consistent_result(query_results_pairs)
    return most_consistent_query, most_consistent_result