import gradio as gr

def echo_chat(message, history):
    return f"Hello! I received: {message}"

demo = gr.ChatInterface(
    fn=echo_chat,
    title="Echo Bot (Phase 1 Test)"
)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7861)