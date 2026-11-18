from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from gradio_client import Client, handle_file
import httpx
import os
import re

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

gradio_client = Client(
    "http://127.0.0.1:7862/"
)


def download_image(url, filename):
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    response = httpx.get(url, headers=headers)

    image_path = f"./images/{filename}"
    os.makedirs("./images", exist_ok=True)

    with open(image_path, "wb") as f:
        f.write(response.content)

    return image_path


def slackify_message(message):
    pattern = r'\[(.*?)\]\((.*?)\)'
    cleaned = re.sub(pattern, r'<\2|\1>', message)
    cleaned = re.sub(r'```\w+\n', '```', cleaned)
    return cleaned.strip()

@app.event("app_mention")
def handle_app_mention_events(body, say):
    print("EVENT RECEIVED!!!")
    try:
        text = body["event"]["text"]
        bot_user_id = body["authorizations"][0]["user_id"]

        clean_message = text.replace(
            f"<@{bot_user_id}>", ""
        ).strip()

        files = []

        if "files" in body["event"]:
            for file in body["event"]["files"]:
                if file["filetype"] in [
                    "png", "jpg", "jpeg", "gif", "webp"
                ]:
                    image_path = download_image(
                        file["url_private_download"],
                        file["name"]
                    )
                    files.append(handle_file(image_path))
                    break

        result = gradio_client.predict(
           message=clean_message,
           image=files[0] if files else None,
           api_name="/chat"
)

        print("GRADIO RESULT:", repr(result))
        say(slackify_message(result))

    except Exception as e:
        print("ERROR OCCURRED:", repr(e))
        say(f"Error: {e}")

if __name__ == "__main__":
    handler = SocketModeHandler(
        app,
        SLACK_APP_TOKEN
    )

    handler.start()