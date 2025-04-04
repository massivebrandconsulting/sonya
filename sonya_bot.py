from flask import Flask, request, jsonify
import openai
import os
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Load environment variables
openai.api_key = os.environ['OPENAI_API_KEY']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_HEADERS = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json"
}

# Sonya's voice and role
SONYA_PROMPT = """
You are Sonya, a digital alter ego for a Chief Human Resources Officer at Massive Brand Consulting, led by CEO Tanya. You have 25 years of experience in Human Resources, a DBA in Organizational Leadership, and advanced certifications. You are professional, strategic, and supportive. You specialize in leadership, people operations, DEI, organizational effectiveness, ClickUp, and Bossly. Respond like a confident, no-nonsense HR executive who supports fast-scaling businesses.
"""

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()
    logging.info(f"Incoming event: {data}")

    # 🔐 Slack URL verification
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    event = data.get("event", {})
    event_type = event.get("type")
    channel_type = event.get("channel_type")

    # ✅ Respond to both @mentions and DMs
    if event_type in ["app_mention", "message"] and channel_type in ["im", "channel", "group"]:
        user_message = event.get("text")
        channel_id = event.get("channel")
        logging.info(f"User message: {user_message}")
        logging.info(f"Channel ID: {channel_id}")

        # Clean the message (remove @bot mention if present)
        if ">" in user_message:
            cleaned_prompt = user_message.split(">", 1)[1].strip()
        else:
            cleaned_prompt = user_message.strip()

        logging.info(f"Cleaned prompt: {cleaned_prompt}")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": SONYA_PROMPT},
                    {"role": "user", "content": cleaned_prompt}
                ]
            )
            reply = response['choices'][0]['message']['content']
            logging.info(f"GPT reply: {reply}")
        except Exception as e:
            reply = f"⚠️ Sorry, I had a technical hiccup: {str(e)}"
            logging.error(f"GPT error: {e}")

        # Send the GPT reply to Slack
        slack_response = requests.post("https://slack.com/api/chat.postMessage", headers=SLACK_HEADERS, json={
            "channel": channel_id,
            "text": reply
        })
        logging.info(f"Slack response: {slack_response.text}")

    return jsonify({"status": "ok"})

# Required for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
