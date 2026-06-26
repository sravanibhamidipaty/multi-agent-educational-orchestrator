import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_PATH

chroma_path = CHROMA_PATH

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
client = chromadb.PersistentClient(path=chroma_path)
collection = client.get_collection("network_science")


def basic_rag(query: str, k: int = 5) -> list[dict[str, object]]:
    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    return [
        {
            "text": doc,
            "chapter": meta["chapter"],
            "chunk_index": meta["chunk_index"],
            "distance": dist,
        }

        for doc, meta, dist in zip(
            results["documents"][0], results["metadatas"][0], results["distances"][0]
        )
    ]


if __name__ == "__main__":
    test_queries = [
        "What is a node in a network?",
        "How does the scale-free network form?",
        "What is the clustering coefficient?",
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        hits = basic_rag(query)

        for i, hit in enumerate(hits):
            print(f"[{i + 1}] Chapter {hit['chapter']} | distance: {hit['distance']:.4f}")
            print(hit["text"][:200] + "\n")