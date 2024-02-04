from pydantic import BaseModel
from typing import List, Any

class Question(BaseModel):
    question: str

class Response(BaseModel):
    sql_query: str
    query_result: List[List[Any]]

