import re
import chromadb
from config import CHROMA_PATH

chroma_path: str | None = CHROMA_PATH

client: chromadb.ClientAPI = chromadb.PersistentClient(path=chroma_path)
collection: chromadb.Collection = client.get_collection("network_science")

print(f"Total chunks: {collection.count()}")

sample = collection.peek(5)

for i, (doc, meta) in enumerate(zip(sample["documents"], sample["metadatas"])):
  clean = re.sub(r'[-]', '', doc)
  clean = re.sub(r'\s+', ' ', clean).strip()
  print(f"Chunk {i} - Chapter {meta['chapter']}")
  print(clean[:300].strip())
  print()