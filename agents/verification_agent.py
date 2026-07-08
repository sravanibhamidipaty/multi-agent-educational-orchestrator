import re
from collections.abc import Callable
from groq import Groq
from config import GROQ_API_KEY

client: Groq = Groq(api_key=GROQ_API_KEY)
N_SAMPLES: int = 4

SAMPLE_SYSTEM_PROMPT: str = """
You are a tutor for CS 7280: Network Science grounded in Barabási's
Network Science textbook. Answer the student's question in 2-3 concise
sentences using precise network science terminology.
"""

CHECK_PROMPT_TEMPLATE: str = """
Context: {sample}

Sentence: {sentence}

Is the sentence supported by the context above? Answer only "Yes" or "No".
"""

SamplerCall = Callable[[str, float], str]  # (question, temperature) -> sampled answer
CheckerCall = Callable[[str, float], str]  # (prompt, temperature) -> "Yes"/"No"


def _default_sampler(question: str, temperature: float = 1.0) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SAMPLE_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=temperature,  # HIGH temperature -> stochastic samples (the core of the method)
        max_tokens=200,
    )

    return response.choices[0].message.content


def _default_checker(prompt: str, temperature: float = 0.0) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,  # deterministic support judgement
        max_tokens=5,
    )

    return response.choices[0].message.content


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def generate_samples(question: str, sampler: SamplerCall, n: int = N_SAMPLES) -> list[str]:
    return [sampler(question, 1.0) for _ in range(n)]


# 0.0 = supported, 1.0 hallucinated
def sentence_score(
    sentence: str, samples: list[str], checker: CheckerCall) -> float:
    votes = []
    for sample in samples:
        verdict = checker(
            CHECK_PROMPT_TEMPLATE.format(sample=sample, sentence=sentence), 0.0
        )
        votes.append(0.0 if verdict.strip().lower().startswith("yes") else 1.0)

    return sum(votes) / len(votes) if votes else 0.0


def selfcheck(
    question: str,
    answer: str,
    n: int = N_SAMPLES,
    sampler: SamplerCall = _default_sampler,
    checker: CheckerCall = _default_checker,
) -> dict[str, object]:
    samples = generate_samples(question, sampler, n)
    per_sentence = [
        {"sentence": s, "score": round(sentence_score(s, samples, checker), 4)}
        for s in split_sentences(answer)
    ]
    passage = (
        sum(p["score"] for p in per_sentence) / len(per_sentence)
        if per_sentence
        else 0.0
    )
    return {
        "question": question,
        "answer": answer,
        "n_samples": n,
        "samples": samples,
        "sentence_scores": per_sentence,
        "hallucination_score": round(passage, 4),
    }


if __name__ == "__main__":
    question = "What is preferential attachment?"
    answer = (
        "Preferential attachment means new nodes tend to link to nodes that already have high "
        "degree. This rich-get-richer dynamic drives the emergence of hubs in the Barabási-Albert "
        "model."
    )
    response = selfcheck(question, answer)
    false_answer = (
        "Preferential attachment means new nodes connect to random nodes with equal probability. "
        "This produces a Poisson degree distribution with no hubs."
    )
    response1 = selfcheck(question, false_answer)
    for p in response["sentence_scores"]:
        print(f"[{p['score']:.2f}] {p['sentence']}")
    print(f"\nHallucination score: {response['hallucination_score']:.2f} (0.0=grounded, 1.0=hallucinated)")

    for p in response1["sentence_scores"]:
        print(f"[{p['score']:.2f}] {p['sentence']}")
    print(f"\nHallucination score: {response1['hallucination_score']:.2f} (0.0=grounded, 1.0=hallucinated)")
