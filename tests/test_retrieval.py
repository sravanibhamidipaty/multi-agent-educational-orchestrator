from retrieval.basic_rag import basic_rag
from retrieval.hyde_rag import hyde
import pytest
import chromadb
from typing import Any

ACCURATE_DATA: list[Any] = [
    {"query": "What is a node in a network?", "relevant_chapter": 2},
    # xfail for basic RAG: vocabulary mismatch — raw query lacks textbook terms
    # ("preferential attachment", "Barabási-Albert") that chapter 5 uses.
    # HyDE generates this vocabulary first, which is why it succeeds here.
    pytest.param(
        {"query": "How does the scale-free network form?", "relevant_chapter": 5},
        marks=pytest.mark.xfail(
            reason="Basic RAG vocabulary mismatch: query has no textbook terms",
            strict=False,
        ),
    ),

    {"query": "What is the clustering coefficient?", "relevant_chapter": 2},
    {"query": "What is preferential attachment?", "relevant_chapter": 5},
    {"query": "What is a random network?", "relevant_chapter": 3},
    {"query": "What is the small world phenomenon?", "relevant_chapter": 3},
    {"query": "What is a power law degree distribution?", "relevant_chapter": 4},
    {"query": "What is network robustness?", "relevant_chapter": 8},
]


def test_basic_rag_returns_k_results() -> None:
    assert len(basic_rag("What is a node?", k=5)) == 5


def test_basic_rag_result_has_required_keys() -> None:
    hits = basic_rag("What is a node?", k=5)
    assert {"text", "chapter", "chunk_index", "distance"} == hits[0].keys()


def test_basic_rag_distance_is_positive() -> None:
    hits = basic_rag("What is a node?", k=3)
    assert all(h["distance"] > 0 for h in hits)


def test_basic_rag_results_sorted_by_distance() -> None:
    hits = basic_rag("What is a node?", k=5)
    distances = [h["distance"] for h in hits]
    assert distances == sorted(distances)


def test_hyde_returns_hypothetical_answer() -> None:
    result = hyde("What is a node?", k=3)
    assert "hypothetical_answer" in result
    assert len(result["hypothetical_answer"]) > 20


def test_hyde_guardrail_no_direct_answer() -> None:
    banned = ["the answer is", "the result is", "therefore x equals", "the solution is"]
    result = hyde("What is the clustering coefficient?", k=3)
    answer = result["hypothetical_answer"].lower()

    for phrase in banned:
        assert phrase not in answer, (f"Guardrail failed — found banned phrase: '{phrase}'")

def test_hyde_returns_k_results() -> None:
  result = hyde("What is a node?", k=5)
  assert len(result["hits"]) == 5

def test_hyde_result_has_required_keys() -> None:
    result = hyde("What is a node?", k=1)
    assert {"text", "chapter", "chunk_index", "distance"} == result["hits"][0].keys()

def _id(g: Any) -> str:
    return (g["query"] if isinstance(g, dict) else g.values[0]["query"])[:40]

@pytest.mark.parametrize("item", ACCURATE_DATA, ids=[_id(g) for g in ACCURATE_DATA])
def test_basic_rag_top5_accuracy(item: dict[str, Any]) -> None:
  hits = basic_rag(item["query"], k=5)
  chapters = [h["chapter"] for h in hits]

  assert item["relevant_chapter"] in chapters, (
      f"Expected chapter {item['relevant_chapter']} in top-5, got {chapters}"
  )


@pytest.mark.parametrize("item", ACCURATE_DATA, ids=[_id(g) for g in ACCURATE_DATA])
def test_hyde_top5_accuracy(item: dict[str, Any]) -> None:
  result = hyde(item["query"], k=5)
  chapters = [h["chapter"] for h in result["hits"]]

  assert item["relevant_chapter"] in chapters, (
      f"Expected chapter {item['relevant_chapter']} in top-5, got {chapters}"
  )


@pytest.mark.parametrize("item", ACCURATE_DATA, ids=[_id(g) for g in ACCURATE_DATA])
def test_hyde_beats_basic_rag_best_distance(item: dict[str, Any]) -> None:
  basic_hits = basic_rag(item["query"], k=5)
  hyde_result = hyde(item["query"], k=5)

  best_basic = min(h["distance"] for h in basic_hits)
  best_hyde = min(h["distance"] for h in hyde_result["hits"])

  assert best_hyde < best_basic, (
      f"HyDE ({best_hyde:.4f}) should beat plain RAG ({best_basic:.4f}) "
      f"for: '{item['query']}'"
  )