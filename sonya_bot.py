    event = data.get("event", {})
    event_type = event.get("type")
    channel_type = event.get("channel_type")

    if event_type in ["app_mention", "message"] and channel_type in ["im", "channel", "group"]:
        user_message = event.get("text")
        channel_id = event.get("channel")
        logging.info(f"User message: {user_message}")
        logging.info(f"Channel ID: {channel_id}")

        # Clean prompt (strip @Sonya if present)
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
            reply = f"Sorry, I had a technical hiccup: {e}"
            logging.error(f"GPT error: {e}")

        # Send message to Slack
        slack_response = requests.post("https://slack.com/api/chat.postMessage", headers=SLACK_HEADERS, json={
            "channel": channel_id,
            "text": reply
        })
        logging.info(f"Slack response: {slack_response.text}")
