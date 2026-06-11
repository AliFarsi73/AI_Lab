from pathlib import Path
import chromadb

client = chromadb.PersistentClient(path="../db")

collection = client.get_or_create_collection(
    name="company_docs"
)

base_path = Path(__file__).resolve().parent.parent
docs_path = base_path / "data" / "documents"

for file in docs_path.glob("*.txt"):

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    collection.add(
        documents=[content],
        ids=[file.stem]
    )

    print(f"Added: {file.name}")

print("Done!")
