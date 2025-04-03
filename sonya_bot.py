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

    # ✅ This is what Slack needs for verification
    if data and data.get("type") == "url_verification":
        challenge = data.get("challenge")
        return jsonify({"challenge": challenge})

    # 🧠 Later: Handle mentions or DMs
    return jsonify({"status": "ok"})
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
