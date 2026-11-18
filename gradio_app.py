
import gradio as gr
import os
from google import genai
from PIL import Image

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def chat(message, image):
    text = message or ""

    if not text.strip() and image is None:
        return "Please enter a message or upload an image."

    try:
        print("CHAT FUNCTION CALLED:", text)

        contents = []

        if text.strip():
            contents.append(text)

        if image is not None:
            contents.append(Image.open(image))

        print("SENDING TO GEMINI...")

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=contents
        )

        print("GEMINI RESPONSE:", response.text)

        return response.text or "Gemini couldn't generate a response."

    except Exception as e:
        return f"Gemini Error: {str(e)}"


with gr.Blocks() as demo:
    gr.Markdown("# My Gemini AI App")

    message = gr.Textbox(
        label="Message",
        placeholder="Type your message here..."
    )

    image = gr.Image(
        label="Upload an Image",
        type="filepath"
    )

    output = gr.Textbox(label="Response")

    btn = gr.Button("Send")

    btn.click(
        fn=chat,
        inputs=[message, image],
        outputs=output,
        api_name="chat"
    )

demo.launch()
