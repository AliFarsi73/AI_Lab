from pathlib import Path

docs_path = Path("../data/documents")

print("Documents found:")
print("-" * 30)

for file in docs_path.glob("*.txt"):
    print(file.name)

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    print(content)
    print("-" * 30)