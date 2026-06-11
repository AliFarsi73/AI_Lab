import chromadb
from google import genai

from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ChromaDB
db = chromadb.PersistentClient(path="../db")
collection = db.get_collection("company_docs")

# User question
question = input("Ask a question: ")

# Search relevant document
results = collection.query(
    query_texts=[question],
    n_results=1
)

document = results["documents"][0][0]

print("\nRelevant document found:\n")
print(document)

# Ask Gemini
prompt = f"""
You are a helpful IT assistant.

Answer the user's question in German.
Do not copy the documentation word by word.
Rewrite it as a clear and short answer.
Use ONLY the information from the documentation.
If the documentation does not contain enough information, say:
"Ich habe dazu keine ausreichenden Informationen in der Dokumentation gefunden."

Question:
{question}

Documentation:
{document}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\nAnswer:\n")
print(response.text)