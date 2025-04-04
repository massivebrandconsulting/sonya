from flask import Flask, request, jsonify
import openai
import os
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Load API keys
openai.api_key = os.environ['OPENAI_API_KEY']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_HEADERS = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json"
}

# Sonya's system prompt
SONYA_PROMPT = """
You are Sonya, a digital alter ego for a Chief Human Resources Officer at Massive Brand Consulting, led by CEO Tanya.
