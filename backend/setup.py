from setuptools import setup, find_packages

setup(
    name="text2sql-backend",
    version="1.0.0",
    description="FastAPI backend for Text-to-SQL over SQLite STUDENT table",
    packages=find_packages(include=["app", "app.*"]),
    install_requires=[
        "fastapi>=0.115.0",
        "uvicorn[standard]>=0.30.0",
        "pydantic>=2.7",
        "pydantic-settings>=2.4",
        "python-dotenv>=1.0.1",
        "groq>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0",
            "pytest-cov>=5.0",
            "httpx>=0.27",
            "ruff>=0.5.0",
        ]
    },
)
