from src.compose_prompt import compose_prompt
from src.async_call_sql_endpoint import get_most_consistent_query_result
from src.async_generate_sql_queries import get_most_common_ai_generated_sql_queries

def ai_translate_question_to_sql(question) -> str:
    # Step 1: Compose a prompt using similar queries
    prompt = compose_prompt(question)
    # Step 2: Generate multiple SQL queries
    sql_queries = get_most_common_ai_generated_sql_queries(prompt)
    # Step 3: Identifying and returning the most consistent result
    sql_query, query_result = get_most_consistent_query_result(sql_queries)
    
    return {"sql_query": sql_query, "query_result": query_result}
    