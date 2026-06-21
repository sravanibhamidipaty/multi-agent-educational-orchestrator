import re
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
from config import TEXT_DIR, CHROMA_PATH

text_directory = TEXT_DIR
chromadb_path = CHROMA_PATH

def clean_text(text):
    text = re.sub(r"\d+/\d+/\d+,\s+\d+:\d+\s+[AP]M\s+Chapter.+\n", "", text)
    text = re.sub(r"https?://\S+\s+\d+/\d+\n", "", text)
    text = re.sub(r"Image \d+\.\d+\n.*?\n", "", text, flags=re.DOTALL)
    text = re.sub(r"Section \d+\.\d+\s*\nBibliography.*", "", text, flags=re.DOTALL)
    text = re.sub(r"^Network Science\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^by Albert-László Barabási\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

client = chromadb.PersistentClient(path=chromadb_path)

try:
      client.delete_collection("network_science")
      print("Deleted old collection")
except:
  pass

collection = client.get_or_create_collection(name="network_science")

splitter = RecursiveCharacterTextSplitter(chunk_size=500 * 4, chunk_overlap=100 * 4, length_function=len)

for filename in sorted(os.listdir(text_directory)):
    chapter_number = filename.replace("chapter_", "").replace(".txt", "")

    with open(os.path.join(text_directory, filename)) as f:
        text = clean_text(f.read())

    chunks = splitter.split_text(text)
    cleaned_chunks = []

    for chunk in chunks:
        chunk = re.sub(r'(?m)^Network Science[^\n]*\n+', '', chunk)
        chunk = re.sub(r'\n{3,}', '\n\n', chunk)
        chunk = chunk.strip()

        if len(chunk) > 100:
            cleaned_chunks.append(chunk)

    chunks = cleaned_chunks
    embeddings = model.encode(chunks).tolist()

    ids = [f"ch{chapter_number}_chunk{i}" for i in range(len(chunks))]
    metadatas = [{"chapter": int(chapter_number), "chunk_index": i} for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)
    print(f"Chapter {chapter_number}: {len(chunks)} chunks")

print(f"Total chunks in collection: {collection.count()}")