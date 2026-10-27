import os

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pypdf import PdfReader

PDF_PATH = "data/vidhika_resume_2026.pdf"
CHUNK_SIZE = 500
OVERLAP = 100
EMBED_MODEL = "gemini-embedding-001"
TOP_K = 3

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


#verlapped fixed size chunking as 02, wrapped in a function (can be reused)
def load_chunks(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    chunks = []
    current = []
    for line in lines:
        current_len = sum(len(l) + 1 for l in current)
        if current and current_len + len(line) > CHUNK_SIZE:
            chunks.append("\n".join(current))
            overlap_lines = []
            overlap_len = 0
            for prev in reversed(current):
                if overlap_len + len(prev) > OVERLAP:
                    break
                overlap_lines.insert(0, prev)
                overlap_len += len(prev) + 1
            current = overlap_lines
        current.append(line)
    if current:
        chunks.append("\n".join(current))
    return chunks


# Turn a list of texts into a matrix of embeddings (one row per text)
# task_type tells Gemini whether these are documents to store or a question to search with
def embed(texts, task_type):
    result = client.models.embed_content(
        model=EMBED_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(task_type=task_type),
    )
    return np.array([e.values for e in result.embeddings])


# Cosine similarity: 1 = same meaning, 0 = unrelated
def cosine_similarity(query_vec, doc_matrix):
    query_norm = query_vec / np.linalg.norm(query_vec)
    doc_norms = doc_matrix / np.linalg.norm(doc_matrix, axis=1, keepdims=True)
    return doc_norms @ query_norm


# Step 1: chunk the resume and embed every chunk once
chunks = load_chunks(PDF_PATH)
chunk_vectors = embed(chunks, "RETRIEVAL_DOCUMENT")
print(f"Embedded {len(chunks)} chunks, each is a vector of {chunk_vectors.shape[1]} numbers\n")

# Step 2: ask questions, embed each one, and show the closest chunks
while True:
    question = input("Ask about Vidhika (or 'quit'): ")
    # print(question)
    # print(type(question))
    # print([question])
    # print(type([question]))
    if question.lower() == "quit":
        break

    query_vector = embed([question], "RETRIEVAL_QUERY")[0]
    scores = cosine_similarity(query_vector, chunk_vectors)
    top_indices = np.argsort(scores)[::-1][:TOP_K]

    for rank, i in enumerate(top_indices, start=1):
        print(f"\n--- #{rank}  chunk {i}  (score {scores[i]:.3f}) ---")
        print(chunks[i][:300])
    print()
