from collections import defaultdict
from collections.abc import Callable
from retrieval.basic_rag import basic_rag
from retrieval.hyde_rag import hyde

ACCURATE_DATA: list[dict[str, str | int]] = [
    {"query": "What is a node in a network?", "relevant_chapter": 2},
    {"query": "How does the scale-free network form?", "relevant_chapter": 5},
    {"query": "What is the clustering coefficient?", "relevant_chapter": 2},
    {"query": "What is preferential attachment?", "relevant_chapter": 5},
    {"query": "What is a random network?", "relevant_chapter": 3},
    {"query": "What is the small world phenomenon?", "relevant_chapter": 3},
    {"query": "What is a power law degree distribution?", "relevant_chapter": 4},
    {"query": "What is network robustness?", "relevant_chapter": 8},
    {"query": "How did analyzing web-crawler data reveal a power law instead of a Poisson degree distribution?", "relevant_chapter": 0},
    {"query": "What computer-science problem did Barabási map onto invasion percolation in his first network paper?", "relevant_chapter": 0},
    {"query": "What is a complex system and why can't its behavior be derived from its components alone?", "relevant_chapter": 1},
    {"query": "What is a cascading failure, as illustrated by the 2003 Northeast blackout?", "relevant_chapter": 1},
    {"query": "What two forces, network maps and universality, enabled the emergence of network science?", "relevant_chapter": 1},
    {"query": "What is the difference between network science from graph theory?", "relevant_chapter": 1},
    {"query": "Why is network science described as an empirical, data-driven discipline?", "relevant_chapter": 1},
    {"query": "How is the average degree of an undirected network related to its number of nodes and links?", "relevant_chapter": 2},
    {"query": "What does the degree distribution p_k of a network represent?", "relevant_chapter": 2},
    {"query": "What is the transitivity also known as global clustering coefficient, of a network?", "relevant_chapter": 2},
    {"query": "How are the diameter and characteristic path length of a network defined?", "relevant_chapter": 2},
    {"query": "Why does a random network have a Poisson degree distribution?", "relevant_chapter": 3},
    {"query": "At what average degree does a giant component emerge in a random network?", "relevant_chapter": 3},
    {"query": "What is the connectivity threshold ln(N)/N for a random network to become fully connected?", "relevant_chapter": 3},
    {"query": "What does the degree exponent gamma tell us about a scale-free network?", "relevant_chapter": 4},
    {"query": "Why are hubs present in scale-free networks but effectively forbidden in random networks?", "relevant_chapter": 4},
    {"query": "Why do scale-free networks with gamma below 3 lack a meaningful internal scale?", "relevant_chapter": 4},
    {"query": "How does the configuration model generate a network with a given degree sequence?", "relevant_chapter": 4},
    {"query": "What degree exponent does the Barabási–Albert model predict?", "relevant_chapter": 5},
    {"query": "Why do older nodes become hubs in the Barabási–Albert model (first-mover advantage)?", "relevant_chapter": 5},
    {"query": "Why are both growth and preferential attachment necessary for a scale-free network?", "relevant_chapter": 5},
    {"query": "What is node fitness in the Bianconi–Barabási model?", "relevant_chapter": 6},
    {"query": "How does fitness produce a fit-gets-rich dynamic in evolving networks?", "relevant_chapter": 6},
    {"query": "What does an exponentially bounded fitness distribution imply about how hubs form?", "relevant_chapter": 6},
    {"query": "What is Bose–Einstein condensation, or the winner-takes-all phenomenon, in a network?", "relevant_chapter": 6},
    {"query": "How do initial attractiveness and node deletion change the degree exponent of an evolving network?", "relevant_chapter": 6},
    {"query": "What are degree correlations in a network?", "relevant_chapter": 7},
    {"query": "What is the difference between assortative, neutral, and disassortative networks?", "relevant_chapter": 7},
    {"query": "What is the friendship paradox and why does it depend on the ratio of the second moment to the first moment of the degree distribution?", "relevant_chapter": 7},
    {"query": "How does the degree correlation function k_nn(k) and its exponent classify a network's correlations?", "relevant_chapter": 7},
    {"query": "What is structural disassortativity in simple scale-free networks?", "relevant_chapter": 7},
    {"query": "How does percolation theory describe a network breaking apart under random node removal?", "relevant_chapter": 8},
    {"query": "What is the Molloy–Reed criterion for the existence of a giant component?", "relevant_chapter": 8},
    {"query": "How does the critical breakdown threshold depend on the first and second moments of the degree distribution?", "relevant_chapter": 8},
    {"query": "What distribution do the sizes of cascading failures follow?", "relevant_chapter": 8},
    {"query": "What is a community, defined by the connectedness and density hypotheses?", "relevant_chapter": 9},
    {"query": "What is the difference between a strong community and a weak community?", "relevant_chapter": 9},
    {"query": "How does the Girvan–Newman algorithm use link betweenness to detect communities?", "relevant_chapter": 9},
    {"query": "What does the modularity metric measure for a community partition, and when does merging two communities increase it?", "relevant_chapter": 9},
    {"query": "How does a dendrogram from hierarchical clustering represent a network's community structure?", "relevant_chapter": 9},
    {"query": "How do the SI, SIS, and SIR compartmental models describe epidemic spreading?", "relevant_chapter": 10},
    {"query": "What is the basic reproductive number R0 and how does it predict an epidemic's fate?", "relevant_chapter": 10},
    {"query": "Why does the epidemic threshold vanish on a scale-free network?", "relevant_chapter": 10},
    {"query": "Why are super-spreaders equivalent to hubs in a contact network?", "relevant_chapter": 10},
    {"query": "Why does random immunization fail on scale-free networks while targeting hubs works?", "relevant_chapter": 10},
]


def top_k(hits: list[dict[str, object]], relevant_chapter: int, k: int) -> None:
    def top_k_accuracy(hits: list[dict[str, object]], relevant_chapter: int, k: int) -> int:
        return int(any(h["chapter"] == relevant_chapter for h in hits[:k]))

    def recall_at_k(hits: list[dict[str, object]], relevant_chapter: int, k: int) -> float:
        retrieved = sum(1 for h in hits[:k] if h["chapter"] == relevant_chapter)
        return retrieved / k

    def ndcg_at_1(hits: list[dict[str, object]], relevant_chapter: int) -> float:
        if hits and hits[0]["chapter"] == relevant_chapter:
            return 1.0
        return 0.0

    def evaluate(retriever_fn: Callable[[str], object], label: str) -> None:
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

CHAPTER_NAMES = {
    0: "Personal Intro", 1: "Introduction", 2: "Graph Theory",
    3: "Random Networks", 4: "Scale-Free", 5: "Barabási–Albert",
    6: "Evolving Networks", 7: "Degree Correl.", 8: "Robustness",
    9: "Communities", 10: "Spreading", 11: "Preface/Teaching",
}


def hit_at_k(hits, relevant_chapter, k):
    return int(any(h["chapter"] == relevant_chapter for h in hits[:k]))


def recall5(hits, relevant_chapter):
    return sum(1 for h in hits[:5] if h["chapter"] == relevant_chapter) / 5


def ndcg1(hits, relevant_chapter):
    return 1.0 if hits and hits[0]["chapter"] == relevant_chapter else 0.0


def run_rows(retriever_fn):
    rows = []
    for item in ACCURATE_DATA:
        result = retriever_fn(item["query"])
        hits = result["hits"] if isinstance(result, dict) else result
        c = item["relevant_chapter"]
        rows.append({
            "chapter": c,
            "top1": hit_at_k(hits, c, 1),
            "top3": hit_at_k(hits, c, 3),
            "top5": hit_at_k(hits, c, 5),
            "recall5": recall5(hits, c),
            "ndcg1": ndcg1(hits, c),
        })
    return rows


def overall(rows, label):
    n = len(rows)
    print(f"\n{'=' * 52}")
    print(f"Retriever: {label}  (overall, N={n})")
    print(f"{'=' * 52}")
    print(f"Top-1 Accuracy : {sum(r['top1'] for r in rows) / n:.2f}")
    print(f"Top-3 Accuracy : {sum(r['top3'] for r in rows) / n:.2f}")
    print(f"Top-5 Accuracy : {sum(r['top5'] for r in rows) / n:.2f}")
    print(f"Recall@5       : {sum(r['recall5'] for r in rows) / n:.2f}")
    print(f"nDCG@1         : {sum(r['ndcg1'] for r in rows) / n:.2f}")


def per_chapter(rows, label):
    by_ch = {}
    for r in rows:
        by_ch.setdefault(r["chapter"], []).append(r)
    print(f"\n{'-' * 66}")
    print(f"Per-chapter breakdown: {label}")
    print(f"{'-' * 66}")
    print(f"{'Ch':>2}  {'Topic':<17} {'T@1':>5} {'T@3':>5} {'T@5':>5} {'R@5':>5} {'nDCG@1':>7}")
    for ch in sorted(by_ch):
        g = by_ch[ch]
        m = len(g)
        print(
            f"{ch:>2}  {CHAPTER_NAMES.get(ch, '?'):<17} "
            f"{sum(r['top1'] for r in g) / m:>5.2f} "
            f"{sum(r['top3'] for r in g) / m:>5.2f} "
            f"{sum(r['top5'] for r in g) / m:>5.2f} "
            f"{sum(r['recall5'] for r in g) / m:>5.2f} "
            f"{sum(r['ndcg1'] for r in g) / m:>7.2f}"
        )


def compare(basic_rows, hyde_rows):
    def top5_by_ch(rows):
        acc = {}
        for r in rows:
            acc.setdefault(r["chapter"], []).append(r["top5"])
        return {ch: sum(v) / len(v) for ch, v in acc.items()}

    basic = top5_by_ch(basic_rows)
    hyde_ = top5_by_ch(hyde_rows)
    print(f"\n{'=' * 60}")
    print("HyDE vs Plain RAG — Top-5 accuracy per chapter")
    print(f"{'=' * 60}")
    print(f"{'Ch':>2}  {'Topic':<17} {'Basic':>7} {'HyDE':>7} {'Δ':>7}")
    for ch in sorted(CHAPTER_NAMES):
        b = basic.get(ch, 0.0)
        h = hyde_.get(ch, 0.0)
        print(f"{ch:>2}  {CHAPTER_NAMES[ch]:<17} {b:>7.2f} {h:>7.2f} {h - b:>+7.2f}")
    nb = len(basic_rows)
    print(f"{'-' * 60}")
    print(
        f"{'':>2}  {'OVERALL Top-5':<17} "
        f"{sum(r['top5'] for r in basic_rows) / nb:>7.2f} "
        f"{sum(r['top5'] for r in hyde_rows) / nb:>7.2f} "
        f"{(sum(r['top5'] for r in hyde_rows) - sum(r['top5'] for r in basic_rows)) / nb:>+7.2f}"
    )


if __name__ == "__main__":
    basic_rows = run_rows(basic_rag)
    hyde_rows = run_rows(hyde)
    overall(basic_rows, "Plain RAG")
    per_chapter(basic_rows, "Plain RAG")
    overall(hyde_rows, "HyDE")
    per_chapter(hyde_rows, "HyDE")
    compare(basic_rows, hyde_rows)
