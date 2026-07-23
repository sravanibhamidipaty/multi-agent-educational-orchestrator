import gradio as gr

from agents.orchestrator import pipeline, MAX_LEVEL
from agents.intent import is_continuation as _is_continue
from observability.log import new_conversation_id, log_turn
from typing import Any


ESCALATION_MESSAGE: str = (
    "This question has been escalated — please post it on Ed Discussion and a TA "
    "will take a look. This conversation is closed."
)


def chat(message: str, history: list[dict[str, str]], session: dict[str, Any]):
    if session.get("closed"):
        return ESCALATION_MESSAGE

    if not session:
        session.update(
            {
                "conversation_id": new_conversation_id(),
                "turn": 1,
                "level": 1,
                "prior_hints": [],
                "stuck_cycles": 0,
                "question": message
            }
        )
    elif not _is_continue(message):
        session.update(
            {
                "question": message,
                "turn": session["turn"] + 1,
                "level": 1,
                "prior_hints": [],
                "stuck_cycles": 0,
            }
        )

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
        session["closed"] = True
    elif state.get("subquestion"):
        session["stuck_cycles"] = state.get("stuck_cycles", session["stuck_cycles"])
        session["question"] = state["subquestion"]
        session["turn"] += 1
        session["level"] = 1
        session["prior_hints"] = []
    else:
        if state.get("final_hint"):
            session["prior_hints"].append(state["final_hint"])
        session["level"] = min(session["level"] + 1, MAX_LEVEL + 1)

    reason = " | ".join(state.get("notes", []))
    return f"{state.get('final_hint','')}\n\n_(cid={cid[:8]} · turn {turn_no} · {reason})_"


def record_feedback(data: gr.LikeData, session: dict[str, Any]) -> None:
    log_turn(
        event="feedback",
        conversation_id=session.get("conversation_id", "unknown"),
        turn=session.get("turn"),
        liked=data.liked,
        message_index=data.index,
        hint=data.value,
    )


with gr.Blocks(title="Multi Agent Educational Orchestrator") as demo:
    gr.Markdown("## Multi Agent Educational Orchestrator")
    session = gr.State({})
    chat_ui = gr.ChatInterface(
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
    chat_ui.chatbot.like(record_feedback, inputs=[session])

if __name__ == "__main__":
    demo.launch()