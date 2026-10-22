import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

api_key = os.getenv("GEMINI_API_KEY", "").strip()
model_name = os.getenv("GEMINI_MODEL", "").strip()

if not api_key or not model_name:
    raise SystemExit(
        "Set GEMINI_API_KEY and GEMINI_MODEL in Task-3/.env."
    )

print(f"Testing model: {model_name}")
print("Your API key will not be displayed.")

with genai.Client(
    api_key=api_key,
    http_options={"timeout": 60000},
) as client:
    try:
        print("\nChecking available content-generation models...")

        available_models = []

        for model in client.models.list():
            if "generateContent" in (model.supported_actions or []):
                name = (model.name or "").removeprefix("models/")
                available_models.append(name)

        print("\nAvailable model names:")
        for name in available_models:
            print(f"  {name}")

        print(f"\nSending a minimal request to {model_name}...")

        response = client.models.generate_content(
            model=model_name,
            contents="Reply with only: Connection successful",
        )

        print("\nResponse:")
        print(response.text)

    except errors.APIError as exc:
        print(f"\nAPI error code: {exc.code}")
        print(f"Details: {exc}")

    except Exception as exc:
        print(f"\nError: {type(exc).__name__}: {exc}")