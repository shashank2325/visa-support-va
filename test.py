import json

with open("combined_corpus.json", "r", encoding="utf-8") as file:
    corpus = json.load(file)


keyword = " visa"
results = [doc for doc in corpus if keyword.lower() in doc["content"].lower()]

# Display results
for result in results:
    print(f"Source: {result['source']}")
    print(f"Excerpt: {result['content'][:500]}\n")
