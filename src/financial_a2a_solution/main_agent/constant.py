import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MAX_AGENTS_CALLS = int(os.getenv("MAX_AGENTS_CALLS") or 3)
