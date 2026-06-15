import chromadb
from google import genai

from dotenv import load_dotenv
from pathlib import Path
import os

# -----------------------------
# Paths
# -----------------------------
base_path = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(base_path / ".env")

# -----------------------------
# Gemini
# -----------------------------
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------
# ChromaDB
# -----------------------------
db_path = base_path / "db"

db = chromadb.PersistentClient(
    path=str(db_path)
)

collection = db.get_collection("company_docs")

# -----------------------------
# User Question
# -----------------------------
question = input("Ask a question: ")

# -----------------------------
# Search
# -----------------------------
results = collection.query(
    query_texts=[question],
    n_results=3
)

documents = results["documents"][0]
metadatas = results["metadatas"][0]

# -----------------------------
# Show retrieved chunks
# -----------------------------
print("\nRelevant chunks found:\n")

for i, metadata in enumerate(metadatas):
    print(
        f"{i+1}. "
        f"{metadata['source']} "
        f"(chunk {metadata['chunk']})"
    )

# -----------------------------
# Build Context
# -----------------------------
context = "\n\n".join(documents)

prompt = f"""
You are a helpful IT assistant.

Answer the user's question in English.

Do not copy the documentation word by word.

Rewrite the answer in a short and clear way.

Use ONLY the information from the provided documentation.

If the documentation does not contain enough information, answer exactly:

Ich habe dazu keine ausreichenden Informationen in der Dokumentation gefunden.

Question:
{question}

Documentation:
{context}
"""

# -----------------------------
# Gemini Answer
# -----------------------------
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt
)

# -----------------------------
# Output
# -----------------------------
print("\nAnswer:\n")
print(response.text)

print("\nSources:")

for source in sorted(
    set(metadata["source"] for metadata in metadatas)
):
    print("-", source)