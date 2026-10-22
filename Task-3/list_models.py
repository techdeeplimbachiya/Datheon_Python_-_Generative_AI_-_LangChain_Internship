import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv(
    Path(__file__).resolve().parent / ".env",
    override=True,
)

with genai.Client(api_key=os.environ["GEMINI_API_KEY"]) as client:
    for model in client.models.list():
        if "generateContent" in (model.supported_actions or []):
            print((model.name or "").removeprefix("models/"))