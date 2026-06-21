from retrieval.retriever import retrieve
import gradio as gr

def chat(message, history):
    hits = retrieve(message, k=3)
    summary_context = "\n\n".join(f"[Chapter {h['chapter']}]: {h['text'][:300]}" for h in hits)
    answer = "Based on the Network Science textbook, here is what is relevant to your question:\n\n"

    for h in hits:
        answer += f"**Chapter {h['chapter']}** (relevance: {h['score']}):\n"
        answer += f"{h['text'][:400]}\n\n"
    answer += "---\n**Sources:**\n"

    for i, h in enumerate(hits):
        answer += f"{i+1}. Chapter {h['chapter']}, chunk {h['chunk_index']} (score:{h['score']})\n"
        answer += f"   *\"{h['text'][:100]}...\"*\n"
    return answer

demo = gr.ChatInterface(fn=chat,
                        title="Network Science Tutor",
                        description="Ask questions about CS 7280: Network Science grounded in Barabási's textbook.",
                         examples=[
                          "What is a node in a network?",
                          "How does a scale-free network form?",
                          "What is the clustering coefficient?",
                          "What makes a network robust?",
                        ])

if __name__ == "__main__":
    demo.launch()