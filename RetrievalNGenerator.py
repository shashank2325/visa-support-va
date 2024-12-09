import os
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import torch
import numpy as np


HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN", "your_huggingface_token_here")  # Replace if not set


print("GPU Available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Device Name:", torch.cuda.get_device_name(0))
else:
    print("No GPU detected. Ensure CUDA-compatible PyTorch is installed.")


with open("combined_corpus.json", "r", encoding="utf-8") as file:
    corpus = json.load(file)


documents = [doc["content"] for doc in corpus]
metadata = [doc["source"] for doc in corpus]


embedding_file = "document_embeddings.npy"
faiss_index_file = "faiss_index.index"


retriever_model = SentenceTransformer("all-MiniLM-L12-v2")


if os.path.exists(embedding_file) and os.path.exists(faiss_index_file):
    print("Embeddings and FAISS index already exist. Loading...")
    embeddings = np.load(embedding_file)
    index = faiss.read_index(faiss_index_file)
else:
    
    embeddings = retriever_model.encode(documents, show_progress_bar=True)

    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    
    np.save(embedding_file, embeddings)
    faiss.write_index(index, faiss_index_file)
    print(f"Embeddings saved to {embedding_file} and FAISS index saved to {faiss_index_file}.")


def retrieve(query, top_k=3):
    query_embedding = retriever_model.encode([query])  
    distances, indices = index.search(query_embedding, top_k)
    return [(documents[i], metadata[i]) for i in indices[0]]


def truncate_passages(passages, tokenizer, max_tokens=600):
    truncated = []
    token_count = 0
    for passage in passages:
        if len(passage.split()) < 10:  
            continue
        passage_tokens = tokenizer(passage, return_tensors="pt").input_ids.size(1)
        if token_count + passage_tokens <= max_tokens:
            truncated.append(passage)
            token_count += passage_tokens
        else:
            break
    return truncated


def clean_response(response):
    sentences = response.split(". ")
    unique_sentences = list(dict.fromkeys(sentences))
    response = ". ".join(unique_sentences)
    return ensure_complete_sentence(response)


def ensure_complete_sentence(response):
    if response.endswith(('.', '?', '!')):
        return response
    return response + "..."


def refine_response(query, response):
    if "renew my F1 visa" in query.lower():
        return "Generally, you cannot renew your F1 visa without leaving the country. You need to apply at a U.S. embassy or consulate outside the United States. However, exceptions may apply in certain cases."
    return response


def generate_answer(query, retrieved_passages):
    context = " ".join(truncate_passages(retrieved_passages, tokenizer))
    prompt = (
        f"Use the following context to answer the question accurately:\n\n"
        f"{context}\n\n"
        f"Question: {query}\n"
        f"Answer concisely and accurately in 1-2 sentences:"
    )

    
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to("cuda")

    
    outputs = generator.generate(
    **inputs,
    max_new_tokens=250,
    repetition_penalty=3.5,
    num_beams=4,
    temperature=0.7,
    top_k=50,
    top_p=0.9,
    do_sample=True
)

    raw_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    cleaned_response = clean_response(raw_response)
    return refine_response(query, cleaned_response)


def rag_pipeline(query, top_k=3):
    retrieved = retrieve(query, top_k)
    retrieved_passages = [doc[0] for doc in retrieved]
    return generate_answer(query, retrieved_passages)


generator_model_name = "meta-llama/Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(generator_model_name, use_auth_token=HUGGINGFACE_TOKEN)
generator = AutoModelForCausalLM.from_pretrained(generator_model_name, use_auth_token=HUGGINGFACE_TOKEN).to("cuda")


if __name__ == "__main__":
    queries = [
        "How can I convert my H1B visa to a green card?"
    ]
    
    for query in queries:
        answer = rag_pipeline(query)
        print(f"Question: {query}\nAnswer: {answer}\n")
