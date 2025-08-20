from ..core.config import get_settings

try:
    from groq import Groq  # type: ignore
except Exception:  # pragma: no cover - optional at runtime
    Groq = None


def _ensure_configured():
    settings = get_settings()
    if Groq is None:
        raise RuntimeError("groq is not installed. Add it to dependencies.")
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Set it in your environment or .env file.")


def generate_sql(question: str) -> str:
    settings = get_settings()
    _ensure_configured()
    client = Groq(api_key=settings.groq_api_key)
    system_prompt = (
        "You are an expert in converting English questions to SQL queries. "
        "The SQLite table is STUDENT with columns NAME, CLASS, SECTION, MARKS. "
        "Return only the SQL query ending with a semicolon, no markdown or explanation."
    )
    # Groq uses OpenAI-compatible chat completions
    resp = client.chat.completions.create(
        model=settings.groq_model,
        temperature=0.0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    content = resp.choices[0].message.content if resp.choices else ""
    return content or ""
