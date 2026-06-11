from dotenv import load_dotenv
from pathlib import Path
import os

from google import genai

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello to Mohammad Ali."
)

print(response.text)