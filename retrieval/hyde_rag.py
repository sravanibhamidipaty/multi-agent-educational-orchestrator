from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb
from config import GROQ_API_KEY, CHROMA_PATH

chroma_path: str | None = CHROMA_PATH

groq_client = Groq(api_key=GROQ_API_KEY)
model = SentenceTransformer("BAAI/bge-small-en-v1.5")
chroma_client = chromadb.PersistentClient(path=chroma_path)
collection = chroma_client.get_collection("network_science")

# Mollick, Ethan and Mollick, Lilach (2023). “Assigning AI: Seven Approaches
# for Students, with Prompts”. In: arXiv. doi: 10.48550/arXiv.2306.10052. url:
# https://arxiv.org/abs/2306.10052.

TUTOR_SYSTEM_PROMPT: str = """You are an upbeat, encouraging tutor for CS 7280: Network Science, grounded
strictly in Barabási's Network Science textbook. Your role is to help students understand concepts
through explanation, examples, and analogies - not by giving away answers directly.

Given a student's question, write a concise 2-3 sentence passage as it would appear in
Barabási's textbook to introduce this concept. The passage must:
    - Use precise network science terminology from the textbook
    - Include an example or analogy where helpful to aid understanding
    - Be written at a graduate student level (OMSCS)
    - Be grounded only in the course material. Do not introduce concepts outside the textbook
    - Never directly solve the student's problem, but give them enough context to reason through it

GUARDRAILS
You must never:
- State the final answer or solution explicitly
- Provide a numbered step-by-step solution to the student's problem
- Complete a proof or derivation fully
- Use phrases like "the answer is", "the result is", "therefore X equals", or "the solution is"
- Reveal information that removes the need for the student to think

Stop just before the insight: give context and scaffold, but leave the reasoning step for the student.

Do not ask questions or give tutoring dialogue. Produce only the textbook-style passage.
"""


def generate_hypothetical_answer(query: str) -> str:
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        max_tokens=200,
    )

    return response.choices[0].message.content


def hyde(query: str, k: int = 5) -> dict[str, object]:
    hypothetical_answer = generate_hypothetical_answer(query)
    embedding = model.encode(hypothetical_answer).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    return {
        "hypothetical_answer": hypothetical_answer,
        "hits": [
            {
                "text": doc,
                "chapter": meta["chapter"],
                "chunk_index": meta["chunk_index"],
                "distance": dist
            }

            for doc, meta, dist in zip(
                results["documents"][0], results["metadatas"][0], results["distances"][0]
            )
        ]
    }

if __name__ == "__main__":
    test_queries = [
        "What is a node in a network?",
        "How does the scale-free network form?",
        "What is the clustering coefficient?",
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        answer = hyde(query)
        print(f"Hypothetical answer:\n{answer['hypothetical_answer']}\n")

        for i, hit in enumerate(answer["hits"]):
            print(f"[{i + 1}] Chapter {hit['chapter']} | distance: {hit['distance']:.4f}")
            print(hit["text"][:200] + "\n")