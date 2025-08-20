from fastapi import APIRouter, HTTPException
from typing import List

from ...models.schemas import NLQuery, SQLQuery, QueryResult, Student
from ...services import db as db_service
from ...services import nl2sql as nl2sql_service
from ...utils.sql_cleaner import clean_sql_query

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/students", response_model=List[Student])
def list_students() -> List[Student]:
    try:
        rows = db_service.fetch_all("SELECT NAME, CLASS, SECTION, MARKS FROM STUDENT;")
        return [Student(name=r[0], class_name=r[1], section=r[2], marks=r[3]) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sql", response_model=QueryResult)
def run_sql(query: SQLQuery) -> QueryResult:
    try:
        rows = db_service.fetch_all(query.sql)
        return QueryResult(rows=rows)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/nl2sql", response_model=SQLQuery)
def nl_to_sql(payload: NLQuery) -> SQLQuery:
    try:
        raw = nl2sql_service.generate_sql(payload.question)
        cleaned = clean_sql_query(raw)
        return SQLQuery(sql=cleaned)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
