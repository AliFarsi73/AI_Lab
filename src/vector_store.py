from pathlib import Path
import chromadb
from pypdf import PdfReader

client = chromadb.PersistentClient(path="../db")

collection = client.get_or_create_collection(
    name="company_docs"
)

base_path = Path(__file__).resolve().parent.parent
docs_path = base_path / "data" / "documents"

for file in docs_path.iterdir():

    if file.suffix == ".txt":

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

    elif file.suffix == ".pdf":

        reader = PdfReader(file)

        content = ""

        for page in reader.pages:
            content += page.extract_text() + "\n"

    else:
        continue

    collection.upsert(
        documents=[content],
        ids=[file.stem]
    )

    print(f"Added: {file.name}")

print("Done!")
