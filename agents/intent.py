from collections.abc import Callable

import numpy as np
from groq import Groq

from config import GROQ_API_KEY
from retrieval.basic_rag import model

CONTINUE_PROTOTYPES: list[str] = [
    "more", "tell me more", "give me more detail", "more detail",
    "next", "next hint", "give me another hint", "another hint",
    "continue", "go on", "keep going", "carry on",
    "what else", "and then", "elaborate", "explain further",
    "i still don't get it", "i'm still stuck", "hint please",
]


HIGH_CONFIDENCE: float = 0.70
LOW_CONFIDENCE: float = 0.55

_CONT_EMB: np.ndarray = model.encode(CONTINUE_PROTOTYPES, normalize_embeddings=True)

_client: Groq = Groq(api_key=GROQ_API_KEY)
_INTENT_MODEL: str = "llama-3.3-70b-versatile"
_INTENT_SYSTEM: str = (
    "You label a student's message in a tutoring chat as exactly one word.\n"
    "CONTINUE - a content-free request for more of the current hint "
    "(e.g. 'more', 'keep going', 'what else', 'ok').\n"
    "NEW - the student is asking a new question or naming a new topic.\n"
    "Reply with only CONTINUE or NEW."
)

IntentCall = Callable[[str], bool]


def _llm_is_continuation(message: str) -> bool:
    response = _client.chat.completions.create(
        model=_INTENT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": _INTENT_SYSTEM},
            {"role": "user", "content": message},
        ],
    )
    return response.choices[0].message.content.strip().upper().startswith("CONTINUE")


def continuation_score(message: str) -> float:
    emb = model.encode(message, normalize_embeddings=True)
    return float(np.max(_CONT_EMB @ emb))


def is_continuation(message: str, fallback: IntentCall = _llm_is_continuation) -> bool:
    if not message.strip().rstrip("?.! "):
        return True
    score = continuation_score(message)
    if score >= HIGH_CONFIDENCE:
        return True
    if score <= LOW_CONFIDENCE:
        return False
    return fallback(message)  # ambiguous -> ask the LLM


if __name__ == "__main__":
    cases = {
        "more": True, "?": True, "ok": True, "keep going": True,
        "what else can you tell me": True, "i need another nudge": True,
        "go on then": True, "can you elaborate": True,
        "still confused, more please": True, "next one": True,
        "What is a node?": False, "What is a node in a network?": False,
        "what is a hub": False, "define modularity": False,
        "what is preferential attachment": False,
        "how does a scale-free network form?": False,
        "why are hubs important for robustness": False,
        "ok so what about the clustering coefficient then": False,
    }
    ok = 0
    for msg, want in cases.items():
        score = continuation_score(msg) if msg.strip().rstrip("?.! ") else 1.0
        band = "HIGH" if score >= HIGH_CONFIDENCE else "LOW" if score <= LOW_CONFIDENCE else "LLM"
        got = is_continuation(msg)
        ok += got == want
        print(f"{'OK  ' if got == want else 'FAIL'} {band:4} score={score:.3f} "
              f"got={got} want={want}  {msg!r}")
    print(f"{ok}/{len(cases)} correct")
