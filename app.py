import gradio as gr

def chatbot(message):
    return f"AI response: {message}"

demo = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(label="Message"),
    outputs=gr.Textbox(label="Response"),
    title="Slack Gradio Bot"
)

demo.launch()