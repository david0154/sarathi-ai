# app/app.py — Sarathi AI Gradio Web Demo
import sys
sys.path.append("..")

import gradio as gr
from src.pipeline import sarathi


def initialize_model():
    """Initialize model and vector store."""
    try:
        sarathi.load_model()
        sarathi.load_vectorstore()
        return "✅ Sarathi AI is ready! Ask me anything about India."
    except Exception as e:
        return f"❌ Error: {e}"


def chat(message: str, history: list) -> str:
    """Process user message and return Sarathi's response."""
    if not message.strip():
        return "Please ask me something!"
    try:
        return sarathi.query(message)
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"


with gr.Blocks(
    title="Sarathi AI — India's Multi-Domain Assistant",
    theme=gr.themes.Soft(primary_hue="teal")
) as demo:

    gr.Markdown("""
    # 🇮🇳 Sarathi AI
    ### India's Multi-Domain AI Assistant | By David @ Nexuzy Lab, Kolkata

    **I can help with:**
    - ⚖️ Indian Law (IPC, Constitution, Legal Q&A)
    - 🛕 Religions (Gita, Quran, Bible)
    - 🏨 Travel (Kolkata hotels, places, routes)
    - 🌐 General Indian Knowledge
    - 💻 Coding (Python, Kotlin, JavaScript)

    **Languages:** English | हिंदी | বাংলা
    """)

    with gr.Row():
        init_btn = gr.Button("🚀 Initialize Sarathi AI", variant="primary", scale=1)
        status_box = gr.Textbox(label="Status", value="Click Initialize to load the model", scale=3)

    init_btn.click(fn=initialize_model, outputs=status_box)

    chatbot = gr.ChatInterface(
        fn=chat,
        examples=[
            "What is IPC Section 302?",
            "Best hotel in Kolkata under ₹2000?",
            "What does the Bhagavad Gita say about karma?",
            "भारत का संविधान कब लागू हुआ?",
            "কলকাতার বিখ্যাত খাবার কী কী?",
            "Write a Python function to reverse a string",
        ],
        title="Ask Sarathi AI",
        description="Ask in English, Hindi, or Bengali",
    )


if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
