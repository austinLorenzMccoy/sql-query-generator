import re

def clean_sql_query(raw_response: str) -> str:
    cleaned = re.sub(r"```(?:sql)?\s*", "", raw_response, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()
    if cleaned and not cleaned.endswith(";"):
        cleaned += ";"
    return cleaned
