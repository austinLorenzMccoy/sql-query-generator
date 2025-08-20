#!/usr/bin/env python3
"""
Simple demo commands to exercise the FastAPI backend.
Run the server first:

  uvicorn app.main:app --reload --port 8000

Then run:

  python backend/api_demo.py
"""
import subprocess

BASE = "http://127.0.0.1:8000/api/v1"


def run(cmd: list[str]):
    print("$", " ".join(cmd))
    out = subprocess.run(cmd, capture_output=True, text=True)
    print(out.stdout or out.stderr)


if __name__ == "__main__":
    run(["curl", f"{BASE}/health"])  # Health
    run(["curl", f"{BASE}/students"])  # List students
    run(["curl", "-X", "POST", f"{BASE}/sql", "-H", "Content-Type: application/json", "-d", '{"sql":"SELECT COUNT(*) FROM STUDENT;"}'])
    run(["curl", "-X", "POST", f"{BASE}/nl2sql", "-H", "Content-Type: application/json", "-d", '{"question":"How many entries of records are present?"}'])
