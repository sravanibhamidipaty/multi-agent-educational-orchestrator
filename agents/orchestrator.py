from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from agents.hint_agent import (
    transform_retrieve,
    narrow_down,
    _passages_to_dicts,
    render_hint,
    decompose,
    next_level,
    MAX_LEVEL,
)
from agents.verification_agent import selfcheck
from agents.faithfulness import source_faithfulness

HALLUCINATION_THRESHOLD: float = 0.5  # SelfCheckGPT: reject hints scoring above this because that is a lot more hallucination than factual content
MAX_STUCK_CYCLES: int = (
    2  # decompositions at the floor before offering a human support advice
)


class TutorState(TypedDict, total=False):
    # Inputs sent per turn (from ChromaDB student-progres memory)
    question: str
    level: int
    prior_hints: list[str]
    subquestion: str
    stuck_cycles: int

    # Outputs produced by agents (shared state passed node -> node)
    context: list[dict]  # retrieval agent output
    hint: str  # hint-generation agent output
    verification: dict  # SelfCheckGPT result
    faithfulness: dict  # source-faithfulness result
    approved: bool
    final_hint: str  # what the student actually sees this turn
    next_level: int  # suggested level for the next turn (handler stores it in memory)
    escalate_to_human: bool
    notes: list[str]


def _active_question(state: TutorState) -> str:
    return state.get("subquestion") or state["question"]


# Agent 1: Retrieval Agent
def retrieval_node(state: TutorState) -> TutorState:
    pool = transform_retrieve(_active_question(state), k=5)
    context_data = narrow_down(
        pool, min_relevance=0.15, top_n=3
    )  # HINTS narrow-down criteria
    return {"context": _passages_to_dicts(context_data)}


# Agent 2: Hint-Generation Agent
def hint_node(state: TutorState) -> TutorState:
    hint = render_hint(
        _active_question(state),
        state["context"],
        level=state.get("level", 1),
        prior_hints=state.get("prior_hints", []),
    )
    return {"hint": hint}


# Agent 3: Verification Agent
def verification_node(state: TutorState) -> TutorState:
    # Check 1: SelfCheckGPT (N=4) -- hallucination via sample divergence
    verification = selfcheck(_active_question(state), state["hint"])
    # Check 2: source-faithfulness -- grounded in retrieved passages, with source + reason logs.
    faithfulness = source_faithfulness(state["hint"], state["context"])

    approved = verification["hallucination_score"] <= HALLUCINATION_THRESHOLD

    return {
        "verification": verification,
        "faithfulness": faithfulness,
        "approved": approved,
        "final_hint": state["hint"]
        if approved
        else "I am not confident enough to hint safely on that yet — try rephrasing your question.",
        "next_level": next_level(state.get("level", 1)),
        "notes": [
            f"level={state.get('level', 1)}",
            f"hallucination={verification['hallucination_score']:.2f} (<= {HALLUCINATION_THRESHOLD}, GATE)",
            f"faithfulness={faithfulness['faithfulness_score']:.2f} (logged, not a gate)",
            "sources: " + ", ".join(c["source"] for c in faithfulness["checks"])],
    }



def stuck_node(state: TutorState) -> TutorState:
    cycles = state.get("stuck_cycles", 0) + 1
    if cycles > MAX_STUCK_CYCLES:
        # Post in Ed Discussion. Human in the loop is needed
        return {
            "approved": True,
            "escalate_to_human": True,
            "stuck_cycles": cycles,
            "final_hint": (
                "Please post this question on Ed Discussion and a TA will take a look at it"
            ),
            "notes": [f"floor reached; escalating to human (cycle {cycles})"],
        }

    # HINTS "student features cycles": decompose to a subquestion
    subquestion = decompose(
        state["question"], state["context"], prior_hints=state.get("prior_hints", [])
    )
    return {
        "approved": True,
        "subquestion": subquestion,
        "next_level": 1,
        "stuck_cycles": cycles,
        "final_hint": (
            "Before we go further -- tell me what you've tried or where your reasoning stops. Let's zoom in on one piece: "
            + subquestion
        ),
        "notes": [f"floor reached; decomposing to sub-question (cycle {cycles})"],
    }


def _route(state: TutorState) -> str:
    return "stuck" if state.get("level", 1) > MAX_LEVEL else "hint"


def build_pipeline():
    graph = StateGraph(TutorState)
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("hint", hint_node)
    graph.add_node("verification", verification_node)
    graph.add_node("stuck", stuck_node)

    graph.add_edge(START, "retrieval")
    graph.add_conditional_edges(
        "retrieval", _route, {"hint": "hint", "stuck": "stuck"}
    )

    graph.add_edge("hint", "verification")
    graph.add_edge("verification", END)
    graph.add_edge("stuck", END)
    return graph.compile()


pipeline = build_pipeline()

if __name__ == "__main__":
    # Turn 1: initial question, Level 1. level and prior_hints come from memory in production
    state = pipeline.invoke(
        {
            "question": "How does the scale-free network form?",
            "level": 1,
            "prior_hints": [],
            "stuck_cycles": 0,
        }
    )
    print(f"approved={state['approved']} next_level={state.get('next_level')}")
    for n in state["notes"]:
        print(f"  - {n}")
    print("HINT:", state["final_hint"])
