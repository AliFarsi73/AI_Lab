from pathlib import Path
import chromadb
from pypdf import PdfReader
from docx import Document


def split_text(text, chunk_size=800):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


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
            page_text = page.extract_text()

            if page_text:
                content += page_text + "\n"

    elif file.suffix == ".docx":

        doc = Document(file)

        content = ""

        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"

    else:
        continue

    chunks = split_text(content)

    for index, chunk in enumerate(chunks):
        collection.upsert(
            documents=[chunk],
            ids=[f"{file.stem}_chunk_{index}"],
            metadatas=[{
                "source": file.name,
                "chunk": index
            }]
        )

    print(f"Added: {file.name} ({len(chunks)} chunks)")

print("Done!")