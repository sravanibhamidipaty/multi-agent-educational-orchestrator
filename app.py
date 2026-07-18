import gradio as gr

from agents.orchestrator import pipeline, MAX_LEVEL
from observability.log import new_conversation_id
from typing import Any

def chat(message: str, history: list[dict[str, str]], session: dict[str, Any]):
    if not session:
        session.update(
            {
                "conversation_id": new_conversation_id(),
                "turn": 0,
                "level": 1,
                "prior_hints": [],
                "stuck_cycles": 0,
                "question": message
            }
        )

    session["turn"] += 1

    state = pipeline.invoke({
        "conversation_id": session["conversation_id"],
        "turn": session["turn"],
        "question": session["question"],
        "level": session["level"],
        "prior_hints": session["prior_hints"],
        "stuck_cycles": session["stuck_cycles"],
        "context": []
    }
    )

    cid = session["conversation_id"]
    turn_no = session["turn"]

    if state.get("escalate_to_human"):
        session.clear()
    elif state.get("subquestion"):
        session["stuck_cycles"] = state.get("stuck_cycles", session["stuck_cycles"])
        session["question"] = state["subquestion"]
        session["level"] = MAX_LEVEL + 1
    else:
        if state.get("final_hint"):
            session["prior_hints"].append(state["final_hint"])
        session["level"] = min(session["level"] + 1, MAX_LEVEL + 1)

    reason = " | ".join(state.get("notes", []))
    return f"{state.get('final_hint','')}\n\n_(cid={cid[:8]} · turn {turn_no} · {reason})_"


with gr.Blocks(title="Multi Agent Educational Orchestrator") as demo:
    gr.Markdown("## Multi Agent Educational Orchestrator")
    session = gr.State({})
    gr.ChatInterface(
        fn=lambda m, h, s : chat(m, h, s),
        additional_inputs=[session],
        description="Ask questions about CS 7280: Network Science grounded in Barabási's textbook.",
        examples=[
            ["What is a node in a network?"],
            ["How does a scale-free network form?"],
            ["What is the clustering coefficient?"],
            ["What makes a network robust?"],
        ]
    )

if __name__ == "__main__":
    demo.launch()