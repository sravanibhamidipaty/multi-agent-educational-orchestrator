import sys
import httpx
import numpy as np
from sklearn.metrics import average_precision_score

from agents.verification_agent import selfcheck, SAMPLE_SYSTEM_PROMPT
from evaluation.labeled_hints import LABELED, counts

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2:7b"


def _ollama_chat(messages, temperature: float, max_tokens: int) -> str:
    resp = httpx.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        },
        timeout=180,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def ollama_sampler(question: str, temperature: float = 1.0) -> str:
    # high temperature -> stochastic samples (the core of SelfCheckGPT)
    return _ollama_chat(
        [
            {"role": "system", "content": SAMPLE_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature,
        200,
    )


def ollama_checker(prompt: str, temperature: float = 0.0) -> str:
    return _ollama_chat([{"role": "user", "content": prompt}], temperature, 5)


def score_dataset(limit: int | None = None):
    items = LABELED if limit is None else _balanced_subset(limit)
    y_true, y_score = [], []
    for i, item in enumerate(items, start=1):
        result = selfcheck(
            item["question"], item["answer"],
            sampler=ollama_sampler, checker=ollama_checker, use_cache=False,
        )
        y_true.append(item["label"])
        y_score.append(result["hallucination_score"])
        print(f"[{i:>3}/{len(items)}] label={item['label']} "
              f"score={result['hallucination_score']:.3f}  {item['question'][:50]}")
    return np.array(y_true), np.array(y_score)


def _balanced_subset(limit: int):
    half = limit // 2
    pos = [x for x in LABELED if x["label"] == 1][:half]
    neg = [x for x in LABELED if x["label"] == 0][:half]
    out = []
    for n, p in zip(neg, pos):
        out.extend([n, p])
    return out


def evaluate(limit: int | None = None, save_plot: bool = True):
    print("Dataset:", counts(), "| running:", limit if limit else "all")
    y_true, y_score = score_dataset(limit)

    auc_pr = average_precision_score(y_true, y_score)
    baseline = y_true.mean()  # PR-AUC of a random classifier = positive rate

    # PR-AUC (above) is threshold-independent. For the operating point we must match the
    # orchestrator's gate exactly: it REJECTS (predicts hallucinated) when score > THRESHOLD.
    # So sweep candidate thresholds at midpoints between observed scores and maximize F1
    # of the positive (hallucinated) class under that ">" rule.
    uniq = np.unique(y_score)
    candidates = [(uniq[i] + uniq[i + 1]) / 2 for i in range(len(uniq) - 1)]
    candidates = candidates or [float(uniq[0])]

    def f1_at(t: float) -> tuple[float, float, float]:
        pred = y_score > t                      # predicted hallucinated == rejected
        tp = int(np.sum(pred & (y_true == 1)))
        fp = int(np.sum(pred & (y_true == 0)))
        fn = int(np.sum(~pred & (y_true == 1)))
        p = tp / (tp + fp) if (tp + fp) else 0.0
        r = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * p * r / (p + r) if (p + r) else 0.0
        return f1, p, r

    best_threshold = max(candidates, key=lambda t: f1_at(t)[0])
    best_f1, best_p, best_r = f1_at(best_threshold)

    print("\n" + "=" * 55)
    print(f"SelfCheckGPT hallucination detection  (model={OLLAMA_MODEL})")
    print("=" * 55)
    print(f"PR-AUC (NonFactual) : {auc_pr:.3f}")
    print(f"Random baseline     : {baseline:.3f}")
    print(f"Best threshold      : {best_threshold:.3f}  (gate: reject if score > threshold)")
    print(f"  precision={best_p:.2f}  recall={best_r:.2f}  F1={best_f1:.2f}")
    print("\nNote: orchestrator approves when hallucination_score <= THRESHOLD.")
    print(f"Suggested HALLUCINATION_THRESHOLD = {best_threshold:.2f}")

    if save_plot:
        import json
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from pathlib import Path
        from sklearn.metrics import precision_recall_curve
        Path("docs").mkdir(exist_ok=True)

        # persist raw scores so the plot/metrics can be rebuilt without re-calling the model
        with open("docs/eval_scores.json", "w") as f:
            json.dump({
                "model": OLLAMA_MODEL,
                "pr_auc": auc_pr,
                "baseline": float(baseline),
                "threshold": best_threshold,
                "y_true": [int(v) for v in y_true],
                "y_score": [float(v) for v in y_score],
            }, f, indent=2)

        prec_c, rec_c, _ = precision_recall_curve(y_true, y_score)
        plt.figure()
        plt.plot(rec_c, prec_c, label=f"SelfCheck (AP={auc_pr:.2f})")
        plt.axhline(baseline, ls="--", color="gray", label=f"random={baseline:.2f}")
        plt.xlabel("Recall"); plt.ylabel("Precision")
        plt.title(f"Hallucination detection PR curve ({OLLAMA_MODEL}, N={len(y_true)})")
        plt.legend(); plt.grid(True, alpha=0.3)
        plt.savefig("docs/pr_curve.png", dpi=150, bbox_inches="tight")
        print("Saved docs/pr_curve.png and docs/eval_scores.json")

    return auc_pr, best_threshold


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    evaluate(limit)
