from flask import Flask, request, jsonify, render_template
import openai
import webbrowser
import re
from urllib.parse import quote_plus

app = Flask(__name__)

client = openai.OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

chat_history = [{"role": "system", "content": "You are a cheerful, AI assistant."}]

site_map = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chat.openai.com",
    "stackoverflow": "https://stackoverflow.com",
    "gmail": "https://mail.google.com"
}

def open_youtube_search_if_requested(user_text):
    match = re.search(r"play (.+) on youtube", user_text.lower())
    if match:
        song = match.group(1)
        search_url = f"https://www.youtube.com/results?search_query={quote_plus(song)}"
        webbrowser.open(search_url)
        return True
    return False

def open_website(user_text):
    if open_youtube_search_if_requested(user_text):
        return
    for key in site_map:
        if key in user_text.lower():
            webbrowser.open(site_map[key])
            break

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    chat_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=chat_history
    )
    reply = response.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": reply})

    open_website(user_message)

    # Return reply and a flag if joke keywords found in reply (to help frontend)
    joke_keywords = ['joke', 'haha', 'lol', 'funny', 'laugh']
    is_joke = any(word in reply.lower() for word in joke_keywords)

    return jsonify({"reply": reply, "is_joke": is_joke})

if __name__ == "__main__":
    app.run(debug=True)
