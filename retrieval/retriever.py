from retrieval.basic_rag import basic_rag


def retrieve(query: str, k: int = 5) -> list[dict[str, object]]:
    hits = basic_rag(query, k=k)

    return [
        {
            "text": hit["text"],
            "chapter": hit["chapter"],
            "chunk_index": hit["chunk_index"],
            "score": round(1 - hit["distance"], 4),
        }
        for hit in hits
    ]


if __name__ == "__main__":
    vague_queries = [
        "what's a node again?",
        "i don't get louvain communities",
        "how do networks grow?",
        "what is the difference between averaging the mean of communities of their sum vs. averaging the community groups?",
        "why do some nodes have more connections? what do these communities mean?",
        "what makes a network robust?",
        "for a very large network, how to determine if it is bipartite given only the network graph file and nothing else?",
    ]

    for query in vague_queries:
        print(f"\nQuery: {query}")
        hits = retrieve(query)

        for i, hit in enumerate(hits):
            print(f"[{i+1}] Chapter {hit['chapter']} | score: {hit['score']} | chunk: {hit['chunk_index']}")
            print(hit["text"][:200] + "\n")