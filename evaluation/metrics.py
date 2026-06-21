from retrieval.basic_rag import basic_rag
from retrieval.hyde_rag import hyde

ACCURATE_DATA = [
    {"query": "What is a node in a network?", "relevant_chapter": 2},
    {"query": "How does the scale-free network form?", "relevant_chapter": 5},
    {"query": "What is the clustering coefficient?", "relevant_chapter": 2},
    {"query": "What is preferential attachment?", "relevant_chapter": 5},
    {"query": "What is a random network?", "relevant_chapter": 3},
    {"query": "What is the small world phenomenon?", "relevant_chapter": 3},
    {"query": "What is a power law degree distribution?", "relevant_chapter": 4},
    {"query": "What is network robustness?", "relevant_chapter": 8},
]


def top_k(hits, relevant_chapter, k):
    def top_k_accuracy(hits, relevant_chapter, k):
        return int(any(h["chapter"] == relevant_chapter for h in hits[:k]))

    def recall_at_k(hits, relevant_chapter, k):
        retrieved = sum(1 for h in hits[:k] if h["chapter"] == relevant_chapter)
        return retrieved / k

    def ndcg_at_1(hits, relevant_chapter):
        if hits and hits[0]["chapter"] == relevant_chapter:
            return 1.0
        return 0.0

    def evaluate(retriever_fn, label):
        top1, top3, top5, recalls, ndcgs = [], [], [], [], []

        for item in ACCURATE_DATA:
            query = item["query"]
            relevant_chapter = item["relevant_chapter"]

            result = retriever_fn(query)
            hits = result["hits"] if isinstance(result, dict) else result

            top1.append(top_k_accuracy(hits, relevant_chapter, k=1))
            top3.append(top_k_accuracy(hits, relevant_chapter, k=3))
            top5.append(top_k_accuracy(hits, relevant_chapter, k=5))
            recalls.append(recall_at_k(hits, relevant_chapter, k=5))
            ndcgs.append(ndcg_at_1(hits, relevant_chapter))

        n = len(ACCURATE_DATA)
        print(f"\n{'=' * 40}")
        print(f"Retriever: {label}")
        print(f"{'=' * 40}")
        print(f"Top-1 Accuracy : {sum(top1) / n:.2f}")
        print(f"Top-3 Accuracy : {sum(top3) / n:.2f}")
        print(f"Top-5 Accuracy : {sum(top5) / n:.2f}")
        print(f"Recall@5       : {sum(recalls) / n:.2f}")
        print(f"nDCG@1         : {sum(ndcgs) / n:.2f}")

    if __name__ == "__main__":
        evaluate(basic_rag, "Plain RAG")
        evaluate(hyde, "HyDE")