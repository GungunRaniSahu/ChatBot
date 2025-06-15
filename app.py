from flask import Flask, render_template, request, jsonify
import os
import httpx
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_response():
    user_input = request.json["message"]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:5000",  
        "X-Title": "ZiZiChatBot"
    }

    data = {
        "model": "openai/gpt-3.5-turbo", 

        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
        result = response.json()

        if "choices" in result:
            bot_reply = result["choices"][0]["message"]["content"].strip()
        elif "error" in result:
            bot_reply = f"API error: {result['error'].get('message', 'Unknown error')}"
        else:
            bot_reply = f"Unexpected response format: {result}"
    except Exception as e:
        bot_reply = f"Sorry, something went wrong: {str(e)}"

    time_now = datetime.now().strftime("%H:%M:%S")
    return jsonify({"response": bot_reply, "time": time_now})


if __name__ == "__main__":
    app.run(debug=True)
