from flask import Flask, request, jsonify
import openai
import os
import requests

app = Flask(__name__)

openai.api_key = os.environ['OPENAI_API_KEY']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

SLACK_HEADERS = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json"
}

SONYA_PROMPT = """You are Sonya, a digital alter ego for a Chief Human Resources Officer at Massive Brand Consulting, led by CEO Tanya. You have 25 years of experience in Human Resources, a DBA in Organizational Leadership..."""  # <– Use full prompt

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})
    event = data.get("event", {})
    if event.get("type") == "app_mention" and 'bot_id' not in event:
        user_message = event.get("text")
        channel_id = event.get("channel")
        cleaned_prompt = user_message.replace("<@YOUR_BOT_USER_ID>", "").strip()
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SONYA_PROMPT},
                {"role": "user", "content": cleaned_prompt}
            ]
        )
        reply = response['choices'][0]['message']['content']
        requests.post("https://slack.com/api/chat.postMessage", headers=SLACK_HEADERS, json={
            "channel": channel_id,
            "text": reply
        })
    return jsonify({"status": "ok"})
