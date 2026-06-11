import chromadb

client = chromadb.PersistentClient(path="../db")

collection = client.get_collection("company_docs")

question = input("Ask a question: ")

results = collection.query(
    query_texts=[question],
    n_results=1
)

print("\nAnswer source:\n")
print(results["documents"][0][0])