from flask import Flask, request, jsonify
import openai
import os
import requests

app = Flask(__name__)

# Load environment variables
openai.api_key = os.environ['OPENAI_API_KEY']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

SLACK_HEADERS = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json"
}

# Sonya's GPT personality
SONYA_PROMPT = """You are Sonya, a digital alter ego for a Chief Human Resources Officer at Massive Brand Consulting..."""  # paste full personality here

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()

    # 🔐 Slack verification challenge — REQUIRED
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # ✅ Handle actual messages
    event = data.get("event", {})
    if event.get("type") == "app_mention" and "bot_id" not in event:
        user_message = event.get("text")
        channel_id = event.get("channel")

        # Clean the message
        cleaned_prompt = user_message.replace("<@YOUR_BOT_USER_ID>", "").strip()

        # GPT response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SONYA_PROMPT},
                {"role": "user", "content": cleaned_prompt}
            ]
        )

        reply = response['choices'][0]['message']['content']

        # Send back to Slack
        requests.post("https://slack.com/api/chat.postMessage", headers=SLACK_HEADERS, json={
            "channel": channel_id,
            "text": reply
        })

    return jsonify({"status": "ok"})
