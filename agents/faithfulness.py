import re
from collections.abc import Callable
from groq import Groq
from config import GROQ_API_KEY

client: Groq = Groq(api_key=GROQ_API_KEY)

LLMCall = Callable[[str, float], str]  # (prompt, temperature) -> completion text

FAITHFULNESS_PROMPT: str = """
You are verifying whether a tutor's statement is FAITHFUL to the source
textbook passages -- that is, whether it can be inferred from them alone.

Source passages (each tagged with its chapter):
{context}

Statement: {statement}

Answer in exactly this format:
Verdict: <Yes or No>
Source: <the chapter number that best supports the statement, or None>
Reason: <one sentence naming what in the source does or does not support the statement
"""


def _default_llm(prompt: str, temperature: float = 0.0) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=120,
    )

    return response.choices[0].message.content


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def check_sentence(
    sentence: str, context: str, llm: LLMCall = _default_llm
) -> dict[str, object]:
    raw = llm(FAITHFULNESS_PROMPT.format(context=context, statement=sentence), 0.0)
    verdict = re.search(r"verdict:\s*(yes|no)", raw, re.IGNORECASE)
    source = re.search(r"source:\s*(.+)", raw, re.IGNORECASE)
    reason = re.search(r"reason:\s*(.+)", raw, re.IGNORECASE | re.DOTALL)
    return {
        "sentence": sentence,
        "faithful": bool(verdict) and verdict.group(1).lower() == "yes",
        "source": source.group(1).strip()
        if source
        else "None",  # Chapter from the textbook
        "reason": reason.group(1).strip() if reason else raw.strip(),
    }


def source_faithfulness(
    answer: str, context_passages: list[dict[str, object]], llm: LLMCall = _default_llm
) -> dict[str, object]:
    context = "\n\n".join(
        f"[Chapter {p['chapter']}]: {p['text']}" for p in context_passages
    )
    checks = [check_sentence(s, context, llm) for s in split_sentences(answer)]
    score = sum(c["faithful"] for c in checks) / len(checks) if checks else 0.0
    return {
        "faithfulness_score": round(score, 4),
        "checks": checks,
        "unfaithful": [c for c in checks if not c["faithful"]],
    }


if __name__ == "__main__":
    passages = [
        {
            "chapter": 5,
            "text": "In the Barabási-Albert model, new nodes attach preferentially to high-degree nodes, so hubs emerge through a rich-get-richer process.",
        }
    ]
    answer = (
        "Preferential attachment means new nodes tend to link to high-degree nodes. "
        "This is why the model produces a Poisson degree distribution."
    )
    response = source_faithfulness(answer, passages)
    print(f"Faithfulness score: {response['faithfulness_score']:.2f}")
    for c in response["checks"]:
        print(
            f"  [{'OK ' if c['faithful'] else 'BAD'}] src={c['source']} :: {c['sentence']}"
        )
        print(f"    reason: {c['reason']}")
