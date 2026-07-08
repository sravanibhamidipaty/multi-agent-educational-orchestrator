from dataclasses import dataclass, field
from collections.abc import Callable
from groq import Groq
from config import GROQ_API_KEY
from retrieval.retriever import retrieve

# Set up groq client
client: Groq = Groq(api_key=GROQ_API_KEY)

# LLM call format: (system_prompt, user_prompt, temperature) -> text.
LLMCall = Callable[[str, str, float], str]

HINT_LEVELS: dict[int, str] = {
    1: "Level 1 (nudge): name the relevant concept or point to the chapter, with no specifics",
    2: "Level 2 (context): give the key definition or relationship from the textbook context.",
    3: "Level 3 (scaffold): a guiding question or partial reasoning step that stops before the answer.",
}

MAX_LEVEL: int = max(
    HINT_LEVELS
)  # Level 3 is the floor; there is no level that reveals the answer.

HINT_SYSTEM_PROMPT: str = """
You are an upbeat, encouraging tutor for CS 7280: Network Science, grounded strictly
in Barabási's Network Science textbook. Your role is to help students understand concepts
by guiding them step-by-step with hints and not by giving away answers directly.

Given a student's question and the retrieved textbook context, produce EXACTLY ONE hint at the requested level.
The hint must:
    - Use precise network science terminology from the textbook
    - Build on any hints already shown, revealing a little more without repeating them
    - Be grounded only in the provided context. Do not introduce concepts outside the textbook
    - Match the requested level of detail:
        {level_desc}
    - Give enough scaffolding for the student to reason through the next step themselves

GUARDRAILS
You must never:
- State the final answer or solution explicitly
- Provide a numbered step-by-step solution to the student's problem
- Complete a proof or derivation fully
- Use phrases like "the answer is", "the result is", "therefore X equals", or "the solution is"
- Reveal information that removes the need for the student to think

Stop just before the insight: give context and scaffold, but leave the reasoning step for the student.

Produce only the hint text, nothing else.
"""

# Used only when the student is still stuck after Level 3.
# Treat the stuck state as new hint data and restart the ladder on a smaller
# prerequisite sub-concept, rather than ever revealing the answer.
DECOMPOSE_SYSTEM_PROMPT: str = """
You are a tutor for CS 7280: Network Science. The student is still stuck
even after the most detailed hint allowed. Using ONLY the provided textbook
context, identify ONE smaller prerequisite concept the student most likely needs
to understand first.

Output only that as a single short sub-question. Do NOT answer it, and do not
reveal the solution to the original question.
"""


@dataclass
class HintData:
    kind: str  # "retrieved passage | hint"
    content: str
    level: int = 0
    relevance: float = 0.0  # retrieval score in [0, 1]
    meta: dict[str, object] = field(default_factory=dict)


def _default_llm(system: str, user: str, temperature: float = 0.3) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
        max_tokens=250,
    )
    return response.choices[0].message.content


# Step 1: Transformation (question -> pool of textbook passages)
# Retrieval breadth (k) vs. selection (top_n) are distinct:
# k = how many passages this step retrieves BEFORE selection.
# top_n = how many survive narrow_down and actually feed the hint (matches app.py's 3 sources).
# Keep k > top_n (e.g. k=5, top_n=3) so the downstream narrow-down step does real work: it selects
# the best top_n by the relevance + quality criteria. If k == top_n, narrow_down keeps everything
# and the quality criterion becomes a no-op (only the min_relevance filter remains). app.py uses
# k=3 because it has no narrow-down stage; the hint agent has one, so retrieving extra then
# selecting is the correct pattern.
def transform_retrieve(question: str, k: int = 5) -> list[HintData]:
    hits = retrieve(question, k=k)
    return [
        HintData(
            kind="passage",
            content=hit["text"],
            relevance=hit["score"],
            meta={"chapter": hit["chapter"], "chunk_index": hit["chunk_index"]},
        )
        for hit in hits
    ]


# Step 2: Narrow Down based on two constraints
def narrow_down(
    pool: list[HintData], min_relevance: float = 0.0, top_n: int | None = None
) -> list[HintData]:
    """
    Narrow-down step, with two criteria:
        relevance criterion : keep passages relevant to the student's question (score >= min_relevance)
        quality criterion   : keep only the top_n highest-scoring passages
    """
    selected = [d for d in pool if d.relevance >= min_relevance]
    selected.sort(key=lambda d: d.relevance, reverse=True)
    return selected[:top_n] if top_n is not None else selected


def _passages_to_dicts(context_data: list[HintData]) -> list[dict[str, object]]:
    return [
        {
            "chapter": d.meta["chapter"],
            "chunk_index": d.meta["chunk_index"],
            "score": d.relevance,
            "text": d.content,
        }
        for d in context_data
    ]


def _context_string(context_passages: list[dict[str, object]]) -> str:
    return "\n\n".join(
        f"[Chapter {p['chapter']}]: {p['text']}" for p in context_passages
    )


# Step 3: passages -> ONE level-appropriate hint starting with a nudge
def render_hint(
    question: str,
    context_passages: list[dict[str, object]],
    level: int = 1,
    prior_hints: list[str] | None = None,
    llm: LLMCall = _default_llm,
) -> str:
    if level not in HINT_LEVELS:
        raise ValueError(f"level must be one of {list(HINT_LEVELS)}, got {level}")
    prior = (
        "\n".join(f"- (level {i + 1}) {h}" for i, h in enumerate(prior_hints or []))
        or "none"
    )
    return llm(
        HINT_SYSTEM_PROMPT.format(level_desc=HINT_LEVELS[level]),
        f"Student question: {question}\n\nTextbook context:\n{_context_string(context_passages)}\n\n"
        f"Hints already shown to this student:\n{prior}\nNow produce ONLY the level {level} hint.",
        0.3,
    ).strip()


def generate_hint(
    question: str,
    level: int = 1,
    prior_hints: list[str] | None = None,
    k: int = 5,
    min_relevance: float = 0.15,
    top_n: int = 3,
    llm: LLMCall = _default_llm,
) -> dict[str, object]:
    context_data = narrow_down(transform_retrieve(question, k=k), min_relevance, top_n)
    passages = _passages_to_dicts(context_data)
    hint = render_hint(
        question, passages, level=level, prior_hints=prior_hints, llm=llm
    )
    return {
        "question": question,
        "level": level,
        "hint": hint,
        "max_level": MAX_LEVEL,
        "exhausted": level >= MAX_LEVEL,
        "context": passages,
    }


# If all 3 levels of HINTS are exhausted then decompose to a prerequisite sub-concept
def decompose(
    question: str,
    context_passages: list[dict[str, object]],
    prior_hints: list[str] | None = None,
    llm: LLMCall = _default_llm,
) -> str:
    prior = "\n".join(f"- {h}" for h in (prior_hints or [])) or "(none)"
    return llm(
        DECOMPOSE_SYSTEM_PROMPT,
        f"Original question: {question}\n\nTextbook context:\n{_context_string(context_passages)}\n\n"
        f"Hints already tried:\n{prior}\n\nGive one prerequisite sub-question.",
        0.3,
    ).strip()


def next_level(current_level: int) -> int:
    return current_level + 1


if __name__ == "__main__":
    # Simulate a multi-turn dialogue: the student keeps asking for more, so the AI climbs 1 -> 2 -> 3.
    question: str = "How does the scale-free network form?"
    print(f"Question: {question}")

    shown: list[str] = []
    level: int = 1
    while level <= MAX_LEVEL:
        result = generate_hint(question, level=level, prior_hints=shown)
        print(f"\n{'-' * 70}")
        print(f"[Level {result['level']} / {result['max_level']}]")
        print(f"{'-' * 70}")
        print(result["hint"])
        shown.append(result["hint"])
        level: int = next_level(level)