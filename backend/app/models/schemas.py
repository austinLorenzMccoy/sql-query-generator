from pydantic import BaseModel, Field
from typing import List, Any


class NLQuery(BaseModel):
    question: str = Field(..., description="English question to convert to SQL")


class SQLQuery(BaseModel):
    sql: str = Field(..., description="SQL query to execute")


class QueryResult(BaseModel):
    rows: List[List[Any]]


class Student(BaseModel):
    name: str
    class_name: str
    section: str
    marks: int
